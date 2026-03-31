from init import bot
from disnake.ext import commands


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("Я нихуя не поняла.")

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("ТЫ НЕ ПРОЙДЕЕЕЕШЬ.")

    if isinstance(error, commands.MissingAnyRole):
        return await ctx.send("Приятель, а не пошёл бы ты нахуй.")

    await ctx.send(f"⚠️ Ошибка: {error}")