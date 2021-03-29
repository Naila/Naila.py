import os

import discord
import httpx
from discord.ext import commands

from bot import Bot
from utils.checks import checks
from utils.ctx import Context

base_url = "https://sheri.bot/api/"


async def sheri_embed(ctx: Context):
    em = discord.Embed(color=await ctx.guildcolor(), description="**Website:** https://sheri.bot/\n")
    em.set_author(name="Images provided by Sheri Blossom", url="https://sheri.bot/")
    em.set_footer(text="If there's an issue with ANY image, please take it up with the provider.")
    return em


async def image_send(ctx: Context, endpoint: str):
    async with httpx.AsyncClient() as session:
        data = await session.get(url=base_url + endpoint, headers={"Authorization": os.getenv("SHERI"),
                                                                   "User-Agent": "Naila Discord Bot - By Kanin#0001"})
        if data.status_code != 200:
            return await ctx.send("Either the website is down or there is an internal error, Please contact support!")
        response = data.json()
        embed = await sheri_embed(ctx)
        embed.set_image(url=response['url'])
        embed.add_field(name="Issue with image?",
                        value="Report it to the sheri.bot using the below link\n"
                              f"{response['report_url']}")
        return await ctx.send(embed=embed)


class Sheri(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.group(name="sheri")
    async def sheri(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri.group(name="sfw")
    async def sheri_sfw(self, ctx: Context):
        """Shows Furry Commands that are SFW"""
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri_sfw.command(name="mur")
    async def sheri_sfw_mur(self, ctx: Context):
        """Shows Random SFW Furry Images"""
        await image_send(ctx, "mur")

    @sheri_sfw.command(name="boop")
    async def sheri_sfw_boop(self, ctx: Context):
        """Shows Random Furry Boop Images"""
        await image_send(ctx, "boop")

    @sheri_sfw.command(name="hug")
    async def sheri_sfw_hug(self, ctx: Context):
        """Shows Random Furry Hug Images"""
        await image_send(ctx, "hug")

    @sheri_sfw.command(name="kiss")
    async def sheri_sfw_kiss(self, ctx: Context):
        """Shows Random Furry Kiss Images"""
        await image_send(ctx, "kiss")

    @sheri_sfw.command(name="cuddle")
    async def sheri_sfw_cuddle(self, ctx: Context):
        """Shows Random Furry Cuddle Images"""
        await image_send(ctx, "cuddle")

    @sheri_sfw.command(name="paws")
    async def sheri_sfw_paws(self, ctx: Context):
        """Shows Random Furry paw Images"""
        await image_send(ctx, "paws")

    @sheri_sfw.command(name="blep")
    async def sheri_sfw_blep(self, ctx: Context):
        """Shows Random Furry blep Images"""
        await image_send(ctx, "blep")

    @checks.is_nsfw()
    @sheri.group(name="nsfw")
    async def sheri_nsfw(self, ctx: Context):
        """Shows Furry Commands that are NSFW"""
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @sheri_nsfw.command(name="yiff")
    async def sheri_nsfw_yiff(self, ctx: Context):
        """Shows Random NSFW Images from sheri.bot"""
        await image_send(ctx, "yiff")

    @sheri_nsfw.command(name="gif")
    async def sheri_nsfw_gif(self, ctx: Context):
        """Shows Random NSFW GIFs from sheri.bot"""
        await image_send(ctx, "gif")

    @sheri_nsfw.command(name="boobs")
    async def sheri_nsfw_boobs(self, ctx: Context):
        """Shows Random NSFW Furry Boobs from sheri.bot"""
        await image_send(ctx, "boob")

    @sheri_nsfw.command(name="booty")
    async def sheri_nsfw_booty(self, ctx: Context):
        """Shows Random NSFW Furry booty from sheri.bot"""
        await image_send(ctx, "booty")

    @sheri_nsfw.command(name="femboy")
    async def sheri_nsfw_femboy(self, ctx: Context):
        """Shows Random NSFW Furry Femboy from sheri.bot"""
        await image_send(ctx, "femboypresentation")


def setup(bot):
    bot.add_cog(Sheri(bot))
