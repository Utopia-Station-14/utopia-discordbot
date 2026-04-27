from disnake.ext.commands import Bot
from disnake import Intents

intent = Intents.default()
intent.message_content = True
intent.members = True

bot = Bot(
    command_prefix="&",
    help_command=None,
    intents=intent
)