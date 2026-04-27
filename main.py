from init import bot
from database import load_data
import importlib
import pkgutil
import config

load_data()

def load_modules(folder: str):
    package = importlib.import_module(folder)

    for _, mod_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{folder}.{mod_name}")


load_modules("commands")
load_modules("helpers")


@bot.event
async def on_ready():
    print(f"Logged as {bot.user}")

    try:
        channel = await bot.fetch_channel(1472600615606550568)
        await channel.send("Бот запущен!")
    except Exception as e:
        print("[on_ready error]", e)


bot.run(config.DISCORD_KEY)