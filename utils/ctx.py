import discord
import yaml
from dictor import dictor
from discord.ext.commands import Context as DefaultContext


class Context(DefaultContext):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    @property
    def log(self):
        return self.bot.log

    # async def guildcolor(self):
    #     if not self.guild:
    #         return self.bot.color
    #     return await self.pool.fetchval("SELECT color FROM guilds WHERE guild_id=$1", self.guild.id)

    def emojis(self, emoji: str):
        with open("config/emojis.yml", "r") as emojis:
            emojis = yaml.safe_load(emojis)
        return self.bot.get_emoji(dictor(emojis, emoji))

    async def embed(self, footer_text: str = None, embed_dict: dict = None) -> discord.Embed:
        footer = str(self.author)
        avatar = self.author.avatar if self.author.avatar else self.author.default_avatar
        if embed_dict:
            em = discord.Embed().from_dict(embed_dict)
            if em.footer.text is not None:
                footer_text = em.footer.text
        else:
            em = discord.Embed()
        if footer_text:
            footer += f" • {footer_text}"
        em.set_footer(icon_url=avatar.with_static_format("png"), text=footer)
        return em

    async def send_error(self, content, ephemeral: bool = False):
        em = discord.Embed(color=discord.Color.red(), title="Error ❌")
        em.description = str(content)
        return await self.send(embed=em, reference=self.message if self.interaction else None, ephemeral=ephemeral)
