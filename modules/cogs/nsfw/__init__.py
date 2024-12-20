from .nsfw import NSFW


async def setup(bot):
    await bot.add_cog(NSFW(bot))
