from init import bot
import disnake
from config import ADMIN
from database import (
    get_all,
    add_user,
    remove_user,
    change_value,
    get_value
)

CURRENCY_NAME = "Социальный Рейтинг"

ROLE_RULES = {
    "Глава Спрайтинга": "Спрайтер",
}


def has_permission(ctx):
    return ADMIN in [r.name for r in ctx.author.roles]


def has_spriter_access(ctx):
    return any(r.name in ["Спрайтер", "Глава Спрайтинга"] for r in ctx.author.roles)


@bot.command(name="table")
async def table(ctx, action: str = None, member: disnake.Member = None):

    if action is None or action.lower() == "show":

        data = get_all()

        embed = disnake.Embed(title="📋 Таблица спрайтеров", color=0xFFC0CB)

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

    if action.lower() == "add":

        if not has_permission(ctx):
            return await ctx.send("Нет прав")

        if member is None:
            return await ctx.send("Укажи пользователя")

        add_user(str(member.id))
        return await ctx.send(f"Добавлен {member.mention}")

    if action.lower() == "remove":

        if not has_permission(ctx):
            return await ctx.send("Нет прав")

        if member is None:
            return await ctx.send("Укажи пользователя")

        remove_user(str(member.id))
        return await ctx.send(f"Удалён {member.mention}")

    return await ctx.send("add / remove / show")


@bot.command(name="rate")
async def rate(ctx, member: disnake.Member = None, value: str = None):

    if not has_permission(ctx):
        return await ctx.send("Нет прав")

    delta = int(value)

    change_value(str(member.id), delta)

    await ctx.send("Обновлено!")


BUY_CHANNEL_ID = 1457655329595854929

BUY_COSTS = {
    "1": 10,
    "2": 20,
    "3": 30
}


@bot.command(name="buy")
async def buy(ctx, level: str = None):

    if not has_spriter_access(ctx):
        return await ctx.send("Нет доступа")

    if level not in BUY_COSTS:
        return await ctx.send("1 / 2 / 3")

    cost = BUY_COSTS[level]
    uid = str(ctx.author.id)

    value = get_value(uid)

    if value < cost:
        return await ctx.send("Не хватает СР")

    change_value(uid, -cost)

    channel = bot.get_channel(BUY_CHANNEL_ID)

    if channel:
        await channel.send(
            f"{ctx.author.mention} купил уровень {level} за {cost} СР"
        )

    await ctx.send("Покупка успешна")