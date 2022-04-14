from utils import Classes, utils
from typing import Union

import secrets
import random
import json


async def search_function(instance: Classes.Instance):
    """
    The entire function to... search.
    Take in instance, it has everything we need!
    """

    # Send message and log
    payload: dict = {"content": "pls search"}
    send_message = await instance.session.post(
        f"https://discord.com/api/v9/channels/{instance.grind_channel_id}/messages",
        json=payload,
        headers=utils.get_headers(payload=payload))
    instance.logger.debug("Sent command request.", extra={"token": instance.token, "username": instance.name, "status_code": 200})


    # send message response error handling
    send_message_json = None
    try:
        send_message_json = await send_message.json()
    except json.decoder.JSONDecodeError:
        instance.logger.warning("Command send response was not json-parsable", extra={"token": instance.token, "username": instance.name, "status_code": 412})
        return 412, "NotJson"
    except Exception:
        instance.logger.error("Command send response - Unhandled Exception", extra={"token": instance.token, "username": instance.name, "status_code": 422})
        return 422, "NotHandled"

    # Send message error handling
    if send_message.status_code != 200:
        instance.logger.warning("Command was not sent.", extra={"token": instance.token, "username": instance.name, "status_code": 417})
        return 417, send_message_json if send_message_json else send_message.content

    # Wait for bot response
    response: tuple[int, Union[Classes.MessageClass, None]] = await instance.wait_for(
        "MESSAGE_CREATE",
        "default",
        send_message_json)

    # Bot Response error handling
    if response[0] == 408:
        instance.logger.warning(f"Bot did not reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 408})
        return 408, "ResponseTimeout"
    elif response[0] == 200:
        instance.logger.debug(f"Bot gave a valid reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 200})

    # Bot response parsing for ban or cooldown
    if response.embed.title:
        if "You've already searched the area" not in response.description:
            instance.logger.critical(f"search reply embed had a title without a ratelimit, conclusion: account has been banned.", extra={"token": instance.token, "username": instance.name, "status_code": 423})
            return 423, "Banned"

        else:
            instance.logger.warning(f"Beg reply embed had a title with a ratelimit, conclusion: command cooldown.", extra={"token": instance.token, "username": instance.name, "status_code": 429})
            return 429, int(response.embed.description.split("**")[1].split(" ")[0])

    # Bot response parsing for success
    if "**Where" not in response[1].content:
        return 400, "InvalidResponse"

    # Calculating where to search (option)
    options: dict = {c.label : c.custom_id for c in response.components}

    for i in options.items(): # location preference
        if i[0] in instance._search_preference:
            option = i
            break
    
    interact = True
    if instance._searach_mode == 0: # if not preference, random
        if not option:
            option = random.choice(list(options.items))

    elif instance._searach_mode == 2: # no matter what, random
        option = random.choice(list(options.items))

    elif instance._search_mode == 1: # if not preference, cancel
        if not option:
            payload: dict = {"content": random.choice(instance._search_cancel)} # random search cancel from instance config
            send_message = await instance.session.post(
                f"https://discord.com/api/v9/channels/{instance.grind_channel_id}/messages",
                json=payload,
                headers=utils.get_headers(payload=payload))
            interact = False # ensure it does not try to interact
            send_message_json = None
            try:
                send_message_json = await send_message.json()
            except json.decoder.JSONDecodeError:
                instance.logger.warning("Command send response was not json-parsable", extra={"token": instance.token, "username": instance.name, "status_code": 412})
                return 412, "NotJson"
            except Exception:
                instance.logger.error("Command send response - Unhandled Exception", extra={"token": instance.token, "username": instance.name, "status_code": 422})
                return 422, "NotHandled"

            # Send message error handling
            if send_message.status_code != 200:
                instance.logger.warning("Command was not sent.", extra={"token": instance.token, "username": instance.name, "status_code": 417})
                return 417, send_message_json if send_message_json else send_message.content

    if interact: # try to interact only if circumstance
        payload: dict = {
            "type":3,
            "guild_id": response.guild_id,
            "channel_id": response.channel_id,
            "message_flags":0,
            "message_id": response.id,
            "application_id":"270904126974590976",
            "session_id": secrets.token_urlsafe(),
            "data": {
                "component_type":2,
                "custom_id": option["custom_id"],
            }
        }

        # Interact with search location option
        interact = await instance.session.post(
            "https://discord.com/api/v9/interactions",
            headers=utils.get_headers(payload=payload),
            json=payload,
        )

        # Interact respoe error handling
        if interact.status_code != 204:
            return 424, "InteractionFailed"

    # Wait for bot response
    response: tuple[int, Union[Classes.MessageClass, None]] = await instance.wait_for(
        "MESSAGE_UPDATE",

        lambda x: x["t"] == "MESSAGE_UPDATE"
        and x["d"]["author"]["id"] == 270904126974590976
        and x["d"]["referenced_message"] is not None
        and str(x["d"]["referenced_message"]["id"]) == str(send_message_json.id),

        send_message_json)

    # Bot response error handling
    if response[0] == 408:
        instance.logger.warning(f"Bot did not reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 408})
        return 408, "ResposneTimeOut"
    elif response[0] == 200:
        instance.logger.debug(f"Bot gave a valid reply in given response_timeout.", extra={"token": instance.token, "username": instance.name, "status_code": 408})

    # Bot response parsing for ban (we can't be on cooldown!)
    if response.embed.title:
        return 498, "Banned"

    # Parsing reply for possible received coins and items
    try:
        response_description = response.embed.description.split("<")[0]
        _coins = utils.get_digits(response_description)
        _item = response_description.split("**")[-2] if len(response_description.split("**")) > 2 else None

        # update instance coins and items
        instance._update_coins(_coins)
        instance._update_item(_item)
    except:
        instance.logger.warning(f"Unable to parse beg reply embed.", extra={"token": instance.token, "username": instance.name, "status_code": 100})

    instance.logger.debug(
        f"Successfully executed `pls beg` and received {_coins if _coins else 'None'} coins and {_item if _item else 'None'} item",
        extra={"token": instance.token, "username": instance.name, "status_code": 200}
        )
    return 200, None
