import contextlib
import inspect
import io
import json
import os
import re
import textwrap
import time
import traceback
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from bot import Bot
from common.functions.text import options_to_string
from utils.checks import checks


ENV = {
    "contextlib": contextlib,
    "inspect": inspect,
    "io": io,
    "os": os,
    "re": re,
    "textwrap": textwrap,
    "time": time,
    "traceback": traceback,
    "BytesIO": io.BytesIO,
    "discord": discord
}


class Dev(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.env = ENV
        self.stdout = io.StringIO()

    async def do_eval(self, ctx, code):
        if code == "exit()":
            self.env = ENV
            return await ctx.send("```Reset history!```")

        env = {
            "message": ctx.message,
            "author": ctx.author,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "ctx": ctx,
            "self": self,
            "bot": self.bot
        }

        self.env.update(env)

        _code = \
            f"""
async def func():
    try:
        with contextlib.redirect_stdout(self.stdout):
{textwrap.indent(code, '            ')}
        if '_' in locals():
            if inspect.isawaitable(_):
                _ = await _
            return _
    finally:
        self.env.update(locals())
            """

        try:
            exec(_code, self.env)
            func = self.env['func']
            res = await func()

        except:
            res = traceback.format_exc()

        out, embed = self._format(code, res)
        try:
            await ctx.send(f"```py\n{out}```", embed=embed)
        except discord.HTTPException:
            data = io.BytesIO(out.encode('utf-8'))
            await ctx.send("The result was a bit too long.. so here is a text file instead 🎁",
                           file=discord.File(data, filename='Result.txt'),
                           )

    @commands.hybrid_command()
    @checks.is_owner()
    async def eval(self, ctx, *, code: str):
        code = code.strip("`")
        if code.startswith("py\n"):
            code = "\n".join(code.split("\n")[1:])

        if not re.search(  # Check if it's an expression
                r"^(return|import|for|while|def|class|"
                r"from|exit|[a-zA-Z0-9]+\s*=)",
                code, re.M) and len(code.split("\n")) == 1:
            code = "_ = " + code

        await self.do_eval(ctx, code)

    def _format(self, inp, out):
        self.env["_"] = out

        res = ""

        # Erase temp input we made
        if inp.startswith("_ = "):
            inp = inp[4:]

        lines = [l for l in inp.split("\n") if l.strip()]
        if len(lines) != 1:
            lines += [""]

        # Create the input dialog
        for i, line in enumerate(lines):
            s = ">>> " if i == 0 else "... "

            if i == len(lines) - 2 and line.startswith("return"):
                line = line[6:].strip()

            res += s + line + "\n"

        self.stdout.seek(0)
        text = self.stdout.read()
        self.stdout.close()
        self.stdout = io.StringIO()

        if text:
            res += text + "\n"

        if not out:
            # No output, return the input statement
            return res, None

        if isinstance(out, discord.Embed):
            # We made an embed? Send that as embed
            res += "<Embed>"
            res = (res, out)

        else:
            # Add the output
            res += str(out)
            res = (res, None)

        return res

    @app_commands.command()
    @checks.is_owner()
    async def test_options(
            self, interaction: discord.Interaction,
            string: Optional[str] = None,
            integer: Optional[int] = None,
            boolean: Optional[bool] = None,
            member: Optional[discord.Member] = None,
            channel: Optional[discord.TextChannel] = None,
            role: Optional[discord.Role] = None,
            number: Optional[float] = None,
            attachment: Optional[discord.Attachment] = None
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        data = interaction.data
        json_string = json.dumps(data, indent=4)
        json_file = io.BytesIO(json_string.encode("utf-8"))
        json_file.seek(0)
        em = discord.Embed(color=discord.Color.blurple(), title="Data:")
        if string:
            em.add_field(name="String:", value=string)
        if integer:
            em.add_field(name="Integer:", value=str(integer))
        if boolean:
            em.add_field(name="Boolean:", value=str(boolean))
        if member:
            em.add_field(name="Member:", value=f"{member.mention} ({member})")
        if channel:
            em.add_field(name="Channel:", value=f"{channel.mention} ({channel})")
        if role:
            em.add_field(name="Role:", value=f"{role.mention} ({role})")
        if number:
            em.add_field(name="Number:", value=str(number))
        if attachment:
            em.add_field(name="Attachment:", value=attachment.filename)

        parent_command = ""
        parent = interaction.command.parent
        while parent:
            parent_command = f"{parent.name} {parent_command}"
            parent = parent.parent
        command = "/" + parent_command + interaction.command.name
        options = options_to_string(interaction.data, code=True)
        command += options
        await interaction.followup.send(command, embed=em, file=discord.File(json_file, "data.json"))

