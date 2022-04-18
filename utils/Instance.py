import asyncio
import logging
from typing import Literal, Tuple, Union
import aiohttp
import time
from scheduler import schedule
from utils import Classes, utils

class Instance:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.id: int = config["id"]
        self.name: str = config["name"]
        self.token: str = config["token"]
        self.grind_channel_id: int = config["grind_channel_id"]
        self.master_id: int = config["master_id"]
        self.response_timeout: int = config["response_timeout"]
        self.queue: schedule.Q() = config["queue"]

        self.coins: int = config["coins"]
        self.items: dict = config["items"] # {item: amount}

        self.ws: aiohttp.ClientWebSocketResponse = None
        self.heartbeat_interval: int = None

        self.session: aiohttp.ClientSession = asyncio.get_event_loop().run_until_complete(self.create_session())
        self.voting_session: aiohttp.ClientSession = asyncio.get_event_loop().run_until_complete(self.create_voting_session())


        self.logger: logging.Logger = None
        self.traceback_logger: logging.Logger = None

        self._search_preference: list = config["_search_preference"]
        self._search_cancel: list = config["_search_cancel"]
        self._search_timeout: int = config["_search_timeout"]

        self._crime_preference: list = config["_crime_preference"]
        self._crime_cancel: list = config["_crime_cancel"]
        self._crime_timeout: int = config["_crime_timeout"]
        
    async def create_session(self):
        my_session = aiohttp.ClientSession()
        return my_session
        
    async def create_voting_session(self):
        my_session = aiohttp.ClientSession()
        return my_session

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

    def _update_balance(self, amount: int, task: Literal["ADD", "REM"]) -> None:
        if task == "ADD":
            self.coins -= amount
        elif task == "REM":
            self.coins -= amount

    def _update_items(self, items: dict, task: Literal["ADD", "REM"]) -> None:
        for item, amount in items.items():
            if task == "ADD":
                self.items[item] += amount
            elif task == "REM":
                self.items[item] -= amount

    async def send_message(self, payload: dict[str, str]) -> aiohttp.ClientResponse:
        send_message = await self.session.post(
            f"https://discord.com/api/v9/channels/{self.grind_channel_id}/messages",
            json=payload,
            headers=utils.get_headers(self, payload=payload))
        return send_message

    # async def interact(self, )

    async def wait_for(self, event_type: str, predicate, send_message_json: dict) -> Tuple[int, Union[None, Classes.MessageClass]]:
        start = time.time()
        if predicate == "default": # must reference
            predicate = event["d"]["author"]["id"] == 270904126974590976 and event["d"]["referenced_message"] is not None and str(event["d"]["referenced_message"]["id"]) == str(send_message_json["id"])
        while time.time() - start < self.response_timeout:
            event = self.ws.recv()
            if event["t"] == event_type and predicate(event, send_message_json):
                return 200, Classes.MessageClass(event["d"])
        else:
            return 408, None
