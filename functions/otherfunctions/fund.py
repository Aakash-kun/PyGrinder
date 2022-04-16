from utils import Classes, utils

async def fund(instance: Classes.Instance, item):
    def check(m): # check for reply
        return m.author.id == 270904126974590976 and m.channel == itemshop.channel and m.reference.message_id == itemshop.id

    withdraw = await bot.grind_channel.send(f"pls with max")
    await bot.wait_for("message", check=check, timeout=conf.response_timeout) # Wait for reply

    itemshop = await bot.grind_channel.send(f"pls shop {item}")
    itemshopresponse = await bot.wait_for("message", check=check, timeout=conf.response_timeout) # Wait for reply

    itemprice = itemshopresponse.embeds[0].description.split("BUY** - ⏣ ")[1].split("\n")[0].replace(",", "")

    await bot.grind_channel.send("pls bal")
    balresponse = await bot.wait_for("message", check=check, timeout=conf.response_timeout) # Wait for reply
    wallet = balresponse.embeds[0].description.split("⏣")[1].split(" ")[1].replace(",", "")

    if int(itemprice) < int(wallet):
        if buy.buy(bot, item) is True:
            return True

    await bot.master.send(item)