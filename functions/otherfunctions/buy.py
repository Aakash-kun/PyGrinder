import asyncio
from ..config import conf
from ..support_functions import sfd

async def buy(bot, item):
    ms = await bot.grind_channel.send(f"pls buy {item}")
    def check(m):
        return m.author.id == 270904126974590976 and m.channel == ms.channel and m.reference.message_id == ms.id
    msg = await bot.wait_for("message", check=check, timeout=conf.response_timeout)

    try:
        interactions = await sfd.get_interactions(msg, bot)
        if len(interactions) > 0:
            await sfd.react(interactions[1]["custom_id"], msg, bot)
    except:
        pass

    if "Successful" in msg.embeds[0].description:
        return True

    return False