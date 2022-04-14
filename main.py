# what this file should actually do and stuff

# from functions.basic7functions import beg, crime, search, postmeme
# from functions.excess_tasks import timely, vote
from utils.Classes import Instance
from ws import heartbeat, create
import logging
import aiohttp
from scheduler.schedule import Q
from functions.excess_tasks.startup import startup
import asyncio
import os
import time

# Creating a Instance of Classes.Instance

config = {
    "token" :"token",
    "grind_channel_id": 1234,
    "master_id": "1234",
    "response_timeout": 10,
    "queue" : Q(),

    "_search_preference": [1, 2, 3],
    "_search_cancel": [1, 2, 3],
    "_search_timeout": 10,

    "_crime_preference": [1, 2, 3],
    "_crime_cancel": [1, 2, 3],
    "_crime_timeout": 10,
    }

config["name"], config["id"], config["coins"], config["items"] = asyncio.run(startup(config["token"]))


async def sessions():
    session = None
    voting_session = None
    async with aiohttp.ClientSession() as session:
        session = session
    async with aiohttp.ClientSession() as voting_session:
        voting_session = voting_session
    return session, voting_session

class MySessions():
    pass

my_sessions = MySessions()
async def sessions():
    my_sessions.session = aiohttp.ClientSession()
    my_sessions.voting_session = aiohttp.ClientSession()

loop = asyncio.new_event_loop()
loop.create_task(sessions())
loop.run_until_complete()

# config["session"] = aiohttp.ClientSession()
# config["voting_session"] = aiohttp.ClientSession()

ws, heartbeat_interval = asyncio.run(create.create(config["token"], my_sessions.session))

config["ws"] = ws
config["heartbeat_interval"] = heartbeat_interval

if not os.path.exists(os.getcwd()+f"/logs/{config['id']}.log"):
    open(f"logs/{config['id']}.log", "a")

logging.basicConfig(
    filename=f"logs\{config['id']}.log",
    format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(status_code)s | %(username)-10s | %(message)s",
    datefmt="%I:%M:%S %p %d/%m/%Y",
    level="INFO"
)
config["logger"] = logging.getLogger()
# # logger.debug("Debug message", extra={"token": "mytoken", "username": "myusername", "status_code": 200})


instance = Instance(config, sessions=my_sessions)
time.sleep(10)
instance["session"].close()
instance["voting_session"].close()