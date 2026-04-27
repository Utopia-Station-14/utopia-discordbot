from init import bot
import disnake
import json
import os
from config import ADMIN

FILE_PATH = "spriter_table.json"
CURRENCY_NAME = "Социальный Рейтинг"
ROLE_RULES = {
    "Глава Спрайтинга": "Спрайтер",
}

def has_permission(ctx) -> bool:
    author_roles = [role.name for role in ctx.author.roles]

    if ADMIN in author_roles:
        return True

    return any(role in ROLE_RULES for role in author_roles)


def is_spriter(ctx) -> bool:
    return any(role.name == "Спрайтер" for role in ctx.author.roles)


def load_table():
    if not os.path.exists(FILE_PATH):
        return {}

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def save_table():
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(spriter_table, f, ensure_ascii=False, indent=4)


spriter_table = load_table()


@bot.command(name="table")
async def table(ctx, action: str = None, member: disnake.Member = None):

    if action is None or action.lower() == "show":

        embed = disnake.Embed(
            title="📋 Таблица спрайтеров",
            color=0xFFC0CB
        )

        if not spriter_table:
            embed.description = "Таблица пустая"
            return await ctx.send(embed=embed)

        text = ""

        for i, (user_id, value) in enumerate(spriter_table.items(), start=1):
            member_obj = ctx.guild.get_member(int(user_id))

            if member_obj:
                text += f"{i}. {member_obj.mention} | {value} {CURRENCY_NAME}\n"
            else:
                text += f"{i}. `Пользователь не найден` | {value} {CURRENCY_NAME}\n"

        embed.add_field(name="Список:", value=text, inline=False)

        if bot.user and bot.user.avatar:
            embed.set_thumbnail(url=bot.user.avatar.url)

        return await ctx.send(embed=embed)

    if action.lower() == "add":

        if not has_permission(ctx):
            return await ctx.send("У вас недостаточно прав!")

        if member is None:
            return await ctx.send("Используйте: `&table add @user`")

        key = str(member.id)

        if key in spriter_table:
            return await ctx.send("Пользователь уже в таблице.")

        spriter_table[key] = 0
        save_table()

        return await ctx.send(f"Добавлен: {member.mention}")

    if action.lower() == "remove":

        if not has_permission(ctx):
            return await ctx.send("У вас недостаточно прав!")

        if member is None:
            return await ctx.send("Используйте: `&table remove @user`")

        key = str(member.id)

        if key not in spriter_table:
            return await ctx.send("Пользователя нет в таблице.")

        del spriter_table[key]
        save_table()

        return await ctx.send(f"Удалён: {member.mention}")

    return await ctx.send("Неизвестное действие: add / remove / show")

@bot.command(name="rate")
async def rate(ctx, member: disnake.Member = None, value: str = None):

    if not has_permission(ctx):
        return await ctx.send("У вас недостаточно прав!")

    if member is None:
        return await ctx.send("Укажите пользователя!")

    try:
        delta = int(value)
    except:
        return await ctx.send("Введите ЦЕЛОЕ число (+/-)")

    key = str(member.id)

    if key not in spriter_table:
        spriter_table[key] = 0

    spriter_table[key] += delta
    save_table()

    await ctx.send("Социальный Рейтинг успешно обновлен!")

BUY_CHANNEL_ID = 1457655329595854929

BUY_COSTS = {
    "1": 10,
    "2": 20,
    "3": 30
}


def has_spriter_access(ctx) -> bool:
    return any(role.name in ["Спрайтер", "Глава Спрайтинга"] for role in ctx.author.roles)


@bot.command(name="buy")
async def buy(ctx, level: str = None):

    if not has_spriter_access(ctx):
        return await ctx.send("У вас нет доступа к покупке!")

    if level not in BUY_COSTS:
        return await ctx.send("Используй: &buy 1 / 2 / 3")

    cost = BUY_COSTS[level]
    user_id = str(ctx.author.id)

    if user_id not in spriter_table:
        return await ctx.send("Ты не в таблице спрайтеров!")

    if spriter_table[user_id] < cost:
        return await ctx.send("Недостаточно Социального Рейтинга!")

    spriter_table[user_id] -= cost
    save_table()

    channel = bot.get_channel(BUY_CHANNEL_ID)

    if channel:
        await channel.send(
            f"<@&{next(role.id for role in ctx.guild.roles if role.name == 'Глава Спрайтинга')}> "
            f"Пользователь {ctx.author.mention} купил уровень {level} за {cost} СР.\n"
            f"Остаток: {spriter_table[user_id]} {CURRENCY_NAME}"
        )

    await ctx.send(
        f"Покупка успешна! -{cost} СР\n"
        f"Осталось: {spriter_table[user_id]} {CURRENCY_NAME}"
    )