
from ...utils import fund
import traceback

"""
Lé currency command, 'pls dig'

Argument bot for bot instance and grind_channel
Import conf for timeout, dig_unscrambles and dig_missing
Import fund for funding shovel
Import sfd for reverse, retype, sort, clean
"""

async def dig_function(bot):

        ms = await bot.grind_channel.send("pls dig") # Send the command!

        def check(m): # Check for reply
            return m.author.id == 270904126974590976 and m.channel == ms.channel and m.reference.message_id == ms.id
        msg = await bot.wait_for("message", check=check, timeout=bot.conf.timeout) # Wait for reply.

        if "You dig in the" in msg.content or "you found nothing" in msg.content:
            return # It was a clean success

        if "You don't have a shovel" in msg.content:
            await fund("shovel")
            return # Requested a fund!
