import random
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

from discord import Embed, Member, File
from discord.ext.commands import Cog, command, guild_only, MissingRequiredArgument, BadArgument

from bot import Bot
from utils.checks import checks
from utils.ctx import Context
from utils.functions import errors
from utils.functions.api import weeb
from utils.functions.images import ship
from utils.functions.text import readable_list


class Social(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @staticmethod
    def process_users(ctx: Context, users):
        users = [x for x in users if not isinstance(x, str)]
        if not users:
            raise MissingRequiredArgument(ctx.command.params["users"])
        users = [x.mention for x in list(set(users)) if x is not ctx.author]
        if len(users) > 5:
            raise BadArgument("You provided too many users!")
        if not users:
            raise errors.UsedOnSelf
        word = "was" if len(users) == 1 else "were"
        users = readable_list(users)
        return users, word

    @staticmethod
    def draw_meter(rigged: bool = False):
        random_integer = 100 if rigged else random.randint(0, 100)
        love = Decimal(str(random_integer / 10)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        love_emoji = "❤"
        empty_bar = "🖤"
        if random_integer == 0:
            empty_bar = "💔"
            love_message = "That's not good... maybe delete this and try again before they see?"
        elif random_integer <= 15:
            love_message = "That's a yikes.."
        elif random_integer <= 30:
            love_message = "Maybe in the future?"
        elif random_integer <= 45:
            love_message = "I mean this is the perfect range for friends?"
        elif random_integer <= 60:
            love_message = "Maybe try talking more?"
        elif random_integer == 69:
            love_emoji = "😏"
            love_message = "That's the sex number *wink wonk*"
        elif random_integer <= 75:
            love_message = "Best friends, stay as best friends."
        elif random_integer <= 90:
            love_message = "Give it a go, you're made for each other!"
        elif random_integer <= 99:
            love_message = "I ship it!"
        else:
            love_emoji = "💛"
            love_message = "Go get married! I hope I'm invited ❤"

        bar = "".join(love_emoji if i < love else empty_bar for i in range(10))

        return f"**Love meter:** {bar} **{random_integer}%**\n**{love_message}**"

    @command(description="Ship your friends!")
    @guild_only()
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def ship(self, ctx: Context, lover1: Member, lover2: Member = None):
        lover2 = lover2 or ctx.author
        rigged = False
        name1 = lover1.name[:-round(len(lover1.name) / 2)] + lover2.name[-round(len(lover2.name) / 2):]
        name2 = lover2.name[:-round(len(lover2.name) / 2)] + lover1.name[-round(len(lover1.name) / 2):]
        if 854105269126168586 in [lover1.id, lover2.id] and 173237945149423619 in [lover1.id, lover2.id]:
            rigged = True
        desc = f"**{ctx.author.mention} ships {lover1.mention} and {lover2.mention}!**\n\n " \
               f"Ship names: __**{name1}**__ or __**{name2}**__\n\n " \
               f"{self.draw_meter(rigged)}"
        em = Embed(color=await ctx.guildcolor(), description=desc)
        em.set_author(name="Lovely shipping!")
        em.set_image(url='attachment://ship.png')
        file = await ship(self.bot.session, lover1.avatar_url_as(format="png"), lover2.avatar_url_as(format="png"))
        await ctx.reply(file=File(fp=file, filename="ship.png"), embed=em)

    @command(description="Bite people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def bite(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} bitten by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "bite"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("Sorry but I cannot let you do that to yourself!")

    @command(description="Did someone make you blush?")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def blush(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} blush!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "blush"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You made yourself blush?")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} blushes!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "blush"))
            await ctx.reply(embed=em)

    @command(description="Cry or say someone made you cry")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def cry(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} cry!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "cry"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You made yourself cry? Don't do that!")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} cries!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "cry"))
            await ctx.reply(embed=em)

    @command(description="Cuddle people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} cuddles with {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "cuddle"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("I'm sorry you're so lonely, you can cuddle me!")

    @command(description="Dance!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def dance(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} dances with {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "dance"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("There are only one of you..")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} dances!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "dance"))
            await ctx.reply(embed=em)

    @command(description="Greet people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def greet(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} greets {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "greet"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You can't greet yourself!")

    @command(description="High five people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} high fives {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "highfive"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("Don't be silly!")

    @command(description="Hug people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def hug(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} given a BIG hug from {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "hug"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You cannot hug yourself!")

    @command(description="Insult people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def insult(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} insults {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "insult"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You cannot insult yourself!")

    @command(description="Kiss people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} kissed by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "kiss"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You pervert! You cannot do that to yourself!")

    @command(description="Lick people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def lick(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} licked by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "lick"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("Weirdo...")

    @command(description="Pat people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def pat(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} pats {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "pat"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("Why would you want to do something like that?")

    @command(description="Poke people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def poke(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} poked by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "poke"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("Why would you want to do something like that?")

    @command(description="Pout or say someone made you pout")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def pout(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} pout!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "pout"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You made yourself pout? Don't do that!")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} pouts!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "pout"))
            await ctx.reply(embed=em)

    @command(description="Punch people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def punch(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} punched by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "punch"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You Masochist! You cannot do that to yourself!")

    @command(description="Shoot people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def shoot(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} shot by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "bang"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("Calm down! I'm sure we can solve whatever problem you're having")

    @command(description="Shrug it off ¯\_(ツ)_/¯")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def shrug(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} shrug!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "shrug"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You made yourself shrug?")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} shrugs!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "shrug"))
            await ctx.reply(embed=em)

    @command(description="Slap people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def slap(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} {word} slapped by {ctx.author.mention}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "slap"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You masochist! I cannot let you do that to yourself!")

    @command(description="Tell people you're sleepy")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def sleepy(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} tells {users} that they are sleepy!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "sleepy"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You don't need to tell yourself..")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} is sleepy!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "sleepy"))
            await ctx.reply(embed=em)

    @command(description="Did someone make you smile?")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def smile(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{users} made {ctx.author.mention} smile!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "smile"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("You made yourself smile?")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} smiles!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "smile"))
            await ctx.reply(embed=em)

    @command(description="Stare into space/at someone")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def stare(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} stares at {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "stare"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("I don't see a mirror..?")
        except MissingRequiredArgument:
            desc = f"{ctx.author.mention} stares into space"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "stare"))
            await ctx.reply(embed=em)

    @command(description="Give people the thumbs up!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def thumbsup(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} gives {users} a thumbs up!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "thumbsup"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("What's the point in that?")

    @command(description="Tickle people!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx: Context, *users: Union[Member, str]):
        try:
            users, word = self.process_users(ctx, users)
            desc = f"{ctx.author.mention} tickles {users}!"
            em = Embed(color=await ctx.guildcolor(), description=desc)
            em.set_image(url=await weeb(ctx.session, "tickle"))
            await ctx.reply(embed=em)
        except errors.UsedOnSelf:
            await ctx.send_error("That's a little weird..")


def setup(bot):
    bot.add_cog(Social(bot))
