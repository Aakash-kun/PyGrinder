async def heartbeat(instance):
    await instance.ws.send(
        {
            "op":1,
            "d": {
                "token": instance.token,
                "intents": 4609,
                "properties": {
                    "$os":"windows",
                    "$browser":"Discord",
                    "$device": "desktop"
                }
            }
        }
    )
