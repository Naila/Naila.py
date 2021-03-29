import contextlib
import inspect
import io
import os
import re
import textwrap
import time
import traceback
from io import BytesIO

import discord
import psutil
from discord.ext import commands

from bot import Bot
from utils.checks import checks
from utils.ctx import Context

ENV = {
    "contextlib": contextlib,
    "inspect": inspect,
    "io": io,
    "os": os,
    "re": re,
    "textwrap": textwrap,
    "time": time,
    "traceback": traceback,
    "BytesIO": BytesIO,
    "discord": discord,
    "psutil": psutil
}


class Evaluate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.process = psutil.Process()
        self.env = ENV
        self.stdout = io.StringIO()

    async def _eval(self, ctx: Context, code):
        if code == "exit()":
            self.env = ENV
            return await ctx.send(f"```Reset history!```")

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

        start = time.time()
        try:
            exec(_code, self.env)
            func = self.env['func']
            res = await func()

        except:
            res = traceback.format_exc()

        end = time.time()
        out, embed = self._format(code, res)
        try:
            await ctx.send(f"```py\n{out}\n\nTime to execute: {round((end - start) * 1000, 3)}ms```", embed=embed)
        except discord.HTTPException:
            data = BytesIO(out.encode('utf-8'))
            await ctx.send(content=f"The result was a bit too long.. so here is a text file instead 🎁",
                           file=discord.File(data, filename=f'Result.txt'))

    @checks.is_owner()
    @commands.command(hidden=True, description="Evaluate code in a REPL like environment")
    async def eval(self, ctx: Context, *, code: str):
        code = code.strip("`")
        if code.startswith("py\n"):
            code = "\n".join(code.split("\n")[1:])

        if not re.search(  # Check if it's an expression
                r"^(return|import|for|while|def|class|"
                r"from|exit|[a-zA-Z0-9]+\s*=)",
                code, re.M) and len(code.split("\n")) == 1:
            code = "_ = " + code

        await self._eval(ctx, code)

    def _format(self, inp, out):
        self.env["_"] = out

        res = ""

        # Erase temp input we made
        if inp.startswith("_ = "):
            inp = inp[4:]

        lines = [line for line in inp.split("\n") if line.strip()]
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

    @checks.is_owner()
    @commands.group(hidden=True)
    async def sql(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @checks.is_owner()
    @sql.command(name="execute")
    async def sql_execute(self, ctx: Context, *, query: str):
        query = query.strip("`")
        con = await self.bot.pool.acquire()
        if query.startswith("sql\n"):
            query = "\n".join(query.split("\n")[1:])

        command = await con.execute(query)
        await ctx.send(f"```py\n{command}```")
        await self.bot.pool.release(con)

    @checks.is_owner()
    @sql.command(name="fetch")
    async def sql_fetch(self, ctx: Context, *, query: str):
        query = query.strip("`")
        con = await self.bot.pool.acquire()
        if query.startswith("sql\n"):
            query = "\n".join(query.split("\n")[1:])

        command = await con.fetch(query)
        await ctx.send(f"```py\n{command}```")
        await self.bot.pool.release(con)


def setup(bot):
    bot.add_cog(Evaluate(bot))
