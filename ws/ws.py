async def create(token, session):
    ws = await session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
    RECV = (await ws.receive()).json()
    heartbeat_interval = RECV['d']['heartbeat_interval']
    await ws.send_json(
        {
            "op":2,
            "d": {
                "token": token,
                "intents": 37377,
                "properties": {
                    "$os":"windows",
                    "$browser":"Discord",
                    "$device": "desktop"
                }
            }
        }
    )

    return ws, heartbeat_interval

async def heartbeat(instance):
    await instance.ws.send(
        {
            "op":1,
            "d": {
                "token": instance.token,
                "intents": 37377,
                "properties": {
                    "$os":"windows",
                    "$browser":"Discord",
                    "$device": "desktop"
                }
            }
        }
    )
