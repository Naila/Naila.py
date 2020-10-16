import os
from utils.functions.api import session_post, session_get
from requests.exceptions import HTTPError


class TopGG:
    base_url = "https://top.gg/api"
    headers = {
        "Authorization": os.getenv("TOPGG")
    }

    async def post_bot_stats(self, bot):
        bot.log.info("Posting to Top.gg")
        resp = await session_post(
            session=bot.session,
            url=self.base_url + f"bots/{bot.user.id}/stats",
            headers=self.headers,
            json={"server_count": len(bot.guilds), "shard_count": bot.shard_count}
        )
        if not resp:
            bot.log.error("Top.gg didn't respond.. maybe it's down?")
        else:
            bot.log.info("Posted to Top.gg")


class BotListSpace:
    base_url = "https://api.botlist.space/v1/"
    headers = {
        "Authorization": os.getenv("BOT_LIST_SPACE"),
        "Content-Type": "application/json"
    }

    # General
    async def get_site_stats(self, bot):
        resp = await session_get(
            session=bot.session,
            url=self.base_url + "statistics",
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            return data

    # Bots
    async def get_all_bots(self, bot):
        resp = await session_get(
            session=bot.session,
            url=self.base_url + "bots"
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            return data

    async def get_bot(self, bot, bot_id: int = None):
        bot_id = bot_id or bot.user.id
        resp = await session_get(
            session=bot.session,
            url=self.base_url + f"bots/{bot_id}",
            allowed_statuses=[200, 404]
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            if resp.status == 200:
                return data
            raise HTTPError(f"BotList.space returned {data['code']}: {data['message']}", response=resp)

    async def post_bot_stats(self, bot):
        # headers = self.headers
        # headers["Content-Type"] = "application/json"
        bot.log.info("Posting to BotList.space")
        resp = await session_post(
            session=bot.session,
            url=self.base_url + f"bots/{bot.user.id}",
            allowed_statuses=[200, 400, 401, 403, 404],
            headers=self.headers,
            json={"server_count": len(bot.guilds)}
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            bot.log.info("Posted to BotList.space")

    async def get_bot_upvotes(self, bot):
        resp = await session_get(
            session=bot.session,
            url=self.base_url + f"bots/{bot.user.id}/upvotes",
            allowed_statuses=[200, 401, 403, 404],
            headers=self.headers
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            if resp.status == 200:
                return data
            raise HTTPError(f"BotList.space returned {data['code']}: {data['message']}", response=resp)

    async def get_bot_uptime(self, bot, bot_id: int = None):
        bot_id = bot_id or bot.user.id
        resp = await session_get(
            session=bot.session,
            url=self.base_url + f"bots/{bot_id}/uptime",
            allowed_statuses=[200, 404],
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            if resp.status == 200:
                return data
            raise HTTPError(f"BotList.space returned {data['code']}: {data['message']}", response=resp)

    # Users
    async def get_user(self, bot, user_id: int = None):
        user_id = user_id or bot.owner_id
        resp = await session_get(
            session=bot.session,
            url=self.base_url + f"users/{user_id}",
            allowed_statuses=[200, 404]
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            if resp.status == 200:
                return data
            raise HTTPError(f"BotList.space returned {data['code']}: {data['message']}", response=resp)

    async def get_users_bots(self, bot, user_id: int = None):
        user_id = user_id or bot.owner_id
        resp = await session_get(
            session=bot.session,
            url=self.base_url + f"users/{user_id}/bots",
            allowed_statuses=[200, 404]
        )
        if not resp:
            bot.log.error("BotList.space didn't respond.. maybe it's down?")
        else:
            data = await resp.json()
            if resp.status == 200:
                return data
            raise HTTPError(f"BotList.space returned {data['code']}: {data['message']}", response=resp)


class DiscordBots:
    base_url = "https://discord.bots.gg/api/v1/"
    headers = {
        "Authorization": os.getenv("DISCORD_BOTS"),
        "Content-Type": "application/json"
    }

    async def post_bot_stats(self, bot):
        bot.log.info("Posting to DiscordBots")
        resp = await session_post(
            session=bot.session,
            url=self.base_url + f"bots/{bot.user.id}/stats",
            headers=self.headers,
            json={"guildCount": len(bot.guilds), "shardCount": bot.shard_count}
        )
        if not resp:
            bot.log.error("DiscordBots didn't respond.. maybe it's down?")
        else:
            bot.log.info("Posted to DiscordBots")
