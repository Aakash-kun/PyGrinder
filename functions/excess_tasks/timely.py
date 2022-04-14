from utils import Classes, utils
import time

async def timely_function(instance: Classes.Instance, command: str):
    """
    Common function for daily/weekly/monthly commands
    instance contains all necessary attrs, command is the command name
    """

    # send message
    payload = {"content": f"pls {command}"}
    send_message = await instance.session.post(
        f"https://discord.com/api/v9/channels/{instance.grind_channel_id}/messages",
        json=payload,
        headers=utils.get_headers(payload=payload))

    # verify that send message aas a success
    if send_message.status_code != 200:
        return "Failed to send message", await send_message.json()

    
    response = await instance.wait_for(
        "MESSAGE_CREATE",
        lambda event: event["d"]["author"]["id"] == 270904126974590976 and
        event["d"]["referenced_message"] is not None and
        str(event["d"]["referenced_message"]["id"]) == str((await send_message.json()).id))

    if response[0] != 409:
        return "Bot did not reply in given response_timeout"

    # parse reply
    if "daily" in response.embed.title.lower():
        if "already claimed your daily" in response.embed.title:
            return "Ratelimited", 
        if "Daily Coins" in response.embed.title:
            pass
        else:
            return "Banned"

    # extract coins and item received
    response_description = response.embed.description.split("!")[0]
    _item = f"{response_description.split('**')[-1]}Box" if len(response_description.split("**")) > 4 else None
    _coins = utils.get_digits(response_description)

    instance._update_balance(_coins)
    instance._update_item(_item)
    instance.logger.info(f"Successfully executed `pls beg` and received {_coins} coins and {_item} item")
    return "Success"


"""Ease of calling in main file"""
async def daily_function(instance: Classes.Instance):
    return await timely_function(instance, "daily")

async def weekly_function(instance: Classes.Instance):
    return await timely_function(instance, "weekly")

async def monthly_function(instance: Classes.Instance):
    return await timely_function(instance, "montly")
