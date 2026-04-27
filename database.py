import asyncpg
import os

pool = None


async def init_db():
    global pool

    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise Exception("DATABASE_URL не найден в environment!")

    pool = await asyncpg.create_pool(db_url)

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS spriters (
            user_id TEXT PRIMARY KEY,
            value INT DEFAULT 0
        )
        """)


def get_pool():
    if pool is None:
        raise Exception("DB pool не инициализирован (init_db не вызван)")
    return pool


async def get_all():
    p = get_pool()
    async with p.acquire() as conn:
        rows = await conn.fetch("SELECT user_id, value FROM spriters")
        return {r["user_id"]: r["value"] for r in rows}


async def add_user(user_id: str):
    p = get_pool()
    async with p.acquire() as conn:
        await conn.execute("""
        INSERT INTO spriters (user_id, value)
        VALUES ($1, 0)
        ON CONFLICT (user_id) DO NOTHING
        """, user_id)


async def remove_user(user_id: str):
    p = get_pool()
    async with p.acquire() as conn:
        await conn.execute("""
        DELETE FROM spriters WHERE user_id = $1
        """, user_id)


async def change_value(user_id: str, delta: int):
    p = get_pool()
    async with p.acquire() as conn:
        await conn.execute("""
        INSERT INTO spriters (user_id, value)
        VALUES ($1, $2)
        ON CONFLICT (user_id)
        DO UPDATE SET value = spriters.value + $2
        """, user_id, delta)


async def get_value(user_id: str):
    p = get_pool()
    async with p.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT value FROM spriters WHERE user_id = $1",
            user_id
        )
        return row["value"] if row else 0