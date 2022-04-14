import json
import time
import aiohttp
import asyncio


async def heartbeat(ws, token, heartbeat_interval):
    await ws.send_json(json.dumps({"op": 1, "d": None}))

def beatheart(ws, token, heartbeat_interval):
    while True:
        time.sleep(heartbeat_interval/1000)
        asyncio.run(heartbeat(ws, token, heartbeat_interval))

async def connect(token):
    ws = await aiohttp.ClientSession().ws_connect(url="wss://gateway.discord.gg/?v=9&encoding=json")
    print("yes")
    RECV = (await ws.receive()).json()
    print(RECV) 
    print("also yes")
    await ws.send_json(
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

    # await ws.send_json(json.dumps({"op":2,"d": {"token":token, "intents": 1, "properties": {"$os":"linux","$browser":"nextcord==2.0.0a8","$device": "nextcord==2.0.0a8" }}}))
    print("maybe yes")

    heartbeat_interval = RECV['d']['heartbeat_interval']
    re = (await ws.receive())
    print("probably yes")
    print(re.data)

    # threading.Thread(target=beatheart, args=(ws, token, heartbeat_interval)).start()
    while True:
        try:
            msg = await ws.receive()
            if msg:
                print(msg.json())
        except KeyboardInterrupt:
            raise SystemExit
        except:
            pass

asyncio.run(connect(""))
