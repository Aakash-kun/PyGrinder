from utils import Classes

async def dbl_vote(instance: Classes.Instance):
    """
    Vote for the bot on discordbotslist.com
    The instance class contains all necessary attrs

    return json of response, handle in main file.
    """

    link = await instance.voting_session.post(
        "https://discord.com/api/v9/oauth2/authorize?client_id=477949690848083968&response_type=code&redirect_uri=https%3A%2F%2Fdiscordbotlist.com%2Fcallback&scope=identify&state=oG8NqZ8f2LBNQRMg88jg23mBaN0ZSFbS",
        headers={
            "Authorization": instance.token
            }, 
        json={
            "authorize": True,
            "permissions":0
        }
    )

    code = (await link.json())["location"].split("code=")[-1]
    auth = await instance.voting_session.get(f"https://discordbotlist.com/api/v1/oauth?code={code}")

    dbl_token = await auth.json()["token"]
    upvote = await instance.voting_session.post("https://discordbotlist.com/api/v1/bots/270904126974590976/upvote", headers={'Authorization':dbl_token})

    return await upvote.json()
