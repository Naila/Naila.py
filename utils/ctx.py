# from datetime import datetime
import asyncio

import discord
# import json
import yaml
from dictor import dictor
from discord.ext import commands

# from typing import Union
# from functools import reduce
from modules.Cogs.Help import command_signature

# import pathlib


class _ContextDBAcquire:
    __slots__ = ('ctx', 'timeout')

    def __init__(self, ctx, timeout):
        self.ctx = ctx
        self.timeout = timeout

    def __await__(self):
        return self.ctx.db_acquire(self.timeout).__await__()

    async def __aenter__(self):
        await self.ctx.db_acquire(self.timeout)
        return self.ctx.db

    async def __aexit__(self, *args):
        await self.ctx.release()


class CustomContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = self.bot.pool
        self._db = None
        # self.emoji_dict = self.handle_file("config/emojis.yml")

    async def db_acquire(self, timeout):
        if self._db is None:
            self._db = await self.pool.acquire(timeout=timeout)
        return self._db

    def acquire(self, *, timeout=None):
        """Acquires a database connection from the pool. e.g. ::
            async with ctx.acquire():
                await ctx.db.execute(...)
        or: ::
            await ctx.acquire()
            try:
                await ctx.db.execute(...)
            finally:
                await ctx.release()
        """
        return _ContextDBAcquire(self, timeout)

    async def release(self):
        """Releases the database connection from the pool.
        Useful if needed for "long" interactive commands where
        we want to release the connection and re-acquire later.
        Otherwise, this is called automatically by the bot.
        """
        # from source digging asyncpg source, releasing an already
        # released connection does nothing

        if self._db is not None:
            await self.bot.pool.release(self._db)
            self._db = None

    @property
    def session(self):
        return self.bot.session

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

    async def prompt(self, message, *, timeout=60.0, delete_after=True, reacquire=True, author_id=None):
        """An interactive reaction confirmation dialog.
        Parameters
        -----------
        message: str
            The message to show along with the prompt.
        timeout: float
            How long to wait before returning.
        delete_after: bool
            Whether to delete the confirmation message after we're done.
        reacquire: bool
            Whether to release the database connection and then acquire it
            again when we're done.
        author_id: Optional[int]
            The member who should respond to the prompt. Defaults to the author of the
            Context's message.
        Returns
        --------
        Optional[bool]
            ``True`` if explicit confirm,
            ``False`` if explicit deny,
            ``None`` if deny due to timeout
        """

        if not self.channel.permissions_for(self.me).add_reactions:
            raise RuntimeError("Bot does not have Add Reactions permission.")

        fmt = f"{message}\n\nReact with ✅ to confirm or ❌ to deny."

        author_id = author_id or self.author.id
        msg = await self.send(fmt)

        confirm = None

        def check(payload):
            nonlocal confirm

            if payload.message_id != msg.id or payload.user_id != author_id:
                return False

            codepoint = str(payload.emoji)

            if codepoint == "✅":
                confirm = True
                return True
            if codepoint == "❌":
                confirm = False
                return True

            return False

        for emoji in ("✅", "❌"):
            await msg.add_reaction(emoji)

        if reacquire:
            await self.release()

        try:
            await self.bot.wait_for("raw_reaction_add", check=check, timeout=timeout)
        except asyncio.TimeoutError:
            confirm = None

        try:
            if reacquire:
                await self.acquire()

            if delete_after:
                await msg.delete()
        finally:
            return confirm
