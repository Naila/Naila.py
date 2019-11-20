import discord
from discord.ext import commands

from utils.functions.api import weeb


class UsedOnSelf(Exception):
    pass


class MissingArgument(Exception):
    pass


class TooManyUsers(Exception):
    pass


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def process_users(ctx, users):
        if not users:
            raise MissingArgument
        users = [x.mention for x in list(set(users)) if x is not ctx.author]
        if len(users) > 5:
            raise TooManyUsers
        if not users:
            raise UsedOnSelf
        word = "was" if len(users) == 1 else "were"
        users = f"{', '.join(users[:-1])}, and {users[-1]}" if len(users) > 2 else " and ".join(users)
        return users, word

    @commands.guild_only()
    @commands.command(description="Bite people!")
    async def bite(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} bitten by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session.session, "bite"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("Sorry but I cannot let you do that to yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Did someone make you blush?")
    async def blush(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} blush!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "blush"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You made yourself blush?")
        except MissingArgument:
            desc = f"{ctx.author.mention} blushes!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "blush"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Cry or say someone made you cry")
    async def cry(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} cry!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "cry"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You made yourself cry? Don't do that!")
        except MissingArgument:
            desc = f"{ctx.author.mention} cries!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "cry"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Cuddle people!")
    async def cuddle(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} cuddles with {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "cuddle"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("I'm sorry you're so lonely, you can cuddle me!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Dance!")
    async def dance(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} dances with {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "dance"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("There are only one of you..")
        except MissingArgument:
            desc = f"{ctx.author.mention} dances!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "dance"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Greet people!")
    async def greet(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} greets {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "greet"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You can't greet yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="High five people!")
    async def highfive(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} high fives {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "highfive"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("Don't be silly!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Hug people!")
    async def hug(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} given a BIG hug from {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "hug"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You cannot hug yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Insult people!")
    async def insult(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} insults {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "insult"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You cannot insult yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Kiss people!")
    async def kiss(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} kissed by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "kiss"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You pervert! You cannot do that to yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Lick people!")
    async def lick(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} licked by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "lick"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("Weirdo...")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Pat people!")
    async def pat(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} pats {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "pat"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("Why would you want to do something like that?")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Poke people!")
    async def poke(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} poked by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "poke"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("Why would you want to do something like that?")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Pout or say someone made you pout")
    async def pout(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} pout!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "pout"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You made yourself pout? Don't do that!")
        except MissingArgument:
            desc = f"{ctx.author.mention} pouts!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "pout"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Punch people!")
    async def punch(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} punched by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "punch"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You Masochist! You cannot do that to yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Shoot people!")
    async def shoot(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} shot by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "bang"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("Calm down! I'm sure we can solve whatever problem you're having")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Shrug it off ¯\_(ツ)_/¯")
    async def shrug(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} shrug!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "shrug"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You made yourself shrug?")
        except MissingArgument:
            desc = f"{ctx.author.mention} shrugs!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "shrug"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Slap people!")
    async def slap(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} {word} slapped by {ctx.author.mention}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "slap"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You masochist! I cannot let you do that to yourself!")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Tell people you're sleepy")
    async def sleepy(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} tells {users} that they are sleepy!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "sleepy"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You don't need to tell yourself..")
        except MissingArgument:
            desc = f"{ctx.author.mention} is sleepy!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "sleepy"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Did someone make you smile?")
    async def smile(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} smile!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "smile"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("You made yourself smile?")
        except MissingArgument:
            desc = f"{ctx.author.mention} smiles!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "smile"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Stare into space/at someone")
    async def stare(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} stares at {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "stare"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("I don't see a mirror..?")
        except MissingArgument:
            desc = f"{ctx.author.mention} stares into space"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "stare"))
            await ctx.send(embed=em)
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Give people the thumbs up!")
    async def thumbsup(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} gives {users} a thumbs up!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "thumbsup"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("What's the point in that?")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")

    @commands.guild_only()
    @commands.command(description="Tickle people!")
    async def tickle(self, ctx, *users: discord.Member):
        """{"user": [], "bot": ["embed_links"]}"""
        try:
            users, word = await self.process_users(ctx, users)
            desc = f"{ctx.author.mention} tickles {users}!"
            em = discord.Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "tickle"))
            await ctx.send(embed=em)
        except UsedOnSelf:
            await ctx.send_error("That's a little weird..")
        except MissingArgument:
            await ctx.missing_argument()
        except TooManyUsers:
            await ctx.send_error("Too many users!")


def setup(bot):
    bot.add_cog(Social(bot))
