import aiosqlite
import asyncio
import json

async def make():
    db = await aiosqlite.connect("db.sqlite3")
    await db.execute("CREATE TABLE IF NOT EXISTS data (user_id bigint UNIQUE PRIMARY KEY, coins int, items text)")
    await db.commit()
    await db.close()

async def put():
    db = await aiosqlite.connect("db.sqlite3")
    await db.execute("INSERT OR REPLACE INTO data (user_id, coins, items) VALUES(?, ?, ?)", (1, 100, json.dumps({"item1": 1, "item2": 2}), ))
    await db.commit()
    await db.close()

async def get():
    db = await aiosqlite.connect("db.sqlite3")
    data = await db.execute("SELECT coins, items FROM data WHERE user_id = ?", (1, ))
    data = await data.fetchone()
    print(data)
    await db.close()


asyncio.run(make())

