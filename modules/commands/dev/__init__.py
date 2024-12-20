from .dev import Dev


async def setup(bot):
    await bot.add_cog(Dev(bot))
