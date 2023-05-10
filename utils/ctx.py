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

    @property
    def pool(self):
        return self.bot.pool

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
        if embed_dict:
            em = discord.Embed().from_dict(embed_dict)
            if em.footer.text is not None:
                footer_text = em.footer.text
        else:
            em = discord.Embed()
        if footer_text:
            footer += f" • {footer_text}"
        em.set_footer(icon_url=self.author.avatar_url_as(static_format="png"), text=footer)
        return em

    # async def missing_argument(self):
    #     prefix = self.prefix.replace(self.bot.user.mention, '@' + self.bot.user.display_name)
    #     command = self.invoked_subcommand or self.command
    #     em = Embed(color=self.bot.error_color)
    #     em.title = "Missing required argument ❌"
    #     em.description = f"{prefix}{command.qualified_name} {command_signature(command)}\n{command.description}"
    #     await self.reply(embed=em)

    async def send_error(self, content, ephemeral: bool = False):
        em = discord.Embed(color=discord.Color.red(), title="Error ❌")
        em.description = str(content)
        return await self.send(embed=em, reference=self.message if self.interaction else None, ephemeral=ephemeral)
    #
    # async def bad_argument(self, content):
    #     em = Embed(color=self.bot.error_color, title="Invalid argument ❌")
    #     em.description = str(content)
    #     await self.reply(embed=em)

    # def handle_file(self, file_path: str, path: str = None, **kwargs) -> dict:
    #     with open(file_path, "r") as file:
    #         if file_path.endswith("json"):
    #             data = json.load(file)
    #         else:
    #             data = yaml.safe_load(file)
    #         data = dictor(data, path)

    #     def sub_val(string: str) -> str:
    #         string = string.format(emojis=self.emoji_dict, **kwargs)
    #         if not string.startswith("#!/"):
    #             return string
    #
    #         data_path = string[3:].split("/")
    #         return reduce(dict.__getitem__, data_path, data)

    #     def recursive_search(obj: Union[dict, list], emojis: bool) -> None:
    #         def handle_element(el):
    #             if isinstance(el, str):
    #                 return sub_val(el)
    #             elif isinstance(el, int):
    #                 if emojis:
    #                     return str(self.bot.get_emoji(obj[sub_key]) or 'UNKNOWN_EMOJI')
    #             return el
    #
    #         if isinstance(obj, list):
    #             for idx, element in enumerate(obj):
    #                 if isinstance(element, (dict, list)):
    #                     recursive_search(element, emojis)
    #                 else:
    #                     obj[idx] = handle_element(obj[idx])
    #         elif isinstance(obj, dict):
    #             for sub_key in obj:
    #                 if isinstance(obj[sub_key], (dict, list)):
    #                     recursive_search(obj[sub_key], emojis)
    #                 else:
    #                     obj[sub_key] = handle_element(obj[sub_key])
    #
    #     recursive_search(data, emojis="emojis.yml" in file_path)
    #     return data
