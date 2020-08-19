import os


class BotListSpace:
    base_url = "https://api.botlist.space/v1/"
    headers = {
        "Authorization": os.getenv("BOT_LIST_SPACE"),
        "Content-Type": "application/json"
    }

    async def post(self, bot):
        async with bot.session.post(
                url=self.base_url + f"bots/{bot.user.id}",
                headers=self.headers,
                json={"server_count": len(bot.guilds)}
        ) as resp:
            if not resp or resp.status not in [200, 400, 401, 403, 404]:
                bot.log.error("Could not post to BotList.space.. maybe it's down?")
            else:
                data = await resp.json()
                if resp.status == 200:
                    bot.log.info("Posted to BotList.space")
                else:
                    bot.log.error(f"BotList.space returned {data['code']}: {data['message']}")
