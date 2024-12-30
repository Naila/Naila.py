from .errors import Errors


async def setup(bot):
    await bot.add_cog(Errors(bot))
