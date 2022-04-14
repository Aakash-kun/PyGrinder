from utils import Classes, utils
from typing import Union
import json

async def hunt_function(instance: Classes.Instance):
    payload = {"content": "pls hunt"}
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

    if "You went hunting in the woods" in sfd.clean(msg.content):
        return

    if "You don't have a hunting rifle" in msg.content:
        await fund("rifle")
        return

    if "fireball" not in msg.content and "dodge" not in msg.content:
        return

    # Dodge the fireball code goes here lmfao.
    interactions = sfd.get_interactions(msg, bot)
    custom_id = interactions[1]["custom_id"][:-2]

    def checkedit(old_message, new_message):
        return old_message == new_message.author and old_message.channel == new_message.channel and new_message.reference.message_id == ms.id
    oldmsg, newmsg = await bot.wait_for("message_edit" , check=checkedit, timeout=conf.timeout)

    thefireline = newmsg.content.split("\n")[1]
    seven_spaces = "       "
    fourteen_spaces = "              "
    if " " not in thefireline:
        return sfd.react(f'{custom_id}{random.choices([":2", ":3"])}')

    elif seven_spaces in thefireline and fourteen_spaces not in thefireline:
        return sfd.react(f'{custom_id}{random.choices([":1", ":3"])}')

    elif fourteen_spaces in thefireline:
        return sfd.react(f'{custom_id}{random.choices([":1", ":2"])}')
    
    await bot.wait_for("message_edit" , check=checkedit, timeout=conf.timeout)
    
    return