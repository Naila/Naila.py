from discord import Embed, Streaming, CategoryChannel
from discord.ext.commands import Cog, group, guild_only

from bot import Bot
from config import config
from modules.Cogs.PrivateVC import DB as PrivateVCDB
from utils.checks import checks
from utils.ctx import Context
from utils.functions import errors
from utils.functions.prefix import Prefixes


class Settings(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @group(aliases=["bset"], description="Manage the settings for the bot", hidden=True)
    @checks.is_owner()
    async def botsettings(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    # TODO: Add list and add/remove commands
    @botsettings.group(name="status")
    async def botsettings_status(self, ctx: Context):
        if ctx.invoked_subcommand:
            return
        em = Embed()
        msg = ""
        for presence in config.presences:
            msg += f"{ctx.emojis('status.' + str(presence['status']))}"
            if presence["activity"]["type"] == Streaming:
                msg += f"{ctx.emojis('status.streaming')}" \
                       f" **Streaming** [{presence['activity']['text']}]({presence['activity']['url']})\n"
            else:
                prefix = str(presence['activity']['prefix']).split(".")[-1].capitalize()
                msg += f" **{prefix}** {presence['activity']['text']}\n"
        em.description = msg
        await ctx.reply(embed=em)

    @group(aliases=["gset"], description="Manage the settings for this guild")
    @guild_only()
    @checks.admin()
    async def guildsettings(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @guildsettings.group(name="privatevc", aliases=["pvc"], description="Private VC management")
    @checks.admin()
    async def gset_privatevc(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @gset_privatevc.command(name="category", aliases=["cat"], description="Set the Private VC category")
    async def gset_privatevc_category(self, ctx: Context, *, category: CategoryChannel):
        if category.guild != ctx.guild:
            return await ctx.send_error("Category must be in this guild!")
        vc = await category.create_voice_channel("Join for a private VC")
        await PrivateVCDB.set_settings(self.bot, ctx.guild, category, vc)
        await ctx.reply("Done!")

    @gset_privatevc.command(name="toggle", description="Toggle Private VC functionality")
    async def gset_privatevc_toggle(self, ctx: Context):
        settings = await PrivateVCDB.settings(self.bot, ctx.guild)
        if not settings["category_id"]:
            return await ctx.send_error("You must set a category before you toggle Private VCs!")
        status = await PrivateVCDB.toggle(self.bot, ctx.guild)
        if status:
            return await ctx.reply("I have enabled Private VCs!")
        await ctx.reply("I have disabled Private VCs!")

    @guildsettings.group(name="prefix", description="Prefix management")
    @checks.admin()
    async def gset_prefix(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @gset_prefix.command(name="add", description="Add a prefix")
    @checks.bot_has_permissions(embed_links=True)
    async def gset_prefix_add(self, ctx: Context, prefix: str):
        try:
            await Prefixes.add(ctx, prefix)
        except errors.PrefixTooLong:
            return await ctx.send_error("That prefix is too long! Prefix must be no more than 10 characters in length.")
        except errors.TooManyPrefixes:
            return await ctx.send_error("This guild already has 10 custom prefixes, remove some before adding more.")
        except errors.DuplicatePrefix:
            return await ctx.send_error("This prefix already exists here or is a default prefix!")
        await ctx.reply(
            embed=Embed(
                color=await ctx.guildcolor(),
                description=f"Prefix `{prefix}` added! Current prefixes:\n{await Prefixes.list(ctx)}"
            ).set_author(name=f"Prefix added in {ctx.guild.name}")
        )

    @gset_prefix.command(name="remove", description="Remove a prefix")
    @checks.bot_has_permissions(embed_links=True)
    async def gset_prefix_remove(self, ctx: Context, prefix):
        try:
            await Prefixes.remove(ctx, prefix)
        except errors.PrefixNotFound:
            return await ctx.send_error("That prefix could not be found, please try again!")
        await ctx.reply(
            embed=Embed(
                color=await ctx.guildcolor(),
                description=f"Prefix `{prefix}` removed! Current prefixes:\n{await Prefixes.list(ctx)}"
            ).set_author(name=f"Prefix removed in {ctx.guild.name}")
        )


def setup(bot):
    bot.add_cog(Settings(bot))
