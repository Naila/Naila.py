from discord.ext.commands import Cog
from discord.ext.tasks import loop
from bot import Bot
from utils.APIs.BotLists import BotListSpace, DiscordBots, TopGG
from modules.Cogs.Reminders import DB as ReminderDB


class Loops(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.ten_second_loop.start()
#        self.botlists.start()

    def cog_unload(self):
        self.ten_second_loop.stop()
#        self.botlists.stop()

    @loop(seconds=10)
    async def ten_second_loop(self):
        await ReminderDB.check(self.bot)

    @loop(minutes=30)
    async def botlists(self):
        self.bot.log.info(
            f"Posting to all bot lists... | Shards: {self.bot.shard_count} | Guilds: {len(self.bot.guilds)}"
        )
#         await BotListSpace().post_bot_stats(self.bot)
        await DiscordBots().post_bot_stats(self.bot)
        await TopGG().post_bot_stats(self.bot)
        self.bot.log.info("Done posting")


def setup(bot):
    bot.add_cog(Loops(bot))
