from discord.ext import commands
from utils.database import PrivateVCs
import discord

__author__ = "Kanin"
__date__ = "12/23/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


class PrivateVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        guild: discord.Guild = member.guild
        if after.channel is not None:
            settings = await PrivateVCs.fetch_settings(self.bot, guild)
            data = await PrivateVCs.fetch_data(self.bot, member)
            if data:
                return
            if settings["vc_enabled"] and after.channel.id == settings["default_vc_id"]:
                category: discord.CategoryChannel = guild.get_channel(settings["category_id"])
                if not category:
                    # TODO: Remove data
                    return
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                vc: discord.VoiceChannel =\
                    await category.create_voice_channel(f"{member.name}'s channel", overwrites=overwrites)
                tc: discord.TextChannel =\
                    await category.create_text_channel(f"{member.name}s-channel", overwrites=overwrites)
                await PrivateVCs.add_data(self.bot, member, guild, tc, vc)
                await member.move_to(vc, reason="User created private channel")
                # TODO: Send helpful information
                await tc.send(member.mention)
        else:
            data = await PrivateVCs.fetch_data(self.bot, member)
            if not data:
                return
            vc: discord.VoiceChannel = guild.get_channel(data["voicechannel_id"])
            tc: discord.TextChannel = guild.get_channel(data["textchannel_id"])
            await vc.delete(reason="User left private vc")
            await tc.delete(reason="User left private vc")
            await PrivateVCs.update_data(self.bot, member)


def setup(bot):
    bot.add_cog(PrivateVC(bot))
