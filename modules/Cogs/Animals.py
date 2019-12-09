import discord
from discord.ext import commands
from utils.APIs.Animals import *

__author__ = "Kanin"
__date__ = "12/02/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Random bears!")
    async def bear(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("bear"))
        em.set_image(url=await Animal(ctx).image("bear"))
        await ctx.send(embed=em)

    @commands.command(description="Random birds!")
    async def bird(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("bird"))
        em.set_image(url=await Animal(ctx).image("bird"))
        await ctx.send(embed=em)

    @commands.command(description="Random dolphins!")
    async def dolphin(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("dolphin"))
        await ctx.send(embed=em)

    @commands.command(description="Random ducks!")
    async def duck(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("duck"))
        await ctx.send(embed=em)

    @commands.command(description="Random elephants!")
    async def elephant(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("elephant"))
        await ctx.send(embed=em)

    @commands.command(description="Random foxes!")
    async def fox(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("fox"))
        em.set_image(url=await Animal(ctx).image("fox"))
        await ctx.send(embed=em)

    @commands.command(description="Random giraffes!")
    async def giraffe(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("giraffe"))
        em.set_image(url=await Animal(ctx).image("giraffe"))
        await ctx.send(embed=em)

    @commands.command(description="Random hippos!")
    async def hippo(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("hippo"))
        await ctx.send(embed=em)

    @commands.command(description="Random horses!")
    async def horse(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("horse"))
        await ctx.send(embed=em)

    @commands.command(description="Random killer whales!")
    async def killerwhale(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("killerwhale"))
        await ctx.send(embed=em)

    @commands.command(description="Random koalas!")
    async def koala(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("koala"))
        em.set_image(url=await Animal(ctx).image("koala"))
        await ctx.send(embed=em)

    @commands.command(description="Random lions!")
    async def lion(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("lion"))
        em.set_image(url=await Animal(ctx).image("lion"))
        await ctx.send(embed=em)

    @commands.command(description="Random pandas!")
    async def panda(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("panda"))
        em.set_image(url=await Animal(ctx).image("panda"))
        await ctx.send(embed=em)

    @commands.command(description="Random pigs!")
    async def pig(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("pig"))
        await ctx.send(embed=em)

    @commands.command(description="Random red pandas!")
    async def redpanda(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("redpanda"))
        await ctx.send(embed=em)

    @commands.command(description="Random sharks!")
    async def shark(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("shark"))
        em.set_image(url=await Animal(ctx).image("shark"))
        await ctx.send(embed=em)

    @commands.command(description="Random snakes!")
    async def snake(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("snake"))
        em.set_image(url=await Animal(ctx).image("snake"))
        await ctx.send(embed=em)

    @commands.command(description="Random spiders!")
    async def spider(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("spider"))
        await ctx.send(embed=em)

    @commands.command(description="Random turtles!")
    async def turtle(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("turtle"))
        await ctx.send(embed=em)

    @commands.group(invoke_without_command=True, case_insensitive=True, description="Random cats!")
    async def meow(self, ctx, *, breed: str = None):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            image, name, details = await Cat(ctx).image(breed)
            if not image:
                return await ctx.send_error("Invalid breed!")
            em = discord.Embed(color=await ctx.guildcolor(), description=details)
            em.set_author(name=name)
            em.set_image(url=image)
            await ctx.send(embed=em)

    @meow.command(name="breeds", description="List the available cat breeds!")
    async def meow_breeds(self, ctx, page: int = 1):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        pages, breed_count = await Cat(ctx).breeds()
        if page > len(pages):
            return await ctx.send_error("There aren't that many pages!")
        em.description = pages[page - 1]
        em.set_author(name=f"There are currently {breed_count} breeds to chose from!")
        em.set_footer(text=f"Page: {page}/{len(pages)}")
        await ctx.send(embed=em)

    @commands.group(invoke_without_command=True, case_insensitive=True, description="Random dogs!")
    async def woof(self, ctx, *, breed: str = None):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            image, name, details = await Dog(ctx).image(breed)
            if not image:
                return await ctx.send_error("Invalid breed!")
            em = discord.Embed(color=await ctx.guildcolor(), description=details)
            em.set_author(name=name)
            em.set_image(url=image)
            await ctx.send(embed=em)

    @woof.command(name="breeds", description="List the available dog breeds!")
    async def woof_breeds(self, ctx, page: int = 1):
        """{"user": [], "bot": ["embed_links"]}"""
        em = discord.Embed(color=await ctx.guildcolor())
        pages, breed_count = await Dog(ctx).breeds()
        if page > len(pages):
            return await ctx.send_error("There aren't that many pages!")
        em.description = pages[page - 1]
        em.set_author(name=f"There are currently {breed_count} breeds to chose from!")
        em.set_footer(text=f"Page: {page}/{len(pages)}")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Animals(bot))
