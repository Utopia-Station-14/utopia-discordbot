import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS spriters (
        user_id TEXT PRIMARY KEY,
        value INTEGER NOT NULL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def get_all():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT user_id, value FROM spriters")
    data = dict(cur.fetchall())

    conn.close()
    return data


def add_user(user_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO spriters (user_id, value)
    VALUES (?, 0)
    """, (user_id,))

    conn.commit()
    conn.close()


def remove_user(user_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM spriters WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()


def change_value(user_id: str, delta: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO spriters (user_id, value)
    VALUES (?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET value = value + ?
    """, (user_id, delta, delta))

    conn.commit()
    conn.close()


def get_value(user_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT value FROM spriters WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    conn.close()
    return row[0] if row else 0