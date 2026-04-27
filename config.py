import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_KEY = os.getenv("DISCORD_KEY")
GLOBAL_MASSAGE_ON = False
ADMIN = "Руководство проекта"
BOT_VERSION = "betabuild V_0.99991"