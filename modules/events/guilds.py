from discord.ext import commands
import discord

from bot import Bot


class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.bot.log.info(f"Joined {guild}")
        await self.bot.pool.execute(
            "INSERT INTO guilds (id, in_guild) VALUES ($1, true) ON CONFLICT (id) DO UPDATE SET in_guild=true",
            str(guild.id)
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.bot.log.info(f"Left {guild}")
        await self.bot.pool.execute(
            "UPDATE guilds SET in_guild=false WHERE id=$1",
            str(guild.id)
        )


async def setup(bot):
    await bot.add_cog(Guilds(bot))
