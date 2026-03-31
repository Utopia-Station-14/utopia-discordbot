from disnake.ext import commands
from functools import wraps


def check_roles(ctx, allowed_roles: list[str]) -> bool:
    user_roles = {role.name.strip().lower() for role in ctx.author.roles}
    allowed_roles = {role.strip().lower() for role in allowed_roles}
    return bool(user_roles & allowed_roles)


def roles_required(*roles):
    roles = {r.lower() for r in roles}

    def wrapper(func):

        @wraps(func)
        async def inner(ctx, *args, **kwargs):
            user_roles = {r.name.lower() for r in ctx.author.roles}

            if not user_roles & roles:
                await ctx.send("нет прав")
                return

            return await func(ctx, *args, **kwargs)

        return inner

    return wrapper