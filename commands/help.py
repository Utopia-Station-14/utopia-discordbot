from init import bot
from disnake import Embed

#region Embed_Help
embed_help = {
    "title": "Панель пользователя",
    "color": 0x00FF99,   
    "fields": [
        {
            "name": "Команды:",
            "value": (
                "&help - Проводник по возможностям бота.\n"
                "&print - Вывод указанного текста.\n"
                "&p - Вывод числа π.\n"
                "&fact - Вывод факториала указанного числа.\n"
                "&admin_help - Проводник по командам администратора. \n"
            ),
            "inline": False
        },
    ]
}

#region Embed_A_Help
embed_a_help = {
    "title": "Панель Администратора",
    "color": 0x00683E,
    "fields": [
        {
            "name": "Команды:",
            "value": (
                "&roles <add>/<remove> @username - Выдача/Снятие указанной роли у пользователя.\n"
            ),
            "inline": False
        },
    ]
}

#region Help
@bot.command(name="help")
async def help_command(ctx):

    embed = Embed(
        title=embed_help["title"],
        color=embed_help["color"]
    )

    for field in embed_help["fields"]:
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field["inline"]
        )

    if bot.user and bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)

    embed.set_footer(text="Версия: betabuild V_0.99991")

    await ctx.send(embed=embed)

#region AHELP
@bot.command(name="admin_help")
async def help_command(ctx):

    embed = Embed(
        title=embed_a_help["title"],
        color=embed_a_help["color"]
    )

    for field in embed_a_help["fields"]:
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field["inline"]
        )

    if bot.user and bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)

    embed.set_footer(text="Версия: betabuild V_0.99991")

    await ctx.send(embed=embed)