import aiohttp
import json


async def create(token, session):
    ws = await session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
    RECV = (await ws.receive()).json()
    heartbeat_interval = RECV['d']['heartbeat_interval']
    await ws.send_json(
        json.dumps(
            {
                "op":2,
                "d": {
                    "token": token,
                    "intents": 4609,
                    "properties": {
                        "$os":"windows",
                        "$browser":"Discord",
                        "$device": "desktop"
                    }
                }
            }
        )
    )

    return ws, heartbeat_interval