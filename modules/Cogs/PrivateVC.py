import asyncio
from datetime import datetime

from discord import Embed, TextChannel, VoiceChannel, PermissionOverwrite, Member, Guild, VoiceState, CategoryChannel
from discord.ext.commands import Cog, group, cooldown, BucketType

from bot import Bot
from utils.ctx import Context


class DB:

    @staticmethod
    async def check(bot: Bot, guild: Guild):
        data = await bot.pool.fetch("SELECT * FROM guildsettings_privatevc WHERE guild_id=$1", guild.id)
        if not data:
            await bot.pool.execute("INSERT INTO guildsettings_privatevc (guild_id) VALUES ($1) ON CONFLICT DO NOTHING",
                                   guild.id)
            bot.log.info(f"Added {guild.name} to the (guildsettings_privatevc) database")

    @staticmethod
    async def settings(bot: Bot, guild: Guild):
        await DB.check(bot, guild)
        settings = await bot.pool.fetchrow("SELECT * FROM guildsettings_privatevc WHERE guild_id=$1", guild.id)
        return settings

    @staticmethod
    async def set_settings(bot: Bot, guild: Guild, category: CategoryChannel, voice: VoiceChannel):
        await DB.check(bot, guild)
        await bot.pool.execute(
            "UPDATE guildsettings_privatevc SET category_id=$1, default_vc_id=$2 WHERE guild_id=$3",
            category.id,
            voice.id,
            guild.id
        )

    @staticmethod
    async def reset_settings(bot: Bot, guild: Guild):
        await bot.pool.execute(
            "UPDATE guildsettings_privatevc SET "
            "category_id=null, default_vc_id=null, vc_enabled=false WHERE guild_id=$1",
            guild.id
        )

    @staticmethod
    async def toggle(bot: Bot, guild: Guild):
        settings = await DB.settings(bot, guild)
        await bot.pool.execute(
            "UPDATE guildsettings_privatevc SET vc_enabled = NOT vc_enabled WHERE guild_id=$1",
            guild.id
        )
        return not settings["vc_enabled"]

    @staticmethod
    async def add_data(bot: Bot, user: Member, guild: Guild, tc: TextChannel, vc: VoiceChannel):
        await bot.pool.execute(
            "INSERT INTO data_privatevc (user_id, guild_id, textchannel_id, voicechannel_id, time_created) VALUES"
            " ($1, $2, $3, $4, $5)"
            " ON CONFLICT DO NOTHING",
            user.id,
            guild.id,
            tc.id,
            vc.id,
            datetime.utcnow()
        )

    @staticmethod
    async def fetch_data(bot: Bot, user: Member):
        data = await bot.pool.fetchrow(
            "SELECT * FROM data_privatevc WHERE user_id=$1 AND time_removed IS NULL",
            user.id
        )
        return data

    @staticmethod
    async def update_data(bot: Bot, user: Member):
        await bot.pool.execute(
            "UPDATE data_privatevc SET time_removed=$1 WHERE user_id=$2 AND time_removed IS NULL",
            datetime.utcnow(),
            user.id,
        )


