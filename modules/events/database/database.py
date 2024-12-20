import discord
from discord.ext import commands

from bot import Bot
from common.functions.database import add_user, increment_user, update_user


class Database(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        await increment_user(message.author)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        await add_user(member)

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
            await update_user(after, data)
