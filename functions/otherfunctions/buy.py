from utils import Instance

async def buy(instance: Instance.Instance, item: str, amount: int):
    ms = await instance.send_message(f"pls buy {item}")

    msg = await instance.wait_for("message", check=check, timeout=conf.response_timeout)

    try:
        interactions = await sfd.get_interactions(msg, bot)
        if len(interactions) > 0:
            await sfd.react(interactions[1]["custom_id"], msg, bot)
    except:
        pass

    if "Successful" in msg.embeds[0].description:
        return True

    return False