import re
from init import bot


@bot.command(name="print")
async def print_command(ctx, *, text: str = None):

    if not text or text.strip() == "":
        await ctx.send("no_message")
        return

    if re.search(r"@(\w+)", text): # проверка на дауна.
        await ctx.send("no")
        return

    await ctx.send(text)