class PrivateVC(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.queued = []

    @group(aliases=["pvc"])
    @cooldown(5, 30, BucketType.user)
    async def privatevc(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @privatevc.command(name="add")
    async def privatevc_add(self, ctx: Context, *, member: Member):
        data = await DB.fetch_data(self.bot, ctx.author)
        if not data:
            return await ctx.send_error("You don't have a private Voice Channel!")
        tc: TextChannel = ctx.guild.get_channel(data["textchannel_id"])
        vc: VoiceChannel = ctx.guild.get_channel(data["voicechannel_id"])
        if not tc:
            return await ctx.send_error("You must run this in the guild your channel is in!")
        if ctx.channel.id != data["textchannel_id"]:
            return await ctx.send_error("You must use this command in your private channel!")
        if member.permissions_in(tc).read_messages:
            return await ctx.send_error("That member already has access!")
        overwrites = {
            **tc.overwrites,
            member: PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
        }
        await tc.edit(overwrites=overwrites)
        await vc.edit(overwrites=overwrites)
        await ctx.reply(f"{member.mention} now has access to your channels!")

    @privatevc.command(name="remove")
    async def privatevc_remove(self, ctx: Context, *, member: Member):
        data = await DB.fetch_data(self.bot, ctx.author)
        if not data:
            return await ctx.send_error("You don't have a private Voice Channel!")
        tc: TextChannel = ctx.guild.get_channel(data["textchannel_id"])
        vc: VoiceChannel = ctx.guild.get_channel(data["voicechannel_id"])
        if not tc:
            return await ctx.send_error("You must run this in the guild your channel is in!")
        if ctx.channel.id != data["textchannel_id"]:
            return await ctx.send_error("You must use this command in your private channel!")
        if member.permissions_in(tc).administrator:
            return await ctx.send_error("That user is an Administrator... we can't remove them!")
        if member == ctx.guild.me:
            return await ctx.send_error("You can't remove me...")
        if not member.permissions_in(tc).read_messages:
            return await ctx.send_error("That member doesn't have access!")
        overwrites = {
            **tc.overwrites,
            member: PermissionOverwrite(read_messages=False, send_messages=False, connect=False)
        }
        await tc.edit(overwrites=overwrites)
        await vc.edit(overwrites=overwrites)
        await ctx.reply(f"{member.mention} no longer has access to your channels!")

    async def clear_data(self, member: Member, guild: Guild):
        if member.id in self.queued:
            return
        data = await DB.fetch_data(self.bot, member)
        if not data:
            return
        self.queued.append(member.id)
        await asyncio.sleep(10)
        if member.voice is not None and member.voice.channel.id == data["voicechannel_id"]:
            self.queued.remove(member.id)
            return
        vc: VoiceChannel = guild.get_channel(data["voicechannel_id"])
        tc: TextChannel = guild.get_channel(data["textchannel_id"])
        await vc.delete(reason="User left private vc")
        await tc.delete(reason="User left private vc")
        await DB.update_data(self.bot, member)
        self.queued.remove(member.id)

    @Cog.listener()
    async def on_voice_state_update(
            self, member: Member, before: VoiceState, after: VoiceState
    ):
        guild: Guild = member.guild
        if after.channel is not None:
            settings = await DB.settings(self.bot, guild)
            data = await DB.fetch_data(self.bot, member)
            if data:
                if after.channel.id == data["voicechannel_id"]:
                    return
                return await self.clear_data(member, guild)
            if settings["vc_enabled"] and after.channel.id == settings["default_vc_id"]:
                category: CategoryChannel = guild.get_channel(settings["category_id"])
                if not category:
                    await DB.reset_settings(self.bot, guild)
                    return
                if member.bot:
                    return await member.move_to(None, reason="Bot joined Private VC")
                overwrites = {
                    guild.default_role: PermissionOverwrite(read_messages=False),
                    member: PermissionOverwrite(read_messages=True, send_messages=True, connect=True),
                    guild.me: PermissionOverwrite(
                        read_messages=True, send_messages=True, embed_links=True, manage_permissions=True
                    )
                }
                vc: VoiceChannel = \
                    await category.create_voice_channel(f"{member.name}'s channel", overwrites=overwrites)
                tc: TextChannel = \
                    await category.create_text_channel(f"{member.name}s-channel", overwrites=overwrites, nsfw=True)
                await DB.add_data(self.bot, member, guild, tc, vc)
                await member.move_to(vc, reason="User created private channel")
                info = f"To add someone to your channel use: `n!pvc add <Member>`\n\n" \
                       f"To remove someone from your channel use: `n!pvc remove <Member>`\n\n" \
                       f"Leave your voice channel and after 10 seconds your channels will be closed."
                em = Embed(color=self.bot.color, description=info)
                em.set_author(name="Welcome to your private channel!")
                return await tc.send(content=member.mention, embed=em)
        await self.clear_data(member, guild)


def setup(bot):
    bot.add_cog(PrivateVC(bot))
