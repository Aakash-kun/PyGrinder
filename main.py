# what this file should actually do and stuff

from functions.basic7functions import beg, crime, search, postmeme
# from functions.excess_tasks import timely, vote
from utils.Classes import Instance, create_session
from ws import heartbeat, create
import logging
import aiohttp
from scheduler.schedule import Q
from functions.excess_tasks.startup import startup
import asyncio
import os
import time
print("h1")
# Creating a Instance of Classes.Instance

config = {
    "token": "token",
    "grind_channel_id": 1234,
    "master_id": 1234,
    "response_timeout": 10,
    "queue" : Q(),

    "_search_preference": [1, 2, 3],
    "_search_cancel": [1, 2, 3],
    "_search_timeout": 10,

    "_crime_preference": [1, 2, 3],
    "_crime_cancel": [1, 2, 3],
    "_crime_timeout": 10,
    }
print("h2")

loop = asyncio.get_event_loop()
# config["name"], config["id"], config["coins"], config["items"] = loop.run_until_complete(startup(config["token"]))
config["name"], config["id"], config["coins"], config["items"] = "name", "1", 1, {"h": 5}

ws, heartbeat_interval = loop.run_until_complete(create.create(config["token"], 
                                                               loop.run_until_complete(create_session())))
print("h3")

config["ws"] = ws
config["heartbeat_interval"] = heartbeat_interval

if not os.path.exists(os.getcwd()+f"/logs/{config['id']}.log"):
    open(f"logs/{config['id']}.log", "a")
print("h4")

logging.basicConfig(
    filename=f"logs\{config['id']}.log",
    format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(status_code)s | %(username)-10s | %(message)s",
    datefmt="%I:%M:%S %p %d/%m/%Y",
    level="INFO"
)
config["logger"] = logging.getLogger()
# # logger.debug("Debug message", extra={"token": "mytoken", "username": "myusername", "status_code": 200})
print("h5")

logging.basicConfig(
    filename=f"tracebacks\{config['id']}.log",
    format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(traceback_id)s | %(username)-10s \n %(message)s \n =========================",
    datefmt="%I:%M:%S %p %d/%m/%Y",
    level="INFO"
)
config["traceback_logger"] = logging.getLogger()
# # logger.debug("Debug message", extra={"token": "mytoken", "username": "myusername", "status_code": 200})
print("h6")


instance = Instance(config)
print("h7")
time.sleep(10)
instance.close_sessions()
print("h8")
