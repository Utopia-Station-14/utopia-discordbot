import disnake
from disnake.ext import commands
from init import bot
from permissions import check_permissions

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