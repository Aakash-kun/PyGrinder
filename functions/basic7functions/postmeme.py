from utils import Classes, utils
import time, secrets, random
from support_functions import fund

async def postmeme_function(instance: Classes.Instance):
    payload = {"content": f"pls {random.choice(['pm', 'postmeme'])}"}
    send_message = await instance.session.post(
        f"https://discord.com/api/v9/channels/{instance.grind_channel_id}/messages",
        json=payload,
        headers=utils.get_headers(payload=payload))

    if send_message.status_code != 200:
        return "Failed to send message", await send_message.json()

    response = await instance.wait_for("MESSAGE_CREATE", "default", send_message_json=await send_message.json())

    if response[0] == 408:
        return "Bot did not reply in given response_timeout", None
    elif response[0] == 200:
        pass

    if response.embed.title:
        if "You can't commit so many crimes" not in response.description:
            return "Crime reply embed had a title without a ratelimit, conclusion: account has been banned", None
        else:
            return "Crime reply embed had a title with a ratelimit, conclusion: command cooldown", int(response.embed.description.split("**")[1].split(" ")[0])

    if "**What" not in response.content:
        return "Bot did not reply with a valid response", None

    options = {c.label : c.custom_id for c in response.components}

    option = False
    if instance._crime_mode == 0:
        for i in instance._crime_preferences:
            if i in options.keys():
                option = i
                break

        if not option:
            return "No valid option found", None

    if response[0] != 204:
        return "Bot did not reply in given response_timeout"

    if response.embed.title:
        if "post memes too much" not in response.description:
            return "Banned"
        else:
            return "Ratelimited", int(response.description.split("**")[1].split(" ")[0])

    if "you need to buy a laptop" in response.content:
        await fund(instance, "laptop")

    if "Pick a meme to post to the internet" not in response.embed.description:
        return "Bot did not reply with a valid response"

    option = random.choice({c.label : c.custom_id for c in response.components})[1]

    payload = {
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

    interact = await instance.session.post(
        "https://discord.com/api/v9/interactions",
        headers=utils.get_headers(payload=payload),
        json=payload,
    )

    if interact.status_code != 204:
        return "Failed to interact", await interact.json() 


    response = instance.wait_for("MESSAGE_UPDATE", lambda event: event["d"]["author"]["id"] == 270904126974590976 and event["d"]["referenced_message"] is not None and str(event["d"]["referenced_message"]["id"]) == str((await send_message.json()).id))
    if response[0] != 204:
        return "Bot did not reply in given response_timeout"
    if response.embed.title:
        return "Banned"

    response_description = response.embed.description
    if "You got" in response_description:
        return "Broke Laptop"

    if "also a fan of your memes" not in response_description:
        _coins = utils.get_digits(response_description)
        _item = None
    else:
        _coins = utils.get_digits(response_description.split("also a fan of your memes")[0])
        _item = response_description.split("**")[-2]

    instance._update_coins(_coins)
    instance._update_item(_item)
    instance.logger.info(f"Successfully executed `pls crime` and received {_coins} COINS and {_item} item")
    return "Success"
