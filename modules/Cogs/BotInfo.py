import time
from datetime import datetime

from discord import Embed, TextChannel, VoiceChannel, CategoryChannel
import psutil
from discord.ext.commands import Cog, command

from bot import Bot
from config import config
from utils.checks import checks
from utils.ctx import Context
from utils.functions.text import filesize_fix
from utils.functions.time import get_bot_uptime


class BotInfo(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(description="List of APIs we use")
    @checks.bot_has_permissions(embed_links=True)
    async def apis(self, ctx: Context):
        em = Embed(color=await ctx.guildcolor())
        em.set_author(name="APIs we use:")
        em.description = "https://some-random-api.ml/\n" \
                         "https://random-d.uk/\n" \
                         "https://thecatapi.com/\n" \
                         "https://thedogapi.com/\n" \
                         "https://weeb.sh/\n" \
                         "https://boob.bot/\n" \
                         "https://sheri.bot/"
        await ctx.reply(embed=em)

    @command(description="Invite the bot or join the bots support server!")
    @checks.bot_has_permissions(embed_links=True)
    async def invite(self, ctx: Context):
        invite = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=applications.commands+bot"
        em = Embed(color=await ctx.guildcolor())
        em.description = f"**Support server:** {config.support_invite}\n" \
                         f"**Bot invite:**" \
                         f" [Recommended perms]({invite + f'&permissions={config.permissions.value}'}) |" \
                         f" [No perms]({invite})"
        await ctx.reply(embed=em)

    @command(description="Various stats about the bot")
    @checks.bot_has_permissions(embed_links=True)
    async def stats(self, ctx: Context):
        bot = self.bot
        text, voice, category, news = 0, 0, 0, 0
        for channel in self.bot.get_all_channels():
            if isinstance(channel, TextChannel):
                if channel.is_news():
                    news += 1
                text += 1
            elif isinstance(channel, VoiceChannel):
                voice += 1
            elif isinstance(channel, CategoryChannel):
                category += 1
        channels = text + voice + category + news
        cpu_usage = f"{psutil.Process().cpu_percent():.1f}"
        memory_usage = filesize_fix(psutil.Process().memory_full_info().uss)
        t1 = time.perf_counter()
        async with ctx.channel.typing():
            t2 = time.perf_counter()
        em = Embed(
            color=await ctx.guildcolor()
        ).add_field(
            name="Ping:",
            value=f"**{round((t2 - t1) * 1000)}ms** {ctx.emojis('utility.ping')}"
        ).add_field(
            name="Serving:",
            value=f"**Guilds:** {len(bot.guilds)} {ctx.emojis('utility.globe')}\n"
                  f"**Users:** {len(set(bot.get_all_members()))} {ctx.emojis('utility.people')}\n"
                  f"**Channels:** {channels} "
                  f"{ctx.emojis('channels.text')}/{ctx.emojis('channels.voice')}/"
                  f"{ctx.emojis('channels.category')}\n"
                  f"**Text Channels:** {text} {ctx.emojis('channels.text')}\n"
                  f"**Voice Channels:** {voice} {ctx.emojis('channels.voice')}\n"
                  f"**Category Channels:** {category} {ctx.emojis('channels.category')}",
            inline=False
        ).add_field(
            name="System:",
            value=f"**OS:** Linux {ctx.emojis('system.linux')}\n"
                  f"**Version:** Ubuntu 18.04 {ctx.emojis('system.ubuntu')}\n"
                  f"**CPU Usage:** {cpu_usage} {ctx.emojis('system.cpu')}\n"
                  f"**Memory Usage:** {memory_usage} {ctx.emojis('system.ram')}",
            inline=False
        ).add_field(
            name="Version:",
            value=f"**Bot:** {bot.version['bot']}\n"
                  f"**Python:** {bot.version['python']} {ctx.emojis('utility.python')}\n"
                  f"**Discord.py:** {bot.version['discord.py']} {ctx.emojis('utility.discordpy')}",
            inline=False
        ).add_field(
            name="Counters:",
            value=f"**Command count:** {len(bot.commands)} {ctx.emojis('utility.abacus')}\n"
                  f"**Messages read:** {bot.counter['messages']} {ctx.emojis('utility.chat')}\n"
                  f"**Commands ran:** {bot.counter['commands_ran']} {ctx.emojis('utility.abacus')}\n"
                  f"**Foxes caught:** {bot.counter['foxes_caught']} {ctx.emojis('utility.fox')}",
            inline=False
        ).add_field(
            name="Uptime:",
            value=f"🆙 **{get_bot_uptime(bot, brief=True)}** 🆙",
            inline=False
        ).set_author(
            name="🦊🐾Bot stats🐾🦊",
            icon_url=bot.user.avatar_url
        ).set_footer(
            text=datetime.utcnow().strftime(bot.config.time_format),
            icon_url=bot.user.avatar_url
        )
        await ctx.reply(embed=em)


def setup(bot):
    bot.add_cog(BotInfo(bot))
