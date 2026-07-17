from functools import wraps
import disnake
from disnake.ext import commands
from config import ADMIN
from init import bot

# Выдача ролей осуществляется с помощью условной иерархии.
# Глава отдела может выдавать только роли своего отдела.
# Иерархия в структуре ниже.
ROLE_RULES = {
    "Глава Спрайтинга": "Спрайтер",
    "Глава Маппинга": "Маппер"
}

# Функция для проверки возможности выполнить команду.
def check_permissions(ctx, role_name: str) -> bool:
    author_roles = [role.name for role in ctx.author.roles]

    # Если у вас есть определенная роль, то вы можете выполнять команду без лишних проверок.
    if ADMIN in author_roles:
        return True

    # Тут, соответственно, проверка на иерархию.
    return any(
        author_role in ROLE_RULES and ROLE_RULES[author_role] == role_name
        for author_role in author_roles
    )

# Функция для проверки указанной роли у юзера.
def check_roles(ctx, allowed_roles: list[str]) -> bool:
    user_roles = {role.name.strip().lower() for role in ctx.author.roles}
    allowed_roles = {role.strip().lower() for role in allowed_roles}
    return bool(user_roles & allowed_roles)


def roles_required(*roles):
    required_roles = {r.strip().lower() for r in roles}

    def wrapper(func):
        @wraps(func)
        async def inner(ctx, *args, **kwargs):
            user_roles = {r.name.strip().lower() for r in ctx.author.roles}

            if not (user_roles & required_roles):
                await ctx.send("Недостаточно прав!")
                return

            return await func(ctx, *args, **kwargs)

        return inner

    return wrapper