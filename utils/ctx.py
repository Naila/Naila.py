from discord import Embed
import yaml
from dictor import dictor
from discord.ext.commands import Context as DefaultContext

from modules.Cogs.Help import command_signature
from utils.functions.errors import TranslationError


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

    @staticmethod
    def translator(path: str, key: str, **kwargs) -> str:
        lang = "en_US"  # Get users language
        # TODO: Cache strings?
        full_path = f"utils/assets/locales/{lang}/bot/{path}.yml"
        try:
            with open(full_path, "r") as file:
                strings = yaml.safe_load(file)
        except FileNotFoundError:
            raise TranslationError("Invalid path provided")

        string = dictor(strings, key)
        if not string:
            raise TranslationError("Invalid key provided")

        try:
            string = string.format(**kwargs)
        except KeyError:
            raise TranslationError("Invalid kwargs provided")

        return string

    async def guildcolor(self):
        if not self.guild:
            return self.bot.color
        return await self.pool.fetchval("SELECT color FROM guilds WHERE guild_id=$1", self.guild.id)

    def emojis(self, emoji: str):
        with open("config/emojis.yml", "r") as emojis:
            emojis = yaml.safe_load(emojis)
        return self.bot.get_emoji(dictor(emojis, emoji))

    async def embed(self, footer_text: str = None, embed_dict: dict = None) -> Embed:
        footer = str(self.author)
        if embed_dict:
            em = Embed().from_dict(embed_dict)
            if em.footer.text != Embed.Empty:
                footer_text = em.footer.text
        else:
            em = Embed()
        em.color = await self.guildcolor()
        if footer_text:
            footer += f" • {footer_text}"
        em.set_footer(icon_url=self.author.avatar_url_as(static_format="png"), text=footer)
        return em

    async def missing_argument(self):
        prefix = self.prefix.replace(self.bot.user.mention, '@' + self.bot.user.display_name)
        command = self.invoked_subcommand or self.command
        em = Embed(color=self.bot.error_color)
        em.title = "Missing required argument ❌"
        em.description = f"{prefix}{command.qualified_name} {command_signature(command)}\n{command.description}"
        await self.reply(embed=em)

    async def send_error(self, content):
        em = Embed(color=self.bot.error_color, title="Error ❌")
        em.description = str(content)
        await self.reply(embed=em)

    async def bad_argument(self, content):
        em = Embed(color=self.bot.error_color, title="Invalid argument ❌")
        em.description = str(content)
        await self.reply(embed=em)

    # def handle_file(self, file_path: str, path: str = None, **kwargs) -> dict:
    #     with open(file_path, "r") as file:
    #         if file_path.endswith("json"):
    #             data = json.load(file)
    #         else:
    #             data = yaml.safe_load(file)
    #         data = dictor(data, path)
    #
    #     def sub_val(string: str) -> str:
    #         string = string.format(emojis=self.emoji_dict, **kwargs)
    #         if not string.startswith("#!/"):
    #             return string
    #
    #         data_path = string[3:].split("/")
    #         return reduce(dict.__getitem__, data_path, data)
    #
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
