import discord
from discord.ext import commands

from bot import Bot
from utils.APIs.Animals import Animal, Cat, Dog
from utils.checks import checks
from utils.ctx import Context


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.command(description="Random bears!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def bear(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("bear"))
        em.set_image(url=await Animal(ctx).image("bear"))
        await ctx.send(embed=em)

    @commands.command(description="Random birds!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def bird(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("bird"))
        em.set_image(url=await Animal(ctx).image("bird"))
        await ctx.send(embed=em)

    @commands.command(description="Random dolphins!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def dolphin(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("dolphin"))
        await ctx.send(embed=em)

    @commands.command(description="Random ducks!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def duck(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("duck"))
        await ctx.send(embed=em)

    @commands.command(description="Random elephants!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def elephant(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("elephant"))
        await ctx.send(embed=em)

    @commands.command(description="Random foxes!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def fox(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("fox"))
        em.set_image(url=await Animal(ctx).image("fox"))
        await ctx.send(embed=em)

    @commands.command(description="Random giraffes!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def giraffe(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("giraffe"))
        em.set_image(url=await Animal(ctx).image("giraffe"))
        await ctx.send(embed=em)

    @commands.command(description="Random hippos!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def hippo(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("hippo"))
        await ctx.send(embed=em)

    @commands.command(description="Random horses!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def horse(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("horse"))
        await ctx.send(embed=em)

    @commands.command(description="Random killer whales!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def killerwhale(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("killerwhale"))
        await ctx.send(embed=em)

    @commands.command(description="Random koalas!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def koala(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("koala"))
        em.set_image(url=await Animal(ctx).image("koala"))
        await ctx.send(embed=em)

    @commands.command(description="Random lions!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def lion(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("lion"))
        em.set_image(url=await Animal(ctx).image("lion"))
        await ctx.send(embed=em)

    @commands.group(aliases=["meow"], invoke_without_command=True, case_insensitive=True, description="Random cats!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def cat(self, ctx: Context, *, breed: str = None):
        if not ctx.invoked_subcommand:
            image, name, details = await Cat(ctx).image(breed)
            if not image:
                return await ctx.send_error("Invalid breed!")
            em = discord.Embed(color=await ctx.guildcolor(), description=details)
            em.set_author(name=name)
            em.set_image(url=image)
            await ctx.send(embed=em)

    @cat.command(name="breeds", description="List the available cat breeds!")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def cat_breeds(self, ctx: Context, page: int = 1):
        em = discord.Embed(color=await ctx.guildcolor())
        pages, breed_count = await Cat(ctx).breeds()
        if page > len(pages):
            return await ctx.send_error("There aren't that many pages!")
        em.description = pages[page - 1]
        em.set_author(name=f"There are currently {breed_count} breeds to chose f rom!")
        em.set_footer(text=f"Page: {page}/{len(pages)}")
        await ctx.send(embed=em)

    @commands.command(description="Random pandas!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def panda(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("panda"))
        em.set_image(url=await Animal(ctx).image("panda"))
        await ctx.send(embed=em)

    @commands.command(description="Random pigs!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def pig(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("pig"))
        await ctx.send(embed=em)

    @commands.command(description="Random red pandas!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def redpanda(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("redpanda"))
        await ctx.send(embed=em)

    @commands.command(description="Random sharks!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def shark(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("shark"))
        em.set_image(url=await Animal(ctx).image("shark"))
        await ctx.send(embed=em)

    @commands.command(description="Random snakes!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def snake(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description=await Animal(ctx).fact("snake"))
        em.set_image(url=await Animal(ctx).image("snake"))
        await ctx.send(embed=em)

    @commands.command(description="Random spiders!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def spider(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("spider"))
        await ctx.send(embed=em)

    @commands.command(description="Random turtles!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def turtle(self, ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor())
        em.set_image(url=await Animal(ctx).image("turtle"))
        await ctx.send(embed=em)

    @commands.group(invoke_without_command=True, case_insensitive=True, description="Random dogs!")
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def woof(self, ctx: Context, *, breed: str = None):
        if not ctx.invoked_subcommand:
            image, name, details = await Dog(ctx).image(breed)
            if not image:
                return await ctx.send_error("Invalid breed!")
            em = discord.Embed(color=await ctx.guildcolor(), description=details)
            em.set_author(name=name)
            em.set_image(url=image)
            await ctx.send(embed=em)

    @woof.command(name="breeds", description="List the available dog breeds!")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def woof_breeds(self, ctx: Context, page: int = 1):
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
