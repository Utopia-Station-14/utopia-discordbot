import json
from init import bot
from config import TABLE_CHANNEL

MESSAGE_PREFIX = "```json"
MESSAGE_SUFFIX = "```"

_message_cache = None

async def _get_message():
    global _message_cache

    if _message_cache is not None:
        return _message_cache

    channel = bot.get_channel(TABLE_CHANNEL)
    if channel is None:
        channel = await bot.fetch_channel(TABLE_CHANNEL)

    async for message in channel.history(limit=100):
        if message.author.id != bot.user.id:
            continue
        _message_cache = message
        return message

    message = await channel.send("```json\n{}\n```")
    _message_cache = message
    return message


async def _read():
    message = await _get_message()

    content = message.content.strip()

    if content.startswith(MESSAGE_PREFIX):
        content = content[len(MESSAGE_PREFIX):]

    if content.endswith(MESSAGE_SUFFIX):
        content = content[:-len(MESSAGE_SUFFIX)]

    if not content.strip():
        return {}

    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        return {}


async def _write(data: dict):
    global _message_cache
    message = await _get_message()

    text = json.dumps(
        data,
        ensure_ascii=False,
        indent=4
    )

    updated_message = await message.edit(
        content=f"```json\n{text}\n```"
    )
    _message_cache = updated_message


async def get_all():
    return await _read()


async def add_user(user_id: str):
    data = await _read()
    if user_id not in data:
        data[user_id] = 0
        await _write(data)


async def remove_user(user_id: str):
    data = await _read()
    if user_id in data:
        del data[user_id]
        await _write(data)


async def change_value(user_id: str, delta: int):
    data = await _read()
    if user_id not in data:
        data[user_id] = 0

    data[user_id] += delta
    await _write(data)


async def get_value(user_id: str):
    data = await _read()
    return data.get(user_id, 0)