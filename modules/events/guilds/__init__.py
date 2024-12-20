from .guilds import Guilds


async def setup(bot):
    await bot.add_cog(Guilds(bot))
