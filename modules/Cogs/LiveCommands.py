from datetime import datetime

import discord
from beautifultable import BeautifulTable, STYLE_BOX_ROUNDED
from discord.ext import commands

from bot import Bot
from utils.checks import checks
from utils.ctx import Context


class TheCore:
    def __init__(self):
        self.command = []
        self.count = []
        self.start = []
        self.process = []
        self.last = None


class LiveCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.command = {}

    def get_commandlist(self):
        if 1 in self.command:
            return self.command[1]
        self.command[1] = TheCore()
        return self.command[1]

    @commands.Cog.listener()
    async def on_command(self, ctx: Context):
        core = self.get_commandlist()

        if ctx.valid:
            cmd = ctx.command.qualified_name.replace(" ", "_")
            if cmd not in core.command:
                core.command.append(cmd)
                core.count.append(1)
                core.process.append(0)
                core.start.append(datetime.utcnow())
            else:
                dex = core.command.index(cmd)
                core.count[dex] += 1
                core.start[dex] = datetime.utcnow()
                core.process[dex] = 0
            core.last = cmd

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: Context):
        core = self.get_commandlist()
        cmd = ctx.command.qualified_name.replace(" ", "_")

        if ctx.valid and cmd in core.command:
            dex = core.command.index(cmd)
            now = datetime.utcnow()
            start = core.start[dex]
            core.process[dex] = abs((now - start).total_seconds())

    @commands.command(name="commandlist", aliases=["cmdlist", "cmdstats"])
    @checks.custom_bot_has_permissions(embed_links=True)
    async def command_list(self, ctx: Context):
        try:
            core = self.get_commandlist()
            command = core.command
            count = core.count
            proc = core.process

            count, command, proc = (list(t) for t in zip(*sorted(zip(count, command, proc), reverse=True)))

            p = BeautifulTable()
            p.set_style(STYLE_BOX_ROUNDED)
            p.rows.separator = ""
            p.column_headers = ["*", "Command", "Count", "Process"]
            z = 0
            for x in range(25):
                try:
                    z += 1
                    p.append_row([x + 1, command[x], f'{count[x]:,}', f"{round(proc[x], 2)}"])
                except (IndexError, RuntimeError):
                    z -= 1
                    break

            post = discord.Embed(color=await ctx.guildcolor())
            post.title = f"Naila's top {z} commands:"
            post.description = f"```ml\n{p}```"
            await ctx.reply(embed=post)
        except ValueError:
            return await ctx.send_error("Unable to post stats, Not enough data!")

    # @commands.command()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def commandinfo(self, ctx, *, command: str):
    #     command = self.bot.get_command(command)
    #
    #     if command is None:
    #         return await ctx.send_help(ctx.command)
    #
    #     aliases = command.aliases
    #     name = command.name
    #     cog = command.cog_name
    #     the_args = command.clean_params
    #     the_checks = command.checks
    #     # the_defaults = the_command.__defaults__
    #     post = f"{name} info:\n" f"Aliases: {aliases}\n" f"Cog: {cog}\n\n"
    #     post += f"Args&Variables: {dict(the_args)}\n\n"
    #     post += f"Checks Req: {the_checks}"
    #
    #     command_stat = self.get_commandlist()
    #     if command in command_stat.command:
    #         dex = command_stat.command.index(command)
    #         times = command_stat.count[dex]
    #
    #         post += f"\n**Used: `{times}` times.**"
    #
    #     await ctx.reply(post)


def setup(bot):
    bot.add_cog(LiveCommands(bot))
