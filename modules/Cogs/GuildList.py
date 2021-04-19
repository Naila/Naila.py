import discord
from discord.ext import commands
from discord.ext.commands import BucketType

from bot import Bot
from config import config
from utils.ctx import Context
from utils.functions.time import get_relative_delta


class GuildList(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.command()
    @commands.cooldown(1, 10800, BucketType.guild)
    async def bump(self, ctx: Context):
        con = await self.bot.pool.acquire()
        guild = await con.fetchrow("SELECT * FROM guildlist_guilds WHERE guild_id=$1", ctx.guild.id)
        if not guild:
            await self.bot.pool.release(con)
            return await ctx.reply("This guild is not listed!")

        nsfw = await con.fetchrow("SELECT * FROM guildlist_guildtags WHERE guild_pk=$1 AND tag_pk=1", guild["id"])
        await self.bot.pool.release(con)

        home: discord.Guild = self.bot.get_guild(294505571317710849)
        out_ch: discord.TextChannel = home.get_channel(770387196388573195 if nsfw else 770387091774767114)
        em = discord.Embed(
            color=await ctx.guildcolor(),
            description=guild["description"] if guild["description"] else guild["brief"]
        )
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
        em.add_field(name="Invite:", value=guild["invite"], inline=False)
        await out_ch.send(embed=em)
        emb = discord.Embed(
            color=self.bot.color,
            description=f"You have successfully bumped {ctx.guild}!\n"
                        f"To view the bump join: {config.support_invite}\n"
                        f"You can bump this server again in 3 hours."
        ).set_author(
            name="Naila's Server Listing",
            icon_url=ctx.guild.me.avatar_url
        ).set_footer(
            text=f"Bumped by {ctx.author}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=emb)


def setup(bot):
    bot.add_cog(GuildList(bot))
