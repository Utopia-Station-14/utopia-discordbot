import json
import asyncio
import os
import atexit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "spriters.json")

print("[DB] file:", DATA_FILE)

_data: dict[str, int] = {}
_dirty = False
_save_task: asyncio.Task | None = None


def load_data():
    global _data

    print("[DB] loading...")

    if not os.path.exists(DATA_FILE):
        print("[DB] file not found, creating new")
        _data = {}
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                print("[DB] empty file, reset")
                _data = {}
                return

            _data = json.loads(content)

        print("[DB] loaded:", _data)

    except Exception as e:
        print("[DB] load error:", e)
        _data = {}


def save_data():
    global _dirty

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(_data, f, ensure_ascii=False, indent=2)

        _dirty = False
        print("[DB] saved:", _data)

    except Exception as e:
        print("[DB] save error:", e)


def _force_save():
    if _dirty:
        print("[DB] force save on exit")
        save_data()


atexit.register(_force_save)


def schedule_save():
    global _save_task, _dirty

    _dirty = True

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return

    if _save_task and not _save_task.done():
        _save_task.cancel()

    _save_task = loop.create_task(_delayed_save())


async def _delayed_save():
    try:
        await asyncio.sleep(60)

        if _dirty:
            save_data()

    except asyncio.CancelledError:
        pass


async def get_all():
    return _data


async def add_user(user_id: str):
    if user_id not in _data:
        _data[user_id] = 0
        schedule_save()


async def remove_user(user_id: str):
    if user_id in _data:
        del _data[user_id]
        schedule_save()


async def change_value(user_id: str, delta: int):
    _data[user_id] = _data.get(user_id, 0) + delta
    schedule_save()


async def get_value(user_id: str):
    return _data.get(user_id, 0)