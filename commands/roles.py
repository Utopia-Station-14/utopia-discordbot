from init import bot
import disnake

ROLE_RULES = {
    "Глава Спрайтинга": "Спрайтер",
    "Глава Маппинга": "Маппер"
}

@bot.command(name="role")
async def role_command(ctx, action: str = None, member: disnake.Member = None, *, role_name: str = None):
    action = action.lower()
    author_roles = [role.name for role in ctx.author.roles]

    allowed = any(
        author_role in ROLE_RULES and ROLE_RULES[author_role] == role_name
        for author_role in author_roles
    )

    if not allowed:
        await ctx.send("У вас недостаточно прав!")
        return

    role = disnake.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send("Роль не найдена.")
        return

    if action == "add":
        if role in member.roles:
            await ctx.send("У пользователя уже есть данная роль.")
            return

        await member.add_roles(role)
        await ctx.send("Роль успешно выдана!")

    if action == "remove":
        if role not in member.roles:
            await ctx.send("У пользователя отсутсвует данная роль.")
            return

        await member.remove_roles(role)
        await ctx.send("Роль успешно снята!")