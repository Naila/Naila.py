import asyncio
import re

from discord import Embed, Streaming, Message, Reaction, User, TextChannel, Invite, Guild, CategoryChannel
from discord.ext.commands import Cog, group, guild_only, cooldown, BucketType

from bot import Bot
from config import config
from utils.checks import checks
from utils.ctx import Context
from modules.Cogs.PrivateVC import DB as PrivateVCDB
from utils.functions import errors
from utils.functions.prefix import Prefixes
from utils.functions.time import get_relative_delta


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

    @guildsettings.group(name="listing")
    async def gset_listing(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @gset_listing.command(name="add")
    @cooldown(1, 30, BucketType.guild)
    @checks.bot_has_permissions(add_reactions=True, create_instant_invite=True)
    async def gset_listing_add(self, ctx: Context):
        con = await self.bot.pool.acquire()
        guild = await con.fetchrow("SELECT * FROM guildlist_guilds WHERE guild_id=$1", ctx.guild.id)
        await self.bot.pool.release(con)
        if guild:
            return await ctx.reply("This guild is already listed!")

        def check(m: Message):
            return m.channel == ctx.channel and m.author == ctx.author

        def rcheck(r: Reaction, u: User):
            return u.id == ctx.author.id and str(r.emoji) in ["✅", "❌"]

        msg = await ctx.reply("This will add your server to a public list, do you wish to continue?")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=rcheck)
        except asyncio.TimeoutError:
            return ctx.reply("Timed out.")
        if str(reaction.emoji) == "❌":
            return await ctx.reply("Okay, cancelled!")

        data = {}
        await ctx.reply(
            "Okay, lets continue then. What channel would you like people to join when invited?"
            " Simply mention the channel.\n\nThe info given during setup CAN be changed later!"
        )
        while True:
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                return await ctx.reply("Timed out.")
            resp = response.content.lower()
            if not re.match(r"<#[0-9]+>", resp):
                await ctx.reply("Mention the channel please!")
            else:
                ch: TextChannel = ctx.guild.get_channel(int(resp.strip("<#>")))
                if not ch:
                    await ctx.reply("Invalid channel!")
                elif not ctx.guild.me.permissions_in(ch).create_instant_invite:
                    await ctx.reply("I don't have permissions to create an invite in this channel!")
                else:
                    invite: Invite = await ch.create_invite(reason="[ Guild List ] This invite will be used!")
                    data["invite"] = invite.url
                    await ctx.reply(f"The invite {invite.url} was created and will be used for listing purposes!")
                    break
            if not response:
                return await ctx.reply("Timed out.")
        await ctx.reply(
            "Is this guild NSFW focused? (yes or no)"
            " You **MUST** say yes if anything public facing (icon, invite splash, banner, etc) are NSFW!\n\n"
            "You will have the opportunity to add other tags to the server later, this is important for listing!"
        )
        while True:
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                return await ctx.reply("Timed out.")
            resp = response.content.lower()
            if resp not in ["yes", "no"]:
                await ctx.reply("Invalid response!")
            else:
                if resp == "yes":
                    data["nsfw"] = True
                elif resp == "no":
                    data["nsfw"] = False
                break
            if not response:
                return await ctx.reply("Timed out.")
        await ctx.reply("Give us a brief description of this guild, max 140 characters!")
        while True:
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                return await ctx.reply("Timed out.")
            if len(response.content) > 140:
                await ctx.reply("Brief description must be shorter!")
            else:
                data["brief"] = response.content
                break
            if not response:
                return await ctx.reply("Timed out.")
        await ctx.reply("Now your long description! Just say \"no\" if you don't want to provide this atm!")
        while True:
            try:
                response = await ctx.bot.wait_for("message", timeout=300, check=check)
            except asyncio.TimeoutError:
                return await ctx.reply("Timed out.")
            if response.content.lower() == "no":
                data["desc"] = None
            else:
                data["desc"] = response.content
            break

        msg = await ctx.reply("Listing..")
        home: Guild = self.bot.get_guild(294505571317710849)
        out_ch: TextChannel = home.get_channel(770386941677404211 if data["nsfw"] else 770386909972660274)
        em = Embed(color=await ctx.guildcolor(), description=data["desc"] if data["desc"] else data["brief"])
        em.set_author(name=ctx.guild.name)
        em.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=1024))
        em.set_image(url=ctx.guild.banner_url)
        em.add_field(
            name="Information:",
            value=f"**Owner:** {ctx.guild.owner.mention} ({ctx.guild.owner})\n"
                  f"**Members:** {ctx.guild.member_count:,}\n"
                  f"**Features:** {', '.join([x.replace('_', ' ').capitalize() for x in ctx.guild.features])}\n"
                  f"**Created:** {get_relative_delta(ctx.guild.created_at, True, True)}"
        )
        em.add_field(name="Invite:", value=data["invite"], inline=False)
        mesg = await out_ch.send(embed=em)
        con = await self.bot.pool.acquire()
        await con.execute(
            "INSERT INTO guildlist_guilds(guild_id, brief, description, invite) VALUES($1, $2, $3, $4)",
            ctx.guild.id, data["brief"], data["desc"], data["invite"]
        )
        if data["nsfw"]:
            guild_pk = await con.fetchval("SELECT id FROM guildlist_guilds WHERE guild_id=$1", ctx.guild.id)
            tag_pk = await con.fetchval("SELECT id FROM guildlist_tags WHERE tag='NSFW'")
            await con.execute("INSERT INTO guildlist_guildtags (tag_pk, guild_pk) VALUES ($1, $2)", tag_pk, guild_pk)
        await self.bot.pool.release(con)
        await msg.edit(content=f"You can now find your guild listed at {mesg.jump_url} over at {config.support_invite}")

    @gset_listing.command(name="remove")
    @checks.bot_has_permissions(add_reactions=True)
    async def gset_listing_remove(self, ctx: Context):
        con = await self.bot.pool.acquire()
        guild = await con.fetchrow("SELECT * FROM guildlist_guilds WHERE guild_id=$1", ctx.guild.id)
        await self.bot.pool.release(con)
        if not guild:
            return await ctx.reply("This guild is not listed!")

        def rcheck(r: Reaction, u: User):
            return u.id == ctx.author.id and str(r.emoji) in ["✅", "❌"]

        msg = await ctx.reply("This will delete your server from our system, do you want to continue?")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=rcheck)
        except asyncio.TimeoutError:
            return ctx.reply("Timed out.")
        if str(reaction.emoji) == "❌":
            return await ctx.reply("Okay, cancelled!")

        con = await self.bot.pool.acquire()
        await con.execute("DELETE FROM guildlist_guildtags WHERE guild_pk=$1", guild["id"])
        await con.execute("DELETE FROM guildlist_guilds WHERE guild_id=$1", ctx.guild.id)
        await self.bot.pool.release(con)
        await ctx.reply("Removed!")

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
