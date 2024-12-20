from .ready import Ready


async def setup(bot):
    await bot.add_cog(Ready(bot))
