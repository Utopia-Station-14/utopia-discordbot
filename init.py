from disnake import Intents
from disnake.ext.commands import Bot

intent = Intents.default()
intent.message_content = True
intent.members = True
intent.guilds = True
intent.guild_messages = True
intent.guild_reactions = True

bot = Bot(
    command_prefix="&",
    help_command=None,
    intents=intent
)