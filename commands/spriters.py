import disnake
from disnake.ext import commands

from database import (
    get_all,
    add_user,
    remove_user,
    change_value,
    get_value
)
from init import bot
from permissions import check_permissions

CURRENCY_NAME = "Социальный Рейтинг"


# Функция для работы с таблицей спрайтеров.
# Содержит 3 действия.
# show - выводит содержание таблицы. add/remove - добавление/удаление юзера из таблицы.
@bot.command(name="table")
async def table(ctx, action: str = "show", member: disnake.Member = None):
    action = action.lower()

    # Вывод таблицы.
    if action == "show":
        data = await get_all()

        embed = disnake.Embed(
            title="📋 Таблица участников",
            color=0xFFC0CB
        )

        # Если таблица пустая - выводится следуйщее.
        if not data:
            embed.description = "*Таблица пока пуста*"
            return await ctx.send(embed=embed)

        # В ином случае, информация выводится с json файла внутри Дискорд сервера.
        # Для подробностей смотрите database.py .
        lines = []
        for i, (uid, value) in enumerate(data.items(), start=1):
            user = ctx.guild.get_member(int(uid))
            if not user:
                try:
                    user = await ctx.guild.fetch_member(int(uid))
                except disnake.NotFound:
                    user = None

            mention = user.mention if user else f"<@{uid}>"
            lines.append(f"{i}. {mention} | **{value}** {CURRENCY_NAME}")

        embed.add_field(name="Список участников:", value="\n".join(lines), inline=False)
        return await ctx.send(embed=embed)

    # Добавление и удаление юзера в таблицу/е.
    if action in ["add", "remove"]:
        # Проверка на главу отдела.
        has_access = any(check_permissions(ctx, r) for r in ["Спрайтер"])
        
        # Ловим возможные ошибки-start.
        if not has_access:
            return await ctx.send("❌ У вас недостаточно прав для редактирования таблицы.")

        if member is None:
            return await ctx.send("❌ Пожалуйста, укажите пользователя через упоминание.")
        # Ловим возможные ошибки-end.

        # Воиспроизводим указанные действия-start.
        if action == "add":
            await add_user(str(member.id))
            return await ctx.send(f"✅ Пользователь успешно добавлен в таблицу.")

        elif action == "remove":
            await remove_user(str(member.id))
            return await ctx.send(f"🗑️ Пользователь успешно удален из таблицы.")
        # Воиспроизводим указанные действия-end.

    return await ctx.send("❓ Некорректное использование. Доступные команды: `&table show` or `&table add/remove @юзер`")


# Функция для изменения значений валюты.
@bot.command(name="rate")
async def rate(ctx, member: disnake.Member = None, value: str = None):
    # Проверка на главу отдела.
    has_any_lead_rights = any(check_permissions(ctx, r) for r in ["Спрайтер"])
    if not has_any_lead_rights:
        return await ctx.send("❌ У вас нет прав на использование этой команды.")

    # Подсказка.
    if member is None or value is None:
        return await ctx.send("ℹ️ Использование: `&rate @user +10` или `&rate @user -5`")

    has_manage_rights = False
    for role in member.roles:
        if check_permissions(ctx, role.name):
            has_manage_rights = True
            break

    if not has_manage_rights:
        return await ctx.send("❌ Вы не можете изменять рейтинг этому пользователю.")

    try:
        delta = int(value)
    except ValueError:
        return await ctx.send("❌ Значение изменения должно быть целым числом.")

    await change_value(str(member.id), delta)
    
    sign = "+" if delta > 0 else ""
    await ctx.send(f"📈 {CURRENCY_NAME} пользователя изменен на **{sign}{delta}**!")