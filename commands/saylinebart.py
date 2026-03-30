import re
from init import bot
from helpers.permissions import roles_required

@bot.command(name="print")
@roles_required("Свидетель")
async def print_command(ctx, *, text: str = None):

    if not text or text.strip() == "":
        await ctx.send("no_message")
        return

    if re.search(r"@(\w+)", text):
        await ctx.send("no")
        return

    await ctx.send(text)