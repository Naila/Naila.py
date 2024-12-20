from .social import Social


async def setup(bot):
    await bot.add_cog(Social(bot))
