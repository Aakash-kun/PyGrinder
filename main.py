from functions.basic7functions import beg, crime, search, postmeme
# from functions.excess_tasks import timely, vote
from utils import Instance
from ws import heartbeat, create
import logging
from scheduler.schedule import Q
from functions.excess_tasks.startup import startup
import asyncio
import os


# Creating a Instance of Classes.Instance
config = {
    "token": "token",
    "grind_channel_id": 1234,
    "master_id": 1234,
    "response_timeout": 10,
    "queue" : Q(),

    "_beg_interval": 10,

    "_search_preference": [1, 2, 3],
    "_search_cancel": [1, 2, 3],
    "_search_timeout": 10,

    "_crime_preference": [1, 2, 3],
    "_crime_cancel": [1, 2, 3],
    "_crime_timeout": 10,

    }

loop = asyncio.get_event_loop()
# config["name"], config["id"], config["coins"], config["items"] = loop.run_until_complete(startup(config["token"]))
config["name"], config["id"], config["coins"], config["items"] = "name", "1", 1, {"h": 5}

instance = Instance.Instance(config)
ws, heartbeat_interval = loop.run_until_complete(create.create(config["token"], instance.session))

config["ws"] = ws
config["heartbeat_interval"] = heartbeat_interval
instance.ws = ws
instance.heartbeat_interval = heartbeat_interval

if not os.path.exists(os.getcwd()+f"/logs/{config['id']}.log"):
    open(f"logs/{config['id']}.log", "a")

logging.basicConfig(
    filename=f"logs\{config['id']}.log",
    format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(status_code)s | %(username)-10s | %(message)s",
    datefmt="%I:%M:%S %p %d/%m/%Y",
    level="INFO"
)
config["logger"] = logging.getLogger()
instance.logger = config["logger"]
# # logger.debug("Debug message", extra={"token": "mytoken", "username": "myusername", "status_code": 200})

logging.basicConfig(
    filename=f"tracebacks\{config['id']}.log",
    format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(traceback_id)s | %(username)-10s \n\n %(message)s\n=========================\n\n",
    datefmt="%I:%M:%S %p %d/%m/%Y",
    level="INFO"
)
config["traceback_logger"] = logging.getLogger()
instance.traceback_logger = config["traceback_logger"]
# # logger.debug("Debug message", extra={"token": "mytoken", "username": "myusername", "status_code": 200})

def queue_beg():
    instance.queue.put(1, beg.beg, instance)

def queue_heartbeat():
    instance.queue.put(0, heartbeat.heartbeat, instance)
instance.scheduler.add_job(queue_beg, "interval", instance._beg_interval)
instance.scheduler.add_job(queue_heartbeat, "interval", instance.heartbeat_interval)
instance.scheduler.start()

while True:
    instance.queue.get()()
