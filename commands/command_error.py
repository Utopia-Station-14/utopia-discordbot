from init import bot
from disnake.ext import commands


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("Неизвестная команда!")

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("У вас отсутствуют права на использование команды.")

    if isinstance(error, commands.MissingAnyRole):
        return await ctx.send("Привет, вы кто?")

    await ctx.send(f"⚠️ Ошибка: {error}")