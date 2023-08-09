import os
import random
from io import BytesIO
from typing import Optional

import discord
from PIL import Image
from _decimal import Decimal, ROUND_HALF_UP
from discord.ext import commands

from bot import Bot
from utils.ctx import Context
from utils.functions.api import weeb


async def ship(session, avatar_1, avatar_2):
    path = "utils/assets/ship/"
    background = Image.new("RGBA", (600, 200), (0, 0, 0, 0))
    avatar_1 = Image.open(BytesIO(await (await session.get(str(avatar_1))).read())).resize((200, 200),
                                                                                           Image.LANCZOS).convert(
        "RGBA")
    avatar_2 = Image.open(BytesIO(await (await session.get(str(avatar_2))).read())).resize((200, 200),
                                                                                           Image.LANCZOS).convert(
        "RGBA")
    heart = Image.open(path + random.choice(list(os.listdir(path)))).convert("RGBA")
    background.paste(avatar_1, (0, 0), avatar_1)
    background.paste(heart, (201, 0), heart)
    background.paste(avatar_2, (401, 0), avatar_2)
    temp_image = BytesIO()
    background.save(temp_image, "PNG")
    temp_image.seek(0)
    return temp_image

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_group(name="social")
    async def social(self, ctx):
        return

    @staticmethod
    def draw_meter():
        random_integer = random.randint(0, 100)
        love = Decimal(str(random_integer / 10)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        love_emoji = "❤"
        empty_bar = "🖤"
        if random_integer == 0:
            empty_bar = "💔"
            love_message = "That's not good... maybe delete this and try again before they see?"
        elif random_integer <= 15:
            love_message = "That's a yikes.."
        elif random_integer <= 30:
            love_message = "Maybe in the future?"
        elif random_integer <= 45:
            love_message = "I mean this is the perfect range for friends?"
        elif random_integer <= 60:
            love_message = "Maybe try talking more?"
        elif random_integer == 69:
            love_emoji = "😏"
            love_message = "That's the sex number *wink wonk*"
        elif random_integer <= 75:
            love_message = "Best friends, stay as best friends."
        elif random_integer <= 90:
            love_message = "Give it a go, you're made for each other!"
        elif random_integer <= 99:
            love_message = "I ship it!"
        else:
            love_emoji = "💛"
            love_message = "Go get married! I hope I'm invited ❤"

        bar = "".join(love_emoji if i < love else empty_bar for i in range(10))

        return f"**Love meter:** {bar} **{random_integer}%**\n**{love_message}**"

    @social.command(name="ship", description="Ship your friends!")
    async def ship(self, ctx: Context, lover1: discord.Member, lover2: Optional[discord.Member]):
        lover2 = lover2 or ctx.author
        name1 = lover1.global_name[:-round(len(lover1.global_name) / 2)] + lover2.global_name[-round(len(lover2.global_name) / 2):]
        name2 = lover2.global_name[:-round(len(lover2.global_name) / 2)] + lover1.global_name[-round(len(lover1.global_name) / 2):]
        desc = f"**{ctx.author.mention} ships {lover1.mention} and {lover2.mention}!**\n\n " \
               f"Ship names: __**{name1}**__ or __**{name2}**__\n\n " \
               f"{self.draw_meter()}"
        em = discord.Embed(color=discord.Color.random(), description=desc)
        em.set_author(name="Lovely shipping!")
        em.set_image(url='attachment://ship.png')
        file = await ship(self.bot.session, lover1.avatar.with_static_format("png").url, lover2.avatar.with_static_format("png").url)
        await ctx.reply(file=discord.File(fp=file, filename="ship.png"), embed=em)

    @social.command(description="Bite people!")
    async def bite(self, ctx: Context, user: discord.Member):
        if user == ctx.author:
            return await ctx.send_error("Sorry but I cannot let you do that to yourself!")
        desc = f"{user.mention} was bitten by {ctx.author.mention}!"
        em = discord.Embed(color=0xaffaff, description=desc)
        em.set_image(url=await weeb(ctx.session, "bite"))
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Social(bot))
