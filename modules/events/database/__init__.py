from .database import Database


async def setup(bot):
    await bot.add_cog(Database(bot))
