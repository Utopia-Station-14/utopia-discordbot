from init import bot
import importlib
import pkgutil
import config
from database import init_db


def load_modules(folder: str):
    package = importlib.import_module(folder)

    for _, mod_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{folder}.{mod_name}")


load_modules("commands")
load_modules("helpers")


@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

    channel = await bot.fetch_channel(1472600615606550568)

    await channel.send("Бот запущен!")


@bot.event
async def setup_hook():
    await init_db()


bot.run(config.DISCORD_KEY)