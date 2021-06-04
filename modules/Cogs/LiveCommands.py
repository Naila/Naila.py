from datetime import datetime

from discord import Embed
from beautifultable import BeautifulTable, STYLE_BOX_ROUNDED
from discord.ext.commands import Cog, command

from bot import Bot
from modules.Cogs.Help import command_signature
from utils.checks import checks
from utils.ctx import Context


class TheCore:
    def __init__(self):
        self.command = []
        self.count = []
        self.start = []
        self.process = []
        self.last = None


class LiveCommands(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.command = {}

    def get_commandlist(self):
        if 1 in self.command:
            return self.command[1]
        self.command[1] = TheCore()
        return self.command[1]

    @Cog.listener()
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

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        core = self.get_commandlist()
        cmd = ctx.command.qualified_name.replace(" ", "_")

        if ctx.valid and cmd in core.command:
            dex = core.command.index(cmd)
            now = datetime.utcnow()
            start = core.start[dex]
            core.process[dex] = abs((now - start).total_seconds())

    @command(name="commandlist", aliases=["cmdlist", "cmdstats"])
    @checks.bot_has_permissions(embed_links=True)
    async def command_list(self, ctx: Context):
        try:
            core = self.get_commandlist()
            cmd = core.command
            count = core.count
            proc = core.process

            count, cmd, proc = (list(t) for t in zip(*sorted(zip(count, cmd, proc), reverse=True)))

            p = BeautifulTable()
            p.set_style(STYLE_BOX_ROUNDED)
            p.rows.separator = ""
            p.column_headers = ["*", "Command", "Count", "Process"]
            z = 0
            for x in range(25):
                try:
                    z += 1
                    p.append_row([x + 1, cmd[x], f'{count[x]:,}', f"{round(proc[x], 2)}"])
                except (IndexError, RuntimeError):
                    z -= 1
                    break

            post = Embed(color=await ctx.guildcolor())
            post.title = f"Naila's top {z} commands:"
            post.description = f"```ml\n{p}```"
            await ctx.reply(embed=post)
        except ValueError:
            return await ctx.send_error("Unable to post stats, Not enough data!")

    @command(aliases=["cmdinfo"])
    @checks.bot_has_permissions(embed_links=True)
    async def commandinfo(self, ctx: Context, *, cmd: str):
        cmd = self.bot.get_command(cmd)

        if not cmd:
            return await ctx.send_help(ctx.command)

        name = cmd.name

        em = Embed(color=await ctx.guildcolor())
        em.set_author(name="Command info")
        em.description = f"**Command:** {name}\n" \
                         f"**Cog:** {cmd.cog_name}"
        if cmd.aliases:
            em.description += f"\n**Aliases:** {', '.join(cmd.aliases)}"

        em.add_field(name="Arguments:", value=command_signature(cmd))
        em.add_field(name="Checks:", value=cmd.checks, inline=False)

        command_stat = self.get_commandlist()
        if name in command_stat.command:
            usage = command_stat.count[command_stat.command.index(name)]
            em.set_footer(text=f"Used {usage} times since reboot")

        await ctx.reply(embed=em)


def setup(bot):
    bot.add_cog(LiveCommands(bot))
