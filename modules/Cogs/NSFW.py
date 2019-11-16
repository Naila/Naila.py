import random

import discord
from discord.ext import commands

from utils.checks import checks
from utils.functions.api import boobbot, sheri, nekos


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @staticmethod
    async def boobbot_embed(ctx):
        em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://boob.bot/\n")
        em.set_author(name="Images provided by BoobBot")
        em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
        return em

    @staticmethod
    async def sheri_embed(ctx):
        em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://sheri.bot/\n")
        em.set_author(name="Images provided by Sheri")
        em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
        return em

    @staticmethod
    async def nekos_embed(ctx):
        em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://nekos.life/\n")
        em.set_author(name="Images provided by Nekos.life")
        em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
        return em

    @checks.is_nsfw()
    @commands.group(aliases=["bb"], case_insensitive=True, description="Porn from boob.bot")
    async def boobbot(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            await ctx.group_help()

    @boobbot.command(name="boobs", description="Boobs")
    async def boobbot_boobs(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "boobs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="butts", description="Butts")
    async def boobbot_butts(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "ass")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="4k", description="High quality porn")
    async def boobbot_4k(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "4k")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="anal", description="Anal")
    async def boobbot_anal(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "anal")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bdsm", description="BDSM")
    async def boobbot_bdsm(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "bdsm")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="black", description="Black women")
    async def boobbot_black(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "black")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bj", description="Blowjobs")
    async def boobbot_blowjob(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "blowjob")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bottomless", description="Bottomless girls")
    async def boobbot_bottomless(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "bottomless")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="collared", description="Girls wearing collars")
    async def boobbot_collared(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "collared")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="cumsluts", description="Covered in cum")
    async def boobbot_cumsluts(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "cumsluts")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="dp", description="Double penetration")
    async def boobbot_dpgirls(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "dpgirls")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="easter", description="Easter themed")
    async def boobbot_easter(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "easter")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="futa", description="Hentai: Futa")
    async def boobbot_futa(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "futa")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="gay", description="Gay porn")
    async def boobbot_gay(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "gay")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="gifs", description="Porn gifs")
    async def boobbot_gifs(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "Gifs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="group", description="Group porn")
    async def boobbot_group(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "group")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="halloween", description="Halloween themed")
    async def boobbot_halloween(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "halloween")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="hentai", description="Hentai")
    async def boobbot_hentai(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "hentai")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="lesbians", description="Girl on girl")
    async def boobbot_lesbians(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "lesbians")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pawg", description="Phat ass white girls")
    async def boobbot_pawg(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "pawg")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pegged", description="Women pegging men")
    async def boobbot_pegged(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "pegged")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="dick", description="Dicks")
    async def boobbot_dick(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "penis")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="poke", description="Hentai: Pokemon")
    async def boobbot_poke(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "PokePorn")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pussy", description="Pussy")
    async def boobbot_pussy(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "pussy")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="real", description="Real women")
    async def boobbot_real(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "real")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="redhead", description="Red heads")
    async def boobbot_redhead(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "red")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="tatted", description="Tatted women")
    async def boobbot_tatted(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        endpoint = random.choice(["tattoo", "wtats"])
        url = await boobbot(ctx, endpoint)
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="thighs", description="Thighs")
    async def boobbot_thighs(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "thighs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="tiny", description="Tiny girls")
    async def boobbot_tiny(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "tiny")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="toys", description="Porn with toys")
    async def boobbot_toys(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "toys")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="traps", description="Traps")
    async def boobbot_traps(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "traps")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="vday", description="Valentines themed")
    async def boobbot_vday(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "vday")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="xmas", description="Christmas themed")
    async def boobbot_xmas(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "xmas")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="yaoi", description="Hentai: Boys' love")
    async def boobbot_yaoi(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "yaoi")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="yiff", description="Furry images")
    async def boobbot_yiff(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx, "yiff")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @checks.is_nsfw()
    @commands.group(case_insensitive=True, description="NSFW Furry images from sheri.bot")
    async def sheri(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            await ctx.group_help()

    @sheri.command(name="yiff", description="Normal yiff")
    async def sheri_yiff(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await sheri(ctx, "yiff")
        em = await self.sheri_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @sheri.command(name="gif", description="Yiff gifs")
    async def sheri_gif(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await sheri(ctx, "gif")
        em = await self.sheri_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @commands.group(case_insensitive=True, description="NSFW images from neko.life")
    async def nneko(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            await ctx.group_help()

    @checks.is_nsfw()
    @nneko.command(name="neko", description="Nekos")
    async def nneko_neko(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await nekos(ctx, "lewd")
        em = await self.nekos_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @checks.is_nsfw()
    @nneko.command(name="ngif", description="Neko gifs")
    async def nneko_ngif(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await nekos(ctx, "nsfw_neko_gif")
        em = await self.nekos_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    # TODO: SFW image commands
    # @neko.command(name="")
    # async def neko_sfw(self, ctx):
    #     """SFW Nekos"""
    #     url = await self.make_embed(ctx, "neko", "neko")
    #     await ctx.send(embed=em)
    #
    # @neko.command(name="gif")
    # async def neko_gif(self, ctx):
    #     """SFW Neko gifs"""
    #     url = await self.make_embed(ctx, "neko", "ngif")
    #     await ctx.send(embed=em)
    #
    # @neko.command(name="")
    # async def neko_kitsune(self, ctx):
    #     """SFW fox girls"""
    #     url = await self.make_embed(ctx, "neko", "fox_girl")
    #     await ctx.send(embed=em)


def setup(bot):
    n = NSFW(bot)
    bot.add_cog(n)
