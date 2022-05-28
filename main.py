from functions.basic7functions import beg, crime, search, postmeme
# from functions.excess_tasks import timely, vote
from utils import Instance
from ws import ws
from scheduler.schedule import Q
from functions.excess_tasks.startup import startup
import asyncio
import os
import Exceptions


def BuildInstance(config):

    instance = Instance.Instance(config)
    loop = asyncio.get_event_loop()
    startup_resp = loop.run_until_complete(startup(instance))

    if startup_resp[0] == 999:
        raise Exceptions.BadToken

    config["name"], config["id"], config["coins"], config["items"] = startup_resp

    instance_ws, heartbeat_interval = loop.run_until_complete(
        ws.create(config["token"], instance.session))

    config["ws"] = instance_ws
    config["heartbeat_interval"] = heartbeat_interval

    instance.update(config)

    if not os.path.exists(os.getcwd()+f"/logs/{config['id']}.log"):
        open(f"logs/{config['id']}.log", "a")
    instance.create_loggers()

    return instance


instance = BuildInstance(
    config={
        "token": "OTU1ODc2ODkxNDUyMTI1MjA0.YmKgAQ.VOeJtAG3bMKAB2rLDuIblK0tpnk",
        "grind_channel_id": 1234,
        "master_id": 1234,
        "response_timeout": 10,
        "queue": Q(),

        "logging_level": "DEBUG",
        "db_push_interval": 10,

        "_beg_interval": 10,

        "_search_preference": [1, 2, 3],
        "_search_cancel": [1, 2, 3],
        "_search_timeout": 10,

        "_crime_preference": [1, 2, 3],
        "_crime_cancel": [1, 2, 3],
        "_crime_timeout": 10,
    }
)


def queue_beg():
    instance.logger.debug("Queued a beg function", extra={
        "token": instance.token, "username": instance.name, "status_code": 100})
    instance.queue.put(1, beg.beg_function, instance)


def queue_heartbeat():
    instance.queue.put(0, ws.heartbeat, instance)


def queue_db_push():
    instance.queue.put(0, instance.db_push)


instance.scheduler.add_job(
    queue_beg, "interval", seconds=instance._beg_interval)
instance.scheduler.add_job(
    queue_heartbeat, "interval", seconds=instance.heartbeat_interval)
instance.scheduler.add_job(
    queue_db_push, "interval", seconds=instance.db_push_interval)
instance.scheduler.start()

while True:
    asyncio.get_event_loop().run_forever()
    print("ran it hehe")
