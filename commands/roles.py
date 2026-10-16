import disnake
from disnake.ext import commands
from init import bot
from config import DEPARTMENT_CHANNEL, DEPARTMENT_CONFIG
from helpers.permissions import ROLE_RULES, check_permissions

async def give_role(member: disnake.Member, role: disnake.Role) -> None:
    await member.add_roles(role)

async def take_role(member: disnake.Member, role: disnake.Role) -> None:
    await member.remove_roles(role)

# Функция для снятия/удаления роли у юзера.
@bot.command(name="role")
async def role_command(ctx, action: str = None, 
member: disnake.Member = None, *, role_name: str = None) -> None:
    if not action or not member or not role_name:
        await ctx.send("Использование: `role <add/remove> @пользователь Имя Роли` ")
        return

    # Проверка на корректный ввод команды.
    action = action.lower()
    if action not in ["add", "remove"]:
        await ctx.send("Неверное действие! Используйте `add` или `remove`.")
        return

    # Проверка на корректный ввод указанной роли.
    role = disnake.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Роль '{role_name}' не найдена на сервере.")
        return

    # Проверка на возможность выдачи опредленной роли юзеру.
    # Для подробностей -> permissions.py.
    # Если кратко - Глава отдела может выдавать только роли своего отдела.
    if not check_permissions(ctx, role.name):
        await ctx.send("У вас недостаточно прав для управления этой ролью!")
        return

    # Добавление роли юзеру.
    if action == "add":
        if role in member.roles:
            await ctx.send(f"У пользователя {member.display_name} уже есть роль **{role.name}**.")
            return

        # Дополнительная проверка на возможноть выдать боту роль с BIG правами.
        try:
            await give_role(member, role)
            await ctx.send(f"Роль **{role.name}** успешно выдана пользователю {member.mention}!")
        except disnake.Forbidden:
            await ctx.send("У бота недостаточно прав для выдачи этой роли.")

    # Снятие роли с юзера.
    elif action == "remove":
        # Вывод сообщения о отсутствии у юзера указанной роли.
        if role not in member.roles:
            await ctx.send(f"У пользователя {member.display_name} отсутствует роль **{role.name}**.")
            return

        # Дополнительная проверка на возможноть снять боту роль с BIG правами. (да я копипастнул текст, что вы мне сделаете?) 
        try:
            await take_role(member, role)
            await ctx.send(f"Роль **{role.name}** успешно снята у пользователя {member.mention}!")
        except disnake.Forbidden:
            await ctx.send("У бота недостаточно прав для снятия этой роли.")


def is_in_project(member: disnake.Member) -> bool:
    all_names = set()
    for cfg in DEPARTMENT_CONFIG.values():
        all_names.update(cfg["titles"])
        all_names.update(cfg["base_roles"])
    return any(r.name in all_names for r in member.roles)


@bot.command(name="department")
async def department_command(ctx, action: str = None, member: disnake.Member = None, department_key: str = None, tier: int = 0, full_remove: str = None) -> None:
    if not action or not member or not department_key:
        await ctx.send("Использование: `department <add/remove> @пользователь <отдел> [тир: 0/1] [all]`")
        return

    action = action.lower()
    if action not in ["add", "remove"]:
        await ctx.send("Неверное действие! Используйте `add` или `remove`.")
        return

    dep_key = department_key.lower()
    if dep_key not in DEPARTMENT_CONFIG:
        await ctx.send(f"Отдел '{department_key}' не найден. Доступные отделы: {', '.join(DEPARTMENT_CONFIG.keys())}")
        return

    config = DEPARTMENT_CONFIG[dep_key]
    titles = config["titles"]
    base_role_names = config["base_roles"]

    if not check_permissions(ctx, config["name"]):
        await ctx.send("У вас недостаточно прав для управления этим отделом!")
        return

    if action == "add":
        if tier >= len(titles):
            tier = len(titles) - 1
        target_title_name = titles[tier]
        junior_title_name = titles[0] if len(titles) > 1 else None

        target_role = disnake.utils.get(ctx.guild.roles, name=target_title_name)
        if not target_role:
            await ctx.send(f"Роль '{target_title_name}' не найдена на сервере.")
            return

        was_in_project = is_in_project(member)
        promoted = False
        gave_anything = False

        try:
            if junior_title_name and junior_title_name != target_title_name:
                junior_role = disnake.utils.get(ctx.guild.roles, name=junior_title_name)
                if junior_role and junior_role in member.roles:
                    await take_role(member, junior_role)
                    promoted = True

            if target_role not in member.roles:
                await give_role(member, target_role)
                gave_anything = True

            for b_name in base_role_names:
                b_role = disnake.utils.get(ctx.guild.roles, name=b_name)
                if b_role and b_role not in member.roles:
                    await give_role(member, b_role)
                    gave_anything = True

            if promoted:
                await ctx.send(f"Пользователь {member.mention} повышен до: **{target_role.name}**, поздравим его!")
            elif gave_anything:
                if was_in_project:
                    await ctx.send(f"Пользователь {member.mention} вступает в отдел: **{target_role.name}**, поздравим его!")
                else:
                    await ctx.send(f"Пользователь {member.mention} вступает в команду проекта в роли: **{target_role.name}**, поздравим его!")
            else:
                await ctx.send(f"У пользователя {member.mention} уже есть все необходимые роли этого отдела.")

        except disnake.Forbidden:
            await ctx.send("У бота недостаточно прав для выдачи ролей.")

    elif action == "remove":
        try:
            removed_roles_list = []
            is_full_removal = full_remove and full_remove.lower() == "all"

            if is_full_removal:
                for r_name in titles + base_role_names:
                    r_obj = disnake.utils.get(ctx.guild.roles, name=r_name)
                    if r_obj and r_obj in member.roles:
                        await take_role(member, r_obj)
                        removed_roles_list.append(r_obj.name)

                if removed_roles_list:
                    await ctx.send(f"Пользователь {member.mention} покидает команду проекта, желаем удачи!")
                else:
                    await ctx.send(f"У пользователя {member.mention} отсутствовали роли отдела **{config['name']}**.")
            else:
                for t_name in titles:
                    t_obj = disnake.utils.get(ctx.guild.roles, name=t_name)
                    if t_obj and t_obj in member.roles:
                        await take_role(member, t_obj)
                        removed_roles_list.append(t_obj.name)

                if removed_roles_list:
                    roles_text = ", ".join(f"**{r}**" for r in removed_roles_list)
                    await ctx.send(f"Пользователь {member.mention} покидает отдел: {roles_text}, не прощаемся!")
                else:
                    await ctx.send(f"У пользователя {member.mention} не найдено ролей в отделе **{config['name']}**.")

        except disnake.Forbidden:
            await ctx.send("У бота недостаточно прав для снятия ролей.")