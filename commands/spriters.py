from init import bot
import disnake
from database import (
    get_all,
    add_user,
    remove_user,
    change_value,
)

CURRENCY_NAME = "Социальный Рейтинг"


def has_permission(ctx):
    return ctx.author.guild_permissions.administrator


@bot.command(name="table")
async def table(ctx, action: str = None, member: disnake.Member = None):

    action = (action or "show").lower()

    if action == "show":

        data = await get_all()

        embed = disnake.Embed(
            title="📋 Таблица спрайтеров",
            color=0xFFC0CB
        )

        if not data:
            embed.description = "Пусто"
            return await ctx.send(embed=embed)

        text = ""

        for i, (uid, value) in enumerate(data.items(), start=1):
            user = ctx.guild.get_member(int(uid))

            if user:
                text += f"{i}. {user.mention} | {value} {CURRENCY_NAME}\n"
            else:
                text += f"{i}. неизвестный | {value} {CURRENCY_NAME}\n"

        embed.add_field(name="Список:", value=text, inline=False)

        return await ctx.send(embed=embed)

    if action == "add":

        if member is None:
            return await ctx.send("Укажи пользователя")

        await add_user(str(member.id))
        return await ctx.send("Пользователь был добавлен в таблицу.")

    if action == "remove":

        if member is None:
            return await ctx.send("Укажи пользователя")

        await remove_user(str(member.id))
        return await ctx.send("Пользователь был удалён из таблицы.")

    return await ctx.send("Корректное использование: &table add/remove/show")


@bot.command(name="rate")
async def rate(ctx, member: disnake.Member = None, value: str = None):

    if member is None or value is None:
        return await ctx.send("Использование: &rate @user +10")

    try:
        delta = int(value)
    except ValueError:
        return await ctx.send("Значение должно быть целым числом.")

    await change_value(str(member.id), delta)

    await ctx.send("Социальный рейтинг успешно обновлён!")