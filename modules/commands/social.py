import discord
from discord.ext import commands

from bot import Bot
from utils.ctx import Context
from utils.functions.api import weeb


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_group(name="social")
    async def social(self, ctx):
        return

    @social.command(description="Bite people!")
    async def bite(self, ctx: Context, user: discord.Member):
        if user == ctx.author:
            return await ctx.send_error("Sorry but I cannot let you do that to yourself!")
        desc = f"{user.mention} was bitten by {ctx.author.mention}!"
        em = discord.Embed(color=0xaffaff, description=desc)
        em.set_image(url=await weeb(ctx.session, "bite"))
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Social(bot))
