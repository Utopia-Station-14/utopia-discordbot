import asyncpg
import os

DB_URL = os.getenv("DATABASE_URL")

pool = None


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DB_URL)

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS spriters (
            user_id TEXT PRIMARY KEY,
            value INT DEFAULT 0
        )
        """)


async def get_all():
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT user_id, value FROM spriters")
        return {r["user_id"]: r["value"] for r in rows}


async def add_user(user_id):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO spriters (user_id, value)
        VALUES ($1, 0)
        ON CONFLICT (user_id) DO NOTHING
        """, user_id)


async def change_value(user_id, delta):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO spriters (user_id, value)
        VALUES ($1, $2)
        ON CONFLICT (user_id)
        DO UPDATE SET value = spriters.value + $2
        """, user_id, delta)


async def get_value(user_id):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT value FROM spriters WHERE user_id = $1",
            user_id
        )
        return row["value"] if row else 0