import json

async def startup(instance):
    coins_cur= await instance.db.execute("SELECT coins FROM data WHERE ID = ?", (instance.id,))
    coins = await coins_cur.fetchone()
    coins = coins[0]

    items_cur= await instance.db.execute("SELECT items FROM data WHERE ID = ?", (instance.id,))
    items = await items_cur.fetchone()
    items = json.loads(items[0])

    response = await instance.session.get("https://discordapp.com/api/v10/users/@me", headers=instance.utils.get_headers(instance))
    print(await response.text())
    # return instance.name, instance.id, coins, items
    