import asyncpg
import os

DB_URL = os.getenv("DATABASE_URL")

pool: asyncpg.Pool | None = None


async def init_db():
    global pool

    if not DB_URL:
        raise Exception("DATABASE_URL не задан")

    pool = await asyncpg.create_pool(DB_URL)

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS spriters (
            user_id TEXT PRIMARY KEY,
            value INT DEFAULT 0
        )
        """)


def ensure_pool():
    if pool is None:
        raise Exception("DB pool не инициализирован (init_db не вызван)")


async def get_all():
    ensure_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT user_id, value FROM spriters")
        return {r["user_id"]: r["value"] for r in rows}


async def add_user(user_id: str):
    ensure_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO spriters (user_id, value)
        VALUES ($1, 0)
        ON CONFLICT (user_id) DO NOTHING
        """, user_id)


async def remove_user(user_id: str):
    ensure_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
        DELETE FROM spriters WHERE user_id = $1
        """, user_id)


async def change_value(user_id: str, delta: int):
    ensure_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO spriters (user_id, value)
        VALUES ($1, $2)
        ON CONFLICT (user_id)
        DO UPDATE SET value = spriters.value + $2
        """, user_id, delta)


async def get_value(user_id: str):
    ensure_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT value FROM spriters WHERE user_id = $1",
            user_id
        )
        return row["value"] if row else 0