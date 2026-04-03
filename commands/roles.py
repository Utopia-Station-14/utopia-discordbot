from init import bot
import disnake
from config import ADMIN

ROLE_RULES = {
    "Глава Спрайтинга": "Спрайтер",
    "Глава Маппинга": "Маппер"
}

def check_permissions(ctx, role_name: str) -> bool:
    author_roles = [role.name for role in ctx.author.roles]

    if ADMIN in author_roles:
        return True

    return any(
        author_role in ROLE_RULES and ROLE_RULES[author_role] == role_name
        for author_role in author_roles
    )

async def give_role(member: disnake.Member, role: disnake.Role):
    await member.add_roles(role)


async def take_role(member: disnake.Member, role: disnake.Role):
    await member.remove_roles(role)


@bot.command(name="role")
async def role_command(ctx, action: str = None, member: disnake.Member = None, *, role_name: str = None):
    action = action.lower()

    role = disnake.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send("Роль не найдена.")
        return

    if not check_permissions(ctx, role_name):
        await ctx.send("У вас недостаточно прав!")
        return

    if action == "add":
        if role in member.roles:
            await ctx.send("У пользователя уже есть данная роль.")
            return

        await give_role(member, role)
        await ctx.send("Роль успешно выдана!")

    elif action == "remove":
        if role not in member.roles:
            await ctx.send("У пользователя отсутствует данная роль.")
            return

        await take_role(member, role)
        await ctx.send("Роль успешно снята!")