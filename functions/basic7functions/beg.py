import traceback
from utils import Classes, utils
from typing import Optional, Union, Tuple

import json
import aiohttp
import time

async def beg_function(instance: Classes.Instance) -> Tuple[int, Union[None, str]]:
    """
    The entire function to... beg.
    Take in instance, it has everything we need!
    """

    # Send message and log
    payload = {"content": "pls beg"}
    send_message: aiohttp.ClientResponse = await instance.send_message(payload)
    instance.logger.debug("Sent command request.", extra={"token": instance.token, "username": instance.name, "status_code": 200})

    # send message response error handling
    send_message_json = None
    try:
        send_message_json: Optional[dict[str, str]] = await send_message.json()
    except json.decoder.JSONDecodeError:
        instance.logger.warning("Command send response was not json-parsable", extra={"token": instance.token, "username": instance.name, "status_code": 412})
        return 412, "NotJson"
    except Exception:
        traceback_id = f"{instance.id}.{time.time()}"
        instance.logger.error(f"beg send response - Unhandled Exception ({traceback_id})", extra={"token": instance.token, "username": instance.name, "status_code": 422})
        instance.log_traceback(traceback_id, traceback.format_exc())
        return 422, "NotHandled"

    # Send message error handling
    if send_message.status_code not in (200, 204):
        instance.logger.warning("Command was not sent.", extra={"token": instance.token, "username": instance.name, "status_code": 417})
        return 417, send_message_json if send_message_json else send_message.content

    # Wait for bot response
    response: Union[Classes.MessageClass, None] = await instance.wait_for(
        "MESSAGE_CREATE",
        "default",
        send_message_json)

    # Bot response error handling
    if response[0] == 408:
        instance.logger.warning(f"Bot did not reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 408})
        return 408, "ResponseTimeout"
    elif response[0] == 200:
        instance.logger.debug(f"Bot gave a valid reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 200})

    # Bot response parsing for ban or cooldown
    if response.embed.title:
        if "Stop begging so much" not in response.embed.description:
            instance.logger.critical(f"Beg reply embed had a title without a ratelimit, conclusion: account has been banned.", extra={"token": instance.token, "username": instance.name, "status_code": 423})
            return 423, "Banned"
        else:
            instance.logger.warning(f"Beg reply embed had a title with a ratelimit, conclusion: command cooldown.", extra={"token": instance.token, "username": instance.name, "status_code": 429})
            return 429, int(response.embed.description.split("**")[1].split(" ")[0])

    try:
        response_description = response.embed.description.split("\"")[1]
        _item = response_description.split("**")[-2] if len(response_description.split("**")) > 4 else 'None'
        _coins = utils.get_digits(response_description)

        instance._update_balance(_coins)
        instance._update_item(_item)
    except:
        instance.logger.warning(f"Unable to parse beg reply embed.", extra={"token": instance.token, "username": instance.name, "status_code": 100})

    instance.logger.debug(
        f"Successfully executed `pls beg` and received {_coins if _coins else 'no'} coins and a {_item if _item else '.'}",
        extra={"token": instance.token, "username": instance.name, "status_code": 200}
        )
    return 200, None
