# from datetime import datetime

import discord
# import json
import yaml
from discord.ext import commands
from dictor import dictor
# from typing import Union
# from functools import reduce
from modules.Cogs.Help import command_signature
# import pathlib

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class CustomContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.emoji_dict = self.handle_file("config/emojis.yml")

    @property
    def session(self):
        return self.bot.session

    @property
    def pool(self):
        return self.bot.pool

    @property
    def log(self):
        return self.bot.log

    async def guildcolor(self):
        if not self.guild:
            return self.bot.color
        return await self.pool.fetchval("SELECT color FROM guilds WHERE guild_id=$1", self.guild.id)

    def emojis(self, emoji: str):
        with open("config/emojis.yml", "r") as emojis:
            emojis = yaml.safe_load(emojis)
        return self.bot.get_emoji(dictor(emojis, emoji))

    # async def embed(self, footer_text: str = None, embed_dict: dict = None) -> discord.Embed:
    #     footer = str(self.author)
    #     if embed_dict:
    #         em = discord.Embed().from_dict(embed_dict)
    #         if em.footer.text != discord.Embed.Empty:
    #             footer_text = em.footer.text
    #     else:
    #         em = discord.Embed()
    #     em.color = await self.guildcolor()
    #     if footer_text:
    #         footer += f" • {footer_text}"
    #     em.set_footer(icon_url=self.author.avatar_url_as(static_format="png"), text=footer)
    #     return em
    #
    # async def respond(self, path: str, **kwargs):
    #     # will get language for guild
    #     response = self.handle_file("locales/en_US.json", path, **kwargs)
    #     em = await self.embed(embed_dict=response["embed"])
    #     print(em.to_dict())
    #     await self.send(content=response["content"] if "content" in response else None, embed=em)

    async def missing_argument(self):
        channel = self.channel
        prefix = self.prefix.replace(self.bot.user.mention, '@' + self.bot.user.display_name)
        command = self.invoked_subcommand if self.invoked_subcommand else self.command
        em = discord.Embed(color=self.bot.error_color)
        em.title = "Missing required argument ❌"
        em.description = f"{prefix}{command.qualified_name} {command_signature(command)}\n{command.description}"
        await channel.send(embed=em)

    async def send_error(self, content):
        channel = self.channel
        em = discord.Embed(color=self.bot.error_color, title="Error ❌")
        em.description = str(content)
        await channel.send(embed=em)

    async def bad_argument(self, content):
        channel = self.channel
        em = discord.Embed(color=self.bot.error_color, title="Invalid argument ❌")
        em.description = str(content)
        await channel.send(embed=em)

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
