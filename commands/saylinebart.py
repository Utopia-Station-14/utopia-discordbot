import re
from init import bot
from helpers.permissions import roles_required
import math

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

@bot.command(name="p")
async def pi(ctx):
    await ctx.send(f"π ≈ {math.pi}")

@bot.command(name="fact")
async def factorial(ctx, number: int = None):

    if number is None:
        await ctx.send("Число мне скажи.")
        return

    if number < 0:
        await ctx.send("Чёта мала.")
        return

    if number > 100:
        await ctx.send("Убейся.")
        return

    result = math.factorial(number)
    await ctx.send(f"{number}! = {result}")