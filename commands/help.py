from init import bot
from disnake import Embed
from config import BOT_VERSION

HELP_DATA = {
    "user": {
        "title": "Панель пользователя",
        "color": 0x00FF99,
        "fields": [
            {
                "name": "Команды:",
                "value": (
                    "&help - Проводник по возможностям бота.\n"
                    "&print - Вывод текста.\n"
                    "&p - Число π.\n"
                    "&fact - Факториал числа.\n"
                    "&admin_help - Проводник по админ-командам.\n"
                    "&spriter_help - Проводник по спрайтер-командам"
                ),
                "inline": False
            }
        ]
    },

    "admin": {
        "title": "Панель Администратора",
        "color": 0x00683E,
        "fields": [
            {
                "name": "Команды:",
                "value": "&role <add/remove> @user Роль - управление ролями",
                "inline": False
            }
        ]
    },

    "spriter": {
        "title": "Панель Спрайтера",
        "color": 0xFFC0CB,
        "fields": [
            {
                "name": "Команды:",
                "value": (
                    "&table add/remove - управление таблицей\n"
                    "&table show - вывод таблицы\n"
                    "&rate @user +/-int - изменение рейтинга"
                ),
                "inline": False
            }
        ]
    }
}

def build_help_embed(key: str) -> Embed:
    data = HELP_DATA[key]

    embed = Embed(
        title=data["title"],
        color=data["color"]
    )

    for field in data["fields"]:
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field["inline"]
        )

    if bot.user and bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)

    embed.set_footer(text=f"Версия: {BOT_VERSION}")

    return embed

@bot.command(name="help")
async def help_command(ctx):
    await ctx.send(embed=build_help_embed("user"))


@bot.command(name="admin_help")
async def admin_help(ctx):
    await ctx.send(embed=build_help_embed("admin"))


@bot.command(name="spriter_help")
async def spriter_help(ctx):
    await ctx.send(embed=build_help_embed("spriter"))