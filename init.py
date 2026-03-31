import discord
from discord.ext import commands

print(discord.__file__)
print(dir(discord))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="&",
    intents=intents,
    help_command=None
)