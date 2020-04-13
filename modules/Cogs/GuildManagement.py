from discord.ext import commands
from utils.database.GuildSettings import Prefixes
from utils.functions import errors
import discord
from utils.checks import checks

__author__ = "Kanin"
__date__ = "11/22/2019"
__copyright__ = "Copyright 2019, Naila"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class GuildManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(aliases=["gset"], description="Manage the settings for this guild")
    async def guildset(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @checks.admin()
    @guildset.group(description="Prefix management")
    async def prefix(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @prefix.command(name="add", description="Add a prefix")
    @checks.custom_bot_has_permissions(embed_links=True)
    @checks.custom_user_has_permissions(manage_guild=True)
    async def prefix_add(self, ctx, prefix: str):
        try:
            await Prefixes(ctx).add(prefix)
        except errors.PrefixTooLong:
            return await ctx.send_error("That prefix is too long! Prefix must be no more than 10 characters in length.")
        except errors.TooManyPrefixes:
            return await ctx.send_error("This guild already has 10 custom prefixes, remove some before adding more.")
        except errors.DuplicatePrefix:
            return await ctx.send_error("This prefix already exists here or is a default prefix!")
        await ctx.send(
            embed=discord.Embed(
                color=await ctx.guildcolor(),
                description=f"Prefix `{prefix}` added! Current prefixes:\n{await Prefixes(ctx).list()}"
            ).set_author(name=f"Prefix added in {ctx.guild.name}")
        )

    @prefix.command(name="remove", description="Remove a prefix")
    @checks.custom_bot_has_permissions(embed_links=True)
    @checks.custom_user_has_permissions(manage_guild=True)
    async def prefix_remove(self, ctx, prefix):
        try:
            await Prefixes(ctx).remove(prefix)
        except errors.PrefixNotFound:
            return await ctx.send_error("That prefix could not be found, please try again!")
        await ctx.send(
            embed=discord.Embed(
                color=await ctx.guildcolor(),
                description=f"Prefix `{prefix}` removed! Current prefixes:\n{await Prefixes(ctx).list()}"
            ).set_author(name=f"Prefix removed in {ctx.guild.name}")
        )


def setup(bot):
    bot.add_cog(GuildManagement(bot))
