import discord
from discord.ext import commands

from bot import Bot
from utils.ctx import Context
from utils.functions.api import boobbot
from utils.APIs.BoobBot import BoobBotApi


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_group(name="nsfw")
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        return

    @nsfw.group(name="fantasy")
    async def fantasy(self, ctx):
        return

    @nsfw.group(name="general")
    async def general(self, ctx):
        return

    @nsfw.group(name="holiday")
    async def holiday(self, ctx):
        return

    @nsfw.group(name="kink")
    async def kink(self, ctx):
        return

    @general.command(name="4k", description="4K Hotness!")
    async def image_4k(self, ctx: commands.Context):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="4k")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="anal", description="That ass love tho.")
    async def anal(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="anal")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="ass", description="Shows some ass.")
    async def ass(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="ass")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(
        name="bdsm",
        description="Bondage and Discipline (BD), Dominance and Submission (DS), Sadism and Masochism (SM)"
    )
    async def bdsm(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="bdsm")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="black", description="Gotta have that black love as well.")
    async def black(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="black")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="blowjob", description="BlowJobs!")
    async def blowjob(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="blowjob")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="boobs", description="Shows some boobs.")
    async def boobs(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="boobs")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="bottomless", description="Sexy!")
    async def bottomless(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="bottomless")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="collared", description="Play nice.")
    async def collared(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="collared")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="cumsluts", description="Sticky Love!")
    async def cumsluts(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="cumsluts")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="dick", description="Got dick?")
    async def dick(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="penis")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="dp", description="Gotta get that double love!")
    async def dp(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="dpgirls")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @holiday.command(name="easter", description="Easter is nice")
    async def easter(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="easter")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="feet", description="Feet")
    async def feet(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="feet")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @fantasy.command(name="futa", description="Hentai traps")
    async def futa(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="futa")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="gay", description="Got men?")
    async def gay(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="gay")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="gif", description="Sexy gifs!")
    async def gif(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="Gifs")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="group", description="For when 2 aren't enough...")
    async def group(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="group")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @holiday.command(name="halloween", description="Halloween")
    async def halloween(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="halloween")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @fantasy.command(name="hentai", description="Hentai")
    async def hentai(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="hentai")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="lesbians", description="Lesbians are sexy!")
    async def lesbians(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="lesbians")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="pawg", description="Phat Ass White Girls!")
    async def pawg(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="pawg")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="pegged", description="Strap-on love!")
    async def pegged(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="pegged")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @fantasy.command(name="poke", description="Pokemon Porn!")
    async def poke(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="PokePorn")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="puffies", description="Puffy nipples")
    async def puffies(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="puffies")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="pussy", description="Pussy!")
    async def pussy(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="pussy")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="red", description="Redheads: because redder is better!")
    async def red(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="red")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="tattoo", description="Tatted up women.")
    async def tattoo(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="tattoo")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @fantasy.command(name="tentacle", description="Tentacles")
    async def tentacle(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="tentacle")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="thicc", description="The beautiful thicc and chubby.")
    async def thicc(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="thicc")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="toys", description="Everything is better with toys ")
    async def toys(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="toys")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @kink.command(name="traps", description="Traps are hot!")
    async def traps(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="traps")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @general.command(name="tummy", description="Shows some tummy.")
    async def tummy(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="tummy")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @holiday.command(name="vday", description="Valentines ❤")
    async def vday(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="vday")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @holiday.command(name="xmas", description="Christmas")
    async def xmas(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="xmas")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @fantasy.command(name="yaoi", description="Boy love.")
    async def yaoi(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="yaoi")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @fantasy.command(name="yiff", description="Fucking furries")
    async def yiff(self, ctx):
        image = await BoobBotApi.get_image(ctx=ctx, image_type="yiff")
        em = discord.Embed(color=0xaffaff, description=f"[BoobBot](https://boob.bot) | [Image]({image})")
        em.set_image(url=image)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @nsfw.group(name="interact")
    async def interact(self, ctx):
        return

    async def validate_user(self, ctx: Context, member: discord.Member):
        if member.id == ctx.guild.me.id:
            await ctx.send_error("You don't meet my standards.")
            return False
        if member.bot:
            await ctx.send_error("Why would you want to do that to a bot..?")
            return False
        if member.id == ctx.author.id:
            await ctx.send_error("I'm not helping you do that!")
            return False
        return True

    @interact.command(name="69")
    async def funny_number(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} & {member.name} 69")
        em.set_image(url=await boobbot(ctx.session, "69"))
        await ctx.reply(content=f"{ctx.author.mention} & {member.mention} 69", embed=em)

    @interact.command(name="cum")
    async def cum(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} came on {member.name}, oh my")
        em.set_image(url=await boobbot(ctx.session, "cum"))
        await ctx.reply(content=f"{ctx.author.mention} came on {member.mention}, oh my", embed=em)

    @interact.command(name="dom")
    async def dom(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} dominates {member.name}")
        em.set_image(url=await boobbot(ctx.session, "dom"))
        await ctx.reply(content=f"{ctx.author.mention} dominates {member.mention}", embed=em)

    @interact.command(name="extreme")
    async def extreme(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} likes it extreme, are you in {member.name}?")
        em.set_image(url=await boobbot(ctx.session, "extreme"))
        await ctx.reply(content=f"{ctx.author.mention} likes it extreme, are you in {member.mention}?", embed=em)

    @interact.command(name="finger")
    async def finger(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} fingers {member.name}")
        em.set_image(url=await boobbot(ctx.session, "finger"))
        await ctx.reply(content=f"{ctx.author.mention} fingers {member.mention}", embed=em)

    @interact.command(name="fuck")
    async def fuck(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} fucks {member.name}")
        em.set_image(url=await boobbot(ctx.session, "fuck"))
        await ctx.reply(content=f"{ctx.author.mention} fucks {member.mention}", embed=em)

    @interact.command(name="kiss")
    async def kiss(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} kisses {member.name}")
        em.set_image(url=await boobbot(ctx.session, "kiss"))
        await ctx.reply(content=f"{ctx.author.mention} kisses {member.mention}", embed=em)

    @interact.command(name="lick")
    async def lick(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} licks {member.name}")
        em.set_image(url=await boobbot(ctx.session, "lick"))
        await ctx.reply(content=f"{ctx.author.mention} licks {member.mention}", embed=em)

    @interact.command(name="playrough")
    async def playrough(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} plays rough with {member.name}")
        em.set_image(url=await boobbot(ctx.session, "playrough"))
        await ctx.reply(content=f"{ctx.author.mention} plays rough with {member.mention}", embed=em)

    @interact.command(name="spank")
    async def spank(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} spanks {member.name}")
        em.set_image(url=await boobbot(ctx.session, "spank"))
        await ctx.reply(content=f"{ctx.author.mention} spanks {member.mention}", embed=em)

    @interact.command(name="sub")
    async def sub(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} is submissive for {member.name}")
        em.set_image(url=await boobbot(ctx.session, "sub"))
        await ctx.reply(content=f"{ctx.author.mention} is submissive for {member.mention}", embed=em)

    @interact.command(name="suck")
    async def suck(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} sucks off {member.name}")
        em.set_image(url=await boobbot(ctx.session, "suck"))
        await ctx.reply(content=f"{ctx.author.mention} sucks off {member.mention}", embed=em)

    @interact.command(name="tease")
    async def tease(self, ctx: Context, member: discord.Member):
        valid = await self.validate_user(ctx, member)
        if not valid:
            return
        em = discord.Embed(color=0xaffaff, title=f"{ctx.author.name} teases {member.name}")
        em.set_image(url=await boobbot(ctx.session, "tease"))
        await ctx.reply(content=f"{ctx.author.mention} teases {member.mention}", embed=em)


async def setup(bot):
    await bot.add_cog(NSFW(bot))
