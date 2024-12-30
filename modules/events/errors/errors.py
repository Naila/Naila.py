import os
import traceback

import discord
import sentry_sdk
from discord import app_commands
from discord.ext import commands
from sentry_sdk import capture_exception

from common.functions.text import options_to_string, pagify
from common.functions.time import float_to_discord_timestamp

from bot import Bot


class Errors(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._old_tree_error = None

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timestamp = float_to_discord_timestamp(error.retry_after)
            # noinspection PyUnresolvedReferences
            return await interaction.response.send_message(f"You're on cooldown! Try again {timestamp}", ephemeral=True)
        if isinstance(error, app_commands.CheckFailure):
            # noinspection PyUnresolvedReferences
            return await interaction.response.send_message(f"You don't have permission to use this command!",
                                                           ephemeral=True)
        # Sentry
        with sentry_sdk.isolation_scope() as scope:
            scope.set_tag("guild", interaction.guild.id if interaction.guild else None)
            scope.set_tag("channel", interaction.channel.id)
            scope.set_tag("command", interaction.command.name)
            scope.set_tag("user", interaction.user.id)
            sentry_sdk.capture_exception(error)

        webhook = discord.Webhook.from_url(os.getenv("ERROR_WEBHOOK"), session=self.bot.session)

        long = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        self.bot.log.error(long)

        parent_command = ""
        parent = interaction.command.parent
        while parent:
            parent_command = f"{parent.name} {parent_command}" if parent_command else f"{parent.name}"
            parent = parent.parent
        command = "/" + (f"{parent_command} " if parent_command else "") + interaction.command.name
        options = options_to_string(interaction.data)
        command += options

        em = discord.Embed(
            color=self.bot.config.colors["error"],
            description=f"`{type(error).__name__}: {str(error)}`",
            title="Error:"
        )
        em.add_field(name="Content:", value=command)
        em.add_field(name="Invoker:", value=f"{interaction.user.mention}\n({interaction.user})")
        if not isinstance(interaction.channel, discord.DMChannel):
            em.add_field(
                name="Location:",
                value=f"**Guild:** {interaction.guild.name}\n"
                      f"**Channel:** {interaction.channel.mention} ({interaction.channel.name})"
            )
        else:
            em.add_field(name="Location:", value="Private messages")

        await webhook.send(embed=em)
        if pages := pagify(long):
            for page in pages:
                await webhook.send(f"```py\n{page}\n```")
