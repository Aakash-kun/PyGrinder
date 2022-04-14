from ctypes import Union
from utils import Classes, utils
import time, secrets, random
import json

async def crime_function(instance: Classes.Instance):

    payload = {"content": "pls crime"}
    send_message = await instance.session.post(
        f"https://discord.com/api/v9/channels/{instance.grind_channel_id}/messages",
        json=payload,
        headers=utils.get_headers(payload=payload))
    instance.logger.debug("Sent command request.", extra={"token": instance.token, "username": instance.name, "status_code": 200})

    if send_message.status_code != 200:
        instance.logger.warning("Command was not sent.", extra={"token": instance.token, "username": instance.name, "status_code": 417})
        return 417, None

    try:
        send_message_json = await send_message.json()
    except json.decoder.JSONDecodeError:
        instance.logger.warning("Command send response was not json-parsable", extra={"token": instance.token, "username": instance.name, "status_code": 412})
        return 412, None
    except Exception:
        instance.logger.error("Command send response - Unhandled Exception", extra={"token": instance.token, "username": instance.name, "status_code": 412})
        return 412, None

    response: Union[Classes.MessageClass, None] = await instance.wait_for(
        "MESSAGE_CREATE",
        "default",
        send_message_json)

    if response[0] == 408:
        instance.logger.warning(f"Bot did not reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 408})
        return 408, None
    elif response[0] == 200:
        instance.logger.debug(f"Bot gave a valid reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 408})

    if response.embed.title:
        if "You can't commit so many crimes" not in response.description:
            instance.logger.critical(f"Crime reply embed had a title without a ratelimit, conclusion: account has been banned.", extra={"token": instance.token, "username": instance.name, "status_code": 423})
            return 423, None
        else:
            instance.logger.warning(f"Crime reply embed had a title with a ratelimit, conclusion: command cooldown.", extra={"token": instance.token, "username": instance.name, "status_code": 429})
            return 429, int(response.embed.description.split("**")[1].split(" ")[0])

    if "**What" not in response.content:
        return 417, "Bot did not reply with a valid response"

    options = {c.label : c.custom_id for c in response.components}



    option = False
    if instance._crime_mode == 0:
        for i in instance._crime_preferences:
            if i in options.keys():
                option = i
                break

        if not option:
            payload = {"content": random.choice(instance._crime_cancel)}

    payload = utils.get_payload(response=response, custom_id=option["custom_id"])

    interact = await instance.session.post(
        "https://discord.com/api/v9/interactions",
        headers=utils.get_headers(payload=payload),
        json=payload,
    )

    if interact.status_code != 204:
        return "Failed to interact", await interact.json() 

    response: Union[Classes.MessageClass, None] = await instance.wait_for(
        "MESSAGE_UPDATE",
        check=check)

    if interact.status_code != 204:
        return "Failed to interact", await interact.json()
    if response.embed.title:
        return "Banned"

    response_description = response.embed.description.split("<")[0]
    _coins = utils.get_digits(response_description)
    _item = response_description.split("**")[-2] if len(response_description.split("**")) > 2 else None

    instance._update_coins(_coins)
    instance._update_item(_item)
    instance.logger.info(f"Successfully executed `pls crime` and received {_coins} COINS and {_item} item")
    return "Success"