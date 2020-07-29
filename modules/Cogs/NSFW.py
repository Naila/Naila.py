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
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @boobbot.command(name="boobs", description="Boobs")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_boobs(self, ctx):
        url = await boobbot(ctx.session, "boobs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="butts", description="Butts")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_butts(self, ctx):
        url = await boobbot(ctx.session, "ass")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="4k", description="High quality porn")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_4k(self, ctx):
        url = await boobbot(ctx.session, "4k")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="anal", description="Anal")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_anal(self, ctx):
        url = await boobbot(ctx.session, "anal")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bdsm", description="BDSM")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_bdsm(self, ctx):
        url = await boobbot(ctx.session, "bdsm")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="black", description="Black women")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_black(self, ctx):
        url = await boobbot(ctx.session, "black")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bj", description="Blowjobs")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_blowjob(self, ctx):
        url = await boobbot(ctx.session, "blowjob")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="bottomless", description="Bottomless girls")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_bottomless(self, ctx):
        url = await boobbot(ctx.session, "bottomless")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="collared", description="Girls wearing collars")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_collared(self, ctx):
        url = await boobbot(ctx.session, "collared")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="cumsluts", description="Covered in cum")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_cumsluts(self, ctx):
        url = await boobbot(ctx.session, "cumsluts")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="dp", description="Double penetration")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_dpgirls(self, ctx):
        url = await boobbot(ctx.session, "dpgirls")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="easter", description="Easter themed")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_easter(self, ctx):
        url = await boobbot(ctx.session, "easter")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="futa", description="Hentai: Futa")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_futa(self, ctx):
        url = await boobbot(ctx.session, "futa")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="gay", description="Gay porn")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_gay(self, ctx):
        url = await boobbot(ctx.session, "gay")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="gifs", description="Porn gifs")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_gifs(self, ctx):
        url = await boobbot(ctx.session, "Gifs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="group", description="Group porn")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_group(self, ctx):
        url = await boobbot(ctx.session, "group")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="halloween", description="Halloween themed")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_halloween(self, ctx):
        url = await boobbot(ctx.session, "halloween")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="hentai", description="Hentai")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_hentai(self, ctx):
        url = await boobbot(ctx.session, "hentai")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="lesbians", description="Girl on girl")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_lesbians(self, ctx):
        url = await boobbot(ctx.session, "lesbians")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pawg", description="Phat ass white girls")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_pawg(self, ctx):
        url = await boobbot(ctx.session, "pawg")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pegged", description="Women pegging men")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_pegged(self, ctx):
        url = await boobbot(ctx.session, "pegged")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="dick", description="Dicks")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_dick(self, ctx):
        url = await boobbot(ctx.session, "penis")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="poke", description="Hentai: Pokemon")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_poke(self, ctx):
        url = await boobbot(ctx.session, "PokePorn")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="pussy", description="Pussy")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_pussy(self, ctx):
        url = await boobbot(ctx.session, "pussy")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="real", description="Real women")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_real(self, ctx):
        url = await boobbot(ctx.session, "real")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="redhead", description="Red heads")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_redhead(self, ctx):
        url = await boobbot(ctx.session, "red")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="tatted", description="Tatted women")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_tatted(self, ctx):
        endpoint = random.choice(["tattoo", "wtats"])
        url = await boobbot(ctx.session, endpoint)
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="thighs", description="Thighs")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_thighs(self, ctx):
        url = await boobbot(ctx.session, "thighs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="tiny", description="Tiny girls")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_tiny(self, ctx):
        url = await boobbot(ctx.session, "tiny")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="toys", description="Porn with toys")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_toys(self, ctx):
        url = await boobbot(ctx.session, "toys")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="traps", description="Traps")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_traps(self, ctx):
        url = await boobbot(ctx.session, "traps")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="vday", description="Valentines themed")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_vday(self, ctx):
        url = await boobbot(ctx.session, "vday")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="xmas", description="Christmas themed")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_xmas(self, ctx):
        url = await boobbot(ctx.session, "xmas")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="yaoi", description="Hentai: Boys' love")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_yaoi(self, ctx):
        url = await boobbot(ctx.session, "yaoi")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @boobbot.command(name="yiff", description="Furry images")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobbot_yiff(self, ctx):
        url = await boobbot(ctx.session, "yiff")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @checks.is_nsfw()
    @commands.group(case_insensitive=True, description="NSFW Furry images from sheri.bot")
    async def sheri(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri.command(name="yiff", description="Normal yiff")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def sheri_yiff(self, ctx):
        url = await sheri(ctx.session, "yiff")
        em = await self.sheri_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    @sheri.command(name="gif", description="Yiff gifs")
    @checks.custom_bot_has_permissions(embed_links=True)
    async def sheri_gif(self, ctx):
        url = await sheri(ctx.session, "gif")
        em = await self.sheri_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.send(embed=em)

    # @checks.is_nsfw()
    # @commands.group(case_insensitive=True, description="NSFW images from neko.life")
    # async def nneko(self, ctx):
    #     if not ctx.invoked_subcommand:
    #         await ctx.send_help(ctx.command)
    #
    # @nneko.command(name="neko", description="Nekos")
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def nneko_neko(self, ctx):
    #     url = await nekos(ctx.session, "lewd")
    #     em = await self.nekos_embed(ctx)
    #     em.set_image(url=url)
    #     em.description += f"**Image URL:** [Click Here]({url})"
    #     await ctx.send(embed=em)
    #
    # @nneko.command(name="ngif", description="Neko gifs")
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def nneko_ngif(self, ctx):
    #     url = await nekos(ctx.session, "nsfw_neko_gif")
    #     em = await self.nekos_embed(ctx)
    #     em.set_image(url=url)
    #     em.description += f"**Image URL:** [Click Here]({url})"
    #     await ctx.send(embed=em)

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
