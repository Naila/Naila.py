import random

import discord
from discord.ext import commands

from bot import Bot
from utils.checks import checks
from utils.ctx import Context
from utils.functions.api import boobbot


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @staticmethod
    async def boobbot_embed(ctx: Context):
        em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://boob.bot/\n")
        em.set_author(name="Images provided by BoobBot")
        em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
        return em

    # @staticmethod
    # async def sheri_embed(ctx):
    #     em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://sheri.bot/\n")
    #     em.set_author(name="Images provided by Sheri")
    #     em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
    #     return em
    #
    # @staticmethod
    # async def nekos_embed(ctx):
    #     em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://nekos.life/\n")
    #     em.set_author(name="Images provided by Nekos.life")
    #     em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
    #     return em

    @commands.command(aliases=["bb"], hidden=True)
    @checks.is_nsfw()
    async def boobbot(self, ctx: Context, old_command: str = None):
        prefix = ctx.prefix
        if not old_command:
            return await ctx.reply(
                f"This command will be deleted soon, you can view the NSFW commands with {prefix}help NSFW"
            )
        return await ctx.reply(f"You no longer have to prefix NSFW commands with `bb` {prefix}help NSFW")

    @commands.command(aliases=["tits"], description="Boobs")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def boobs(self, ctx: Context):
        url = await boobbot(ctx.session, "boobs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(aliases=["ass"], description="Butts")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def butts(self, ctx: Context):
        url = await boobbot(ctx.session, "ass")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(name="4k", description="High quality porn")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def _4k(self, ctx: Context):
        url = await boobbot(ctx.session, "4k")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Anal")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def anal(self, ctx: Context):
        url = await boobbot(ctx.session, "anal")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="BDSM")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def bdsm(self, ctx: Context):
        url = await boobbot(ctx.session, "bdsm")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(name="black", description="Black women")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def black(self, ctx: Context):
        url = await boobbot(ctx.session, "black")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(aliases=["bj"], description="Blowjobs")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def blowjob(self, ctx: Context):
        url = await boobbot(ctx.session, "blowjob")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Bottomless girls")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def bottomless(self, ctx: Context):
        url = await boobbot(ctx.session, "bottomless")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Girls wearing collars")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def collared(self, ctx: Context):
        url = await boobbot(ctx.session, "collared")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Covered in cum")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def cumsluts(self, ctx: Context):
        url = await boobbot(ctx.session, "cumsluts")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(aliases=["dp"], description="Double penetration")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def doublepenetration(self, ctx: Context):
        url = await boobbot(ctx.session, "dpgirls")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Easter themed")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def easter(self, ctx: Context):
        url = await boobbot(ctx.session, "easter")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Hentai: Futa")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def futa(self, ctx: Context):
        url = await boobbot(ctx.session, "futa")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Gay porn")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def gay(self, ctx: Context):
        url = await boobbot(ctx.session, "gay")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Porn gifs")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def gifs(self, ctx: Context):
        url = await boobbot(ctx.session, "Gifs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Group porn")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def group(self, ctx: Context):
        url = await boobbot(ctx.session, "group")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Halloween themed")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def halloween(self, ctx: Context):
        url = await boobbot(ctx.session, "halloween")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Hentai")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def hentai(self, ctx: Context):
        url = await boobbot(ctx.session, "hentai")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Girl on girl")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def lesbians(self, ctx: Context):
        url = await boobbot(ctx.session, "lesbians")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Phat ass white girls")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def pawg(self, ctx: Context):
        url = await boobbot(ctx.session, "pawg")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Women pegging men")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def pegged(self, ctx: Context):
        url = await boobbot(ctx.session, "pegged")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Dicks")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def dick(self, ctx: Context):
        url = await boobbot(ctx.session, "penis")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Hentai: Pokemon")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def pokeporn(self, ctx: Context):
        url = await boobbot(ctx.session, "PokePorn")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Pussy")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def pussy(self, ctx: Context):
        url = await boobbot(ctx.session, "pussy")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Real women")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def real(self, ctx: Context):
        url = await boobbot(ctx.session, "real")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Red heads")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def redhead(self, ctx: Context):
        url = await boobbot(ctx.session, "red")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Tatted women")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def tatted(self, ctx: Context):
        endpoint = random.choice(["tattoo", "wtats"])
        url = await boobbot(ctx.session, endpoint)
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Thighs")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def thighs(self, ctx: Context):
        url = await boobbot(ctx.session, "thighs")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Tiny girls")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def tiny(self, ctx: Context):
        url = await boobbot(ctx.session, "tiny")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Porn with toys")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def toys(self, ctx: Context):
        url = await boobbot(ctx.session, "toys")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Traps")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def traps(self, ctx: Context):
        url = await boobbot(ctx.session, "traps")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Valentines themed")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def vday(self, ctx: Context):
        url = await boobbot(ctx.session, "vday")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Christmas themed")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def xmas(self, ctx: Context):
        url = await boobbot(ctx.session, "xmas")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Hentai: Boys' love")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def yaoi(self, ctx: Context):
        url = await boobbot(ctx.session, "yaoi")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

    @commands.command(description="Furry images")
    @checks.is_nsfw()
    @checks.custom_bot_has_permissions(embed_links=True)
    async def yiff(self, ctx: Context):
        url = await boobbot(ctx.session, "yiff")
        em = await self.boobbot_embed(ctx)
        em.set_image(url=url)
        em.description += f"**Image URL:** [Click Here]({url})"
        await ctx.reply(embed=em)

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
    #     await ctx.reply(embed=em)
    #
    # @nneko.command(name="ngif", description="Neko gifs")
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def nneko_ngif(self, ctx):
    #     url = await nekos(ctx.session, "nsfw_neko_gif")
    #     em = await self.nekos_embed(ctx)
    #     em.set_image(url=url)
    #     em.description += f"**Image URL:** [Click Here]({url})"
    #     await ctx.reply(embed=em)

    # TODO: SFW image commands
    # @neko.command(name="")
    # async def neko_sfw(self, ctx):
    #     """SFW Nekos"""
    #     url = await self.make_embed(ctx, "neko", "neko")
    #     await ctx.reply(embed=em)
    #
    # @neko.command(name="gif")
    # async def neko_gif(self, ctx):
    #     """SFW Neko gifs"""
    #     url = await self.make_embed(ctx, "neko", "ngif")
    #     await ctx.reply(embed=em)
    #
    # @neko.command(name="")
    # async def neko_kitsune(self, ctx):
    #     """SFW fox girls"""
    #     url = await self.make_embed(ctx, "neko", "fox_girl")
    #     await ctx.reply(embed=em)


def setup(bot):
    bot.add_cog(NSFW(bot))
