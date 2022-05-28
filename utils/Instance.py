import asyncio
import logging
from typing import Literal, Tuple, Union
import aiohttp
import time
from scheduler import schedule
from utils import Classes, utils
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import aiosqlite
import json


class Instance:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.id: int = config.get("id", 0)
        self.name: str = config.get("name", "Default")
        self.token: str = config["token"]
        self.grind_channel_id: int = config["grind_channel_id"]
        self.master_id: int = config["master_id"]
        self.response_timeout: int = config["response_timeout"]

        self.db_push_interval: int = config["db_push_interval"]

        self.queue: schedule.Q() = config["queue"]
        self.scheduler = AsyncIOScheduler()

        self.coins: int = config.get("coins", 0)
        self.items: dict = config.get("items", {})

        self.ws: aiohttp.ClientWebSocketResponse = config.get("ws", None)
        self.heartbeat_interval: int = config.get("heartbeat_interval", 40)

        self.session: aiohttp.ClientSession = config.get("session", None)
        self.voting_session: aiohttp.ClientSession = config.get(
            "voting_session", None)

        self.logger: logging.Logger = config.get("logger", None)
        self.traceback_logger: logging.Logger = config.get(
            "traceback_logger", None)
        self.logging_level: str = config.get("logging_level", "INFO")

        self._beg_interval = int(config["_beg_interval"])

        self._search_preference: list = config["_search_preference"]
        self._search_cancel: list = config["_search_cancel"]
        self._search_timeout: int = config["_search_timeout"]

        self._crime_preference: list = config["_crime_preference"]
        self._crime_cancel: list = config["_crime_cancel"]
        self._crime_timeout: int = config["_crime_timeout"]

        self.utils = utils

        self.create_loggers()
        asyncio.get_event_loop().run_until_complete(self.create_sessions())

    def update(self, config):
        self.__init__(config)

    def create_loggers(self):
        logging.basicConfig(
            filename=f"logs\{self.config['id']}.log",
            format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(status_code)s | %(username)-10s | %(message)s",
            datefmt="%I:%M:%S %p %d/%m/%Y",
            level=self.logging_level
        )
        logger = logging.getLogger()
        self.logger = logger
        self.config["logger"] = logger

        logging.basicConfig(
            filename=f"tracebacks\{self.config['id']}.log",
            format="%(levelname)-10s | %(asctime)s | %(filename)-20s | %(token)s | %(traceback_id)s | %(username)-10s \n\n %(message)s\n=========================\n\n",
            datefmt="%I:%M:%S %p %d/%m/%Y",
            level="DEBUG"
        )
        traceback_logger = logging.getLogger()
        self.traceback_logger = traceback_logger
        self.config["traceback_logger"] = traceback_logger

    async def create_sessions(self):
        self.session = aiohttp.ClientSession()
        self.voting_session = aiohttp.ClientSession()

    async def _close_client_sessions(self):
        await self.session.close()
        await self.voting_session.close()

    def close_sessions(self):
        asyncio.get_event_loop().run_until_complete(self._close_client_sessions())

    def get_details(self, key=None):
        if key:
            return self.config.get(key, None)
        else:
            return self.config

    def _update_balance(self, amount: int, task: Literal["ADD", "REM", "SET"]) -> None:
        if task == "ADD":
            self.coins -= amount
        elif task == "REM":
            self.coins -= amount
        elif task == "SET":
            self.coins = amount

    def _update_items(self, items: dict, task: Literal["ADD", "REM", "SET"]) -> None:
        for item, amount in items.items():
            if task == "ADD":
                self.items[item] += amount
            elif task == "REM":
                self.items[item] -= amount
            elif task == "SET":
                self.items[item] = amount

            if not self.items[item]:
                del self.items[item]

    async def db_push(self):
        db = await aiosqlite.connect("dbs/db.sqlite3")
        await db.execute("INSERT OR REPLACE INTO data (user_id, coins, items) VALUES(?, ?, ?)", (self.id, self.coins, json.dumps(self.items), ))
        await db.commit()
        await db.close()

    async def get_items_coins(self):
        db = await aiosqlite.connect("dbs/db.sqlite3")
        data = await db.execute("SELECT coins, items FROM data WHERE user_id = ?", (self.id, ))
        data = await data.fetchone()
        if not data:
            return 0, {}
        return data

    async def send_message(self, payload: dict[str, str]) -> aiohttp.ClientResponse:
        send_message = await self.session.post(
            f"https://discord.com/api/v9/channels/{self.grind_channel_id}/messages",
            json=payload,
            headers=utils.get_headers(self, payload=payload))
        return send_message

    # async def interact(self, )

    async def wait_for(self, event_type: str, predicate, send_message_json: dict) -> Tuple[int, Union[None, Classes.MessageClass]]:
        start = time.time()
        if predicate == "default":  # must reference
            predicate = event["d"]["author"]["id"] == 270904126974590976 and event["d"]["referenced_message"] is not None and str(
                event["d"]["referenced_message"]["id"]) == str(send_message_json["id"])
        while time.time() - start < self.response_timeout:
            event = self.ws.recv()
            if event["t"] == event_type and predicate(event, send_message_json):
                return 200, Classes.MessageClass(event["d"])
        else:
            return 408, None
