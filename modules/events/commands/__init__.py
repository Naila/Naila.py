from .commands import Commands


async def setup(bot):
    await bot.add_cog(Commands(bot))
