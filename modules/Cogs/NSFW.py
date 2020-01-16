import random

import discord
from discord.ext import commands

from utils.checks import checks
from utils.functions.api import boobbot, sheri, nekos


__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            await ctx.send_help(ctx.command)

    @boobbot.command(name="boobs", description="Boobs")
    async def boobbot_boobs(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "boobs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="butts", description="Butts")
    async def boobbot_butts(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "ass")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="4k", description="High quality porn")
    async def boobbot_4k(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "4k")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="anal", description="Anal")
    async def boobbot_anal(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "anal")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bdsm", description="BDSM")
    async def boobbot_bdsm(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "bdsm")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="black", description="Black women")
    async def boobbot_black(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "black")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bj", description="Blowjobs")
    async def boobbot_blowjob(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "blowjob")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bottomless", description="Bottomless girls")
    async def boobbot_bottomless(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "bottomless")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="collared", description="Girls wearing collars")
    async def boobbot_collared(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "collared")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="cumsluts", description="Covered in cum")
    async def boobbot_cumsluts(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "cumsluts")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="dp", description="Double penetration")
    async def boobbot_dpgirls(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "dpgirls")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="easter", description="Easter themed")
    async def boobbot_easter(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "easter")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="futa", description="Hentai: Futa")
    async def boobbot_futa(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "futa")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="gay", description="Gay porn")
    async def boobbot_gay(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "gay")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="gifs", description="Porn gifs")
    async def boobbot_gifs(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "Gifs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="group", description="Group porn")
    async def boobbot_group(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "group")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="halloween", description="Halloween themed")
    async def boobbot_halloween(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "halloween")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="hentai", description="Hentai")
    async def boobbot_hentai(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "hentai")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="lesbians", description="Girl on girl")
    async def boobbot_lesbians(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "lesbians")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pawg", description="Phat ass white girls")
    async def boobbot_pawg(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "pawg")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pegged", description="Women pegging men")
    async def boobbot_pegged(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "pegged")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="dick", description="Dicks")
    async def boobbot_dick(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "penis")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="poke", description="Hentai: Pokemon")
    async def boobbot_poke(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "PokePorn")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pussy", description="Pussy")
    async def boobbot_pussy(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "pussy")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="real", description="Real women")
    async def boobbot_real(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "real")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="redhead", description="Red heads")
    async def boobbot_redhead(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "red")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="tatted", description="Tatted women")
    async def boobbot_tatted(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        endpoint = random.choice(["tattoo", "wtats"])
        url = await boobbot(ctx.session, endpoint)
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="thighs", description="Thighs")
    async def boobbot_thighs(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "thighs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="tiny", description="Tiny girls")
    async def boobbot_tiny(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "tiny")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="toys", description="Porn with toys")
    async def boobbot_toys(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "toys")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="traps", description="Traps")
    async def boobbot_traps(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "traps")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="vday", description="Valentines themed")
    async def boobbot_vday(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "vday")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="xmas", description="Christmas themed")
    async def boobbot_xmas(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "xmas")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="yaoi", description="Hentai: Boys' love")
    async def boobbot_yaoi(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "yaoi")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="yiff", description="Furry images")
    async def boobbot_yiff(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await boobbot(ctx.session, "yiff")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @checks.is_nsfw()
    @commands.group(case_insensitive=True, description="NSFW Furry images from sheri.bot")
    async def sheri(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri.command(name="yiff", description="Normal yiff")
    async def sheri_yiff(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await sheri(ctx.session, "yiff")
        em = await self.sheri_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @sheri.command(name="gif", description="Yiff gifs")
    async def sheri_gif(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await sheri(ctx.session, "gif")
        em = await self.sheri_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @checks.is_nsfw()
    @commands.group(case_insensitive=True, description="NSFW images from neko.life")
    async def nneko(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @nneko.command(name="neko", description="Nekos")
    async def nneko_neko(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await nekos(ctx.session, "lewd")
        em = await self.nekos_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @nneko.command(name="ngif", description="Neko gifs")
    async def nneko_ngif(self, ctx):
        """{"user": [], "bot": ["embed_links"]}"""
        url = await nekos(ctx.session, "nsfw_neko_gif")
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
    bot.add_cog(NSFW(bot))
