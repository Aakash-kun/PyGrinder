import asyncio
import aiohttp

class MyClass:
    pass

myc = MyClass()

async def start():
    myc.session = aiohttp.ClientSession()
    myc.voting_session = aiohttp.ClientSession()

asyncio.get_event_loop().run_until_complete(asyncio.create_task(start()))

print(myc.session)

async def send():
    x = await myc.session.get("https://google.com")
    return x.status_code

asyncio.run(send())