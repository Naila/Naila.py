from io import BytesIO
import json

import discord
from discord.ext import commands

from utils.checks import checks
from utils.functions.archive import format_data

__author__ = "Kanin"
__date__ = "12/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @staticmethod
    def predicate(message):
        return message.type == discord.MessageType.default

    # @commands.command()
    # async def upload(self, ctx):
    #     """{"user": [], "bot": []}"""
    #     data = FormData()
    #     data.add_field("file", open("utils/assets/ship/heart1.png", "rb"), filename="test/testing.png")
    #     async with ctx.session.post(
    #         url="https://cdn.naila.bot/upload/archive",
    #         headers={"Authorization": "6c878e5f-6f10-4502-abff-be50cdf6e6f4"},
    #         data=data
    #     ) as resp:
    #         if resp.status != 204:
    #             resp = await resp.json()
    #             return await ctx.send(resp)
    #         await ctx.send("Uploaded!")

    @checks.is_owner()
    @commands.command(description="TEST: Archive messages")
    async def archive(self, ctx, messages: int):
        """{"user": [], "bot": []}"""
        if messages > 1000:
            return await ctx.send_error("lol no")
        message_list = []
        async for message in ctx.channel.history(limit=messages).filter(self.predicate):
            message_list.append(message)
        message_list = message_list[::-1]
        data = await format_data(ctx, message_list)
        data["channel_name"] = ctx.channel.name
        # df = BytesIO()
        # df.write(json.dumps(data, indent=4).encode("utf8"))
        # df.seek(0)
        # await ctx.send(file=discord.File(df, filename="data.json"))
        data = json.loads(json.dumps(data).encode("utf8"))
        resp = await self.session.post(
            "https://archive.naila.bot",
            json=data
        )
        if resp.status != 200:
            return await ctx.send_error("Something went wrong")
        resp = await resp.text(encoding="utf8")
        file = BytesIO()
        file.write(resp.encode("utf8"))
        file.seek(0)
        await ctx.send(file=discord.File(file, filename=f"{ctx.channel.name}.html"))

    @checks.is_owner()
    @commands.command(description="An embed")
    async def embed(self, ctx):
        chan = "<#483061332766097419>"
        em = discord.Embed(description=chan, title=chan)
        em.set_author(name=chan)
        em.add_field(name=chan, value=chan)
        em.set_footer(text=chan)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Testing(bot))
