from ...utils import fund
from ..config import conf
from ..support_functions import sfd
import random

"""
Lé currency command, 'pls fish'
Take argument bot

Import conf for timeout
Import fund for funding pole
Import sfd for get_interactions and react
"""

async def fish_function(bot):
    ms = await bot.grind_channel.send("pls fish")
    def check(m):
        return m.author.id == 270904126974590976 and m.channel == ms.channel and m.reference.message_id == ms.id
    msg = await bot.wait_for("message", check=check, timeout=conf.timeout)

    if "You cast out your line" in msg.content or "you found nothing" in msg.content:
        return

    if "You don't have a fishing pole, you" in msg.content:
        return await fund("pole")

    if "Catch the fish!" not in msg.content:
        return

    interactions = sfd.get_interactions(msg, bot)
    custom_id = interactions[1]["custom_id"][:-2]

    def checkedit(old_message, new_message):
        return old_message == new_message.author and old_message.channel == new_message.channel and new_message.reference.message_id == ms.id
    oldmsg, newmsg = await bot.wait_for("message_edit" , check=checkedit, timeout=conf.timeout)

    thefishline = newmsg.content.split("\n")[1]
    seven_spaces = "       "
    fourteen_spaces = "              "
    if " " not in thefishline:
        return sfd.react(f'{custom_id}{random.choices([":2", ":3"])}')

    elif seven_spaces in thefishline and fourteen_spaces not in thefishline:
        return sfd.react(f'{custom_id}{random.choices([":1", ":3"])}')

    elif fourteen_spaces in thefishline:
        return sfd.react(f'{custom_id}{random.choices([":1", ":2"])}')

    newmsg = await bot.wait_for("message_edit" , check=checkedit, timeout=conf.timeout)

    return