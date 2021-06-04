import os
from datetime import datetime

from discord import Embed, Webhook, AsyncWebhookAdapter
from discord.ext.commands import Cog

from bot import Bot


class Guilds(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild):
        bots = 0
        users = 0
        for user in guild.members:
            if user.bot:
                bots += 1
            else:
                users += 1
        em = Embed(color=self.bot.color)
        em.set_author(name=guild.name)
        em.set_thumbnail(url=guild.icon_url_as(static_format="png", size=1024))
        em.add_field(
            name="Guild Info:",
            value=f"**Owner:** {guild.owner.mention} ({guild.owner})\n"
                  f"**Users | Bots:** {users:,} | {bots:,} ({round(bots / len(guild.members) * 100)}%)"
        )
        em.add_field(
            name="Bot Stats:",
            value=f"**Guilds:** {len(self.bot.guilds):,}\n**Users:** {len(self.bot.users):,}",
            inline=False
        )
        em.set_footer(text=str(guild.id))
        em.timestamp = datetime.utcnow()
        webhook = Webhook.from_url(os.getenv("GUILDS"), adapter=AsyncWebhookAdapter(self.bot.session))
        await webhook.send(
            embed=em,
            username="Joined a guild",
            avatar_url=self.bot.user.avatar_url_as(static_format="png", size=1024)
        )

    @Cog.listener()
    async def on_guild_remove(self, guild):
        bots = 0
        users = 0
        for user in guild.members:
            if user.bot:
                bots += 1
            else:
                users += 1
        em = Embed(color=self.bot.error_color)
        em.set_author(name=guild.name)
        em.set_thumbnail(url=guild.icon_url_as(static_format="png", size=1024))
        em.add_field(
            name="Guild Info:",
            value=f"**Owner:** {guild.owner.mention} ({guild.owner})\n"
                  f"**Users | Bots:** {users:,} | {bots:,} ({round(bots / len(guild.members) * 100)}%)"
        )
        em.add_field(
            name="Bot Stats:",
            value=f"**Guilds:** {len(self.bot.guilds):,}\n**Users:** {len(self.bot.users):,}",
            inline=False
        )
        em.set_footer(text=str(guild.id))
        em.timestamp = datetime.utcnow()
        webhook = Webhook.from_url(os.getenv("GUILDS"), adapter=AsyncWebhookAdapter(self.bot.session))
        await webhook.send(
            embed=em,
            username="Left a guild",
            avatar_url=self.bot.user.avatar_url_as(static_format="png", size=1024)
        )


def setup(bot):
    bot.add_cog(Guilds(bot))
