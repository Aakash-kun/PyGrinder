async def work(channel, bot, usrid):
    await channel.send("pls work")
    def check(m):
        return m.author.id == 270904126974590976 and m.channel == channel and m.mentions[0].id == usrid
    msg = await bot.wait_for("message", check=check, timeout=imports.config.response_timeout)
    if "**Work for" in msg.content:
        # Work
        if "Reverse" in msg.content:
            gotit = imports.sfd.gettime()
            totype = str(((msg.content).split("`"))[-2][::-1])
        elif "Retype" in msg.content:
            gotit = imports.sfd.gettime()
            totype = str((msg.content).split("`")[-2])
        elif "Scramble" in msg.content:
            gotit = imports.sfd.gettime()
            totype = ""
    elif "until you can work" in msg.content:
        # Sleep
        # work.restart()
        print("sleep")
    elif "currently have a job to work" in msg.content:
        # Take a job
        print("take a job")
