import json

async def startup(instance):
    coins, items = await instance.get_items_coins()

    response = await instance.session.get("https://discordapp.com/api/v9/users/@me", headers=instance.utils.get_headers(instance))
    if response.status != 200:
        return (999, response.status)

    response = await response.json()    
    return response["username"], response["id"], coins, items
