import discord
from config import config
from discord.ext import commands
from discord.utils import oauth_url
from discord_slash import SlashCommand, SlashContext, cog_ext


class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="invite")
    async def slash_invite(self, ctx: SlashContext):
        invite = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=applications.commands+bot"
        em = discord.Embed(color=self.bot.color)
        em.description = f"**Support server:** {config.support_invite}\n" \
                         f"**Bot invite:**" \
                         f" [Recommended perms]({invite + f'&permissions={config.permissions.value}'}) |" \
                         f" [No perms]({invite})"
        await ctx.send(embeds=[em])


def setup(bot):
    bot.add_cog(SlashCommands(bot))
