import os
import sys
import importlib
import pkgutil
import config
from init import bot

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def load_modules(folder: str):
    package = importlib.import_module(folder)
    for _, mod_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{folder}.{mod_name}")

load_modules("commands")


@bot.event
async def on_ready():
    print(f"Logged as {bot.user}")

    try:
        channel = await bot.fetch_channel(1472600615606550568)
        await channel.send("Бот запущен!")
    except Exception as e:
        print("[on_ready error]", e)


bot.run(config.DISCORD_KEY)