import discord
from discord.ext import commands

from bot import Bot
from common.functions.database import database


class Database(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await database.add_user_bulk(guild.members)
        await database.add_guild(guild)
        await database.update_presence(guild, True)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await database.update_presence(guild, False)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.guild:
            await database.increment_guild(message.guild)
        await database.increment_user(message.author)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        await database.add_user(member)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if after.bot:
            return

        data = {}
        if before.name != after.name:
            data["username"] = after.name
        if before.global_name != after.global_name:
            data["display_name"] = after.global_name
        if before.avatar != after.avatar:
            data["avatar"] = after.avatar.key
        if data:
            await database.update_user(after, data)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        data = {}
        if before.name != after.name:
            data["name"] = after.name
        if before.icon != after.icon:
            data["icon"] = after.icon.key
        if before.owner != after.owner:
            data["owner_id"] = after.owner.id
        if data:
            await database.update_guild(after, data)
