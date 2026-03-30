from init import bot
import importlib
import pkgutil
from config import DISCORD_KEY
from discord.ext import commands as discord_commands

def load_modules(folder: str):
    package = importlib.import_module(folder)

    for _, mod_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{folder}.{mod_name}")


load_modules("commands")
load_modules("helpers")

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, discord_commands.CommandNotFound):
        return await ctx.send("Я нихуя не поняла.")

    if isinstance(error, discord_commands.MissingPermissions):
        return await ctx.send("ТЫ НЕ ПРОЙДЕЕЕЕШЬ.")

    if isinstance(error, discord_commands.MissingAnyRole):
        return await ctx.send("Приятель, а не пошёл бы ты нахуй.")

    await ctx.send(f"⚠️ Ошибка: {error}")

bot.run(DISCORD_KEY)