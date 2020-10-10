import discord


async def sheri_embed(ctx):
    em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://sheri.bot/\n")
    em.set_author(name="Images provided by Sheri")
    em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
    return em

