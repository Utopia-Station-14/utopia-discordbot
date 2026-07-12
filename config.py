import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_KEY = os.getenv("DISCORD_KEY")
GLOBAL_MASSAGE_ON = False
ADMIN = "Руководство проекта"
BOT_VERSION = "betabuild V_0.99991"
BOT_CHANNEL = 1472600615606550568
TABLE_CHANNEL = 1524057869274845215