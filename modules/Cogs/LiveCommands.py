from datetime import datetime as dt

import discord
from beautifultable import BeautifulTable, STYLE_RST
from discord.ext import commands


class The_Core():
    def __init__(self):
        self.cmd = []
        self.count = []
        self.start = []
        self.process = []
        self.last = None


ban_cmd = ["reload", "load", "unload", "update", "cmdlist"]


class Live_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = {}

    def get_cmdlist(self):
        if 1 in self.cmd:
            return self.cmd[1]
        else:
            self.cmd[1] = The_Core()
            return self.cmd[1]

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        core = self.get_cmdlist()

        if ctx.valid:
            if not str(ctx.command.name) in core.cmd:
                if str(ctx.command.name) not in ban_cmd:
                    core.cmd.append(str(ctx.command.name))
                    core.count.append(1)
                    core.process.append(0)
                    core.start.append(dt.now().strftime("%I %M %S %f"))
                    core.last = str(ctx.command.name)
            else:
                if str(ctx.command.name) not in ban_cmd:
                    dex = core.cmd.index(f"{str(ctx.command.name)}")
                    core.count[dex] += 1
                    core.start[dex] = dt.now().strftime("%I %M %S %f")
                    core.process[dex] = 0
                    core.last = str(ctx.command.name)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.command_statistics["commands_processed"] += 1
        self.bot.command_statistics[ctx.command.name] += 1
        core = self.get_cmdlist()
        if ctx.valid:
            if str(ctx.command.name) not in ban_cmd:
                if str(ctx.command.name) in core.cmd:
                    dex = core.cmd.index(f"{str(ctx.command.name)}")
                    now = dt.now().strftime("%I %M %S %f")
                    start = core.start[dex]
                    core.process[dex] = abs(
                        (dt.strptime(now, "%I %M %S %f") - dt.strptime(start, "%I %M %S %f")).total_seconds())
                else:
                    pass

    @commands.command(name="cmdlist", aliases=['cmdstats'])
    async def cmd_list(self, ctx):
        core = self.get_cmdlist()
        cmds = core.cmd
        count = core.count
        proc = core.process
        
        count, cmds, proc = (list(t) for t in zip(*sorted(zip(count, cmds, proc), reverse=True)))

        most_used_cmds = cmds[0]
        uses = count[0]

        cmd_list = ""

        # for x in range(25):
        # 	try:
        # 		z += 1
        # 		cmd_list += f"[{cmds[x]}]"
        # 		cmd_list += f"[{count[x]}]"
        # 		cmd_list += f"{round(proc[x], 2)}\n"
        # 	except (IndexError, RuntimeError):
        # 		z -= 1
        # 		break

        p = BeautifulTable()
        p.set_style(STYLE_RST)
        p.column_headers = [" ", "Command", "Count", "Process"]
        z = 0
        for x in range(25):
            try:
                z += 1
                p.append_row([x + 1, cmds[x], f'{count[x]:,}', f"{round(proc[x], 2)}"])
            except (IndexError, RuntimeError):
                z -= 1
                break

        post = discord.Embed()
        post.title = f"Nalia Live {z} Commands:"
        post.description = f"Most Used: {most_used_cmds}({uses:,})\nLast Cmd Ran: {core.last}"
        post.description += f"```ml\n{str(p)}```"

        await ctx.send(embed=post)

    @commands.command()
    async def cmdinfo(self, ctx, *, cmd: str):
        the_cmd = self.bot.get_command(cmd)

        if the_cmd is None:
            await ctx.send("No command found")
        else:
            cmd_stat = self.get_cmdlist()

            aliases = the_cmd.aliases
            name = the_cmd.name
            cog = the_cmd.cog_name
            the_args = the_cmd.clean_params
            the_checks = the_cmd.checks
            # the_defaults = the_cmd.__defaults__
            post = f"{name} info:\n" f"Aliases: {aliases}\n" f"Cog: {cog}\n\n"
            post += f"Args&Variables: {dict(the_args)}\n\n"
            post += f"Checks Req: {the_checks}"
            if cmd in cmd_stat.cmd:
                dex = cmd_stat.cmd.index(cmd)
                times = cmd_stat.count[dex]

                post += f"\n**Used: `{times}` times.**"

            await ctx.send(post)


def setup(bot):
    bot.add_cog(Live_Commands(bot))
