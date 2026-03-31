from init import bot
from disnake import Embed


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
            ),
            "inline": False
        },
    ]
}


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

    embed.set_footer(text="Версия: betabuild V_0.9999")

    await ctx.send(embed=embed)