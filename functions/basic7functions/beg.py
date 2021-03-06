import aiohttp

from typing import Union, Tuple
from utils import Classes, utils, Instance


async def beg_function(instance: Instance.Instance) -> Tuple[int, Union[None, str]]:
    # Send message and log
    payload = {"content": "pls beg"}
    send_message: aiohttp.ClientResponse = await instance.send_message(payload)
    instance.logger.debug("Sent command request.", extra={"token": instance.token, "username": instance.name, "status_code": 200})

    send_message_response = await utils.send_response_eh(instance, send_message)
    if send_message_response[0] not in (200, 204):
        return send_message_response

    send_message_json = send_message_response[1]

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
            return 999, "PANIC"
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
