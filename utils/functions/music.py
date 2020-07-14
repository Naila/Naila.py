import asyncio
import re
from decimal import Decimal, ROUND_HALF_UP

import yaml
from dictor import dictor
from lavalink import AudioTrack

import discord
from discord.ext import commands
from discord.utils import escape_markdown
# from ksoftapi.errors import NoResults

__author__ = "Kanin"
__date__ = "02/09/2020"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"

url_rx = re.compile("https?://(?:www\\.)?.+")


async def connect(bot, guild_id: int, channel_id: int):
    ws = bot.shards[bot.get_guild(guild_id).shard_id].ws
    await ws.voice_state(str(guild_id), str(channel_id))


async def disconnect(bot, guild_id: int):
    ws = bot.shards[bot.get_guild(guild_id).shard_id].ws
    await ws.voice_state(str(guild_id), None)


async def enqueue_and_send(bot, ctx, query=None, track=None):
    player = bot.lavalink.player_manager.get(ctx.guild.id)
    spotify_track = spotify = None
    em = await embed(bot, ctx.guild.id)
    if query:
        query = query.strip("<>")
        if not url_rx.match(query):
            query = f"ytsearch:{query}"
        # elif "spotify.com" in query:
        #     if "/track/" in query:
        #         track_id = query.split("/track/")[1].split("?si=")[0]
        #         spotify_track = bot.spotify.track(track_id)
        #         query = f"ytsearch:{spotify_track['artists'][0]['name']} {spotify_track['name']}"
        #     elif "/playlist/" in query:
        #         errors = added = 0
        #         playlist_id = query.split("/playlist/")[1].split("?si=")[0]
        #         playlist = bot.spotify.playlist(playlist_id)
        #         tracks = playlist["tracks"]
        #         for track in tracks["items"]:
        #             track = track["track"]
        #             query = f"ytsearch:{track['artists'][0]['name']} {track['name']}"
        #             results = await player.node.get_tracks(query)
        #             if not results or not results["tracks"]:
        #                 errors += 1
        #             else:
        #                 added += 1
        #                 spotify = {
        #                     "uri": track["external_urls"]["spotify"],
        #                     "title": track["name"],
        #                     "album_art": track["album"]["images"][0]["url"]
        #                 }
        #                 player.add(track=AudioTrack(results["tracks"][0], ctx.author.id, **spotify),
        #                            requester=ctx.author.id)
        #         em.title = "Playlist Enqueued:"
        #         em.description = f"<:spotify:678293495416356897> " \
        #                          f"**[{playlist['name']}]({playlist['external_urls']['spotify']})** -" \
        #                          f" {added} tracks added to the queue! ({errors} failed to add)"
        #         await ctx.send(embed=em)
        #         if not player.is_playing:
        #             await player.play()
        #         return

        results = await player.node.get_tracks(query)
        if not results or not results["tracks"]:
            em.description = "Nothing found!"
            return await ctx.send(embed=em)
        if results["loadType"] == "PLAYLIST_LOADED":
            tracks = results["tracks"]
            for track1 in tracks:
                player.add(requester=ctx.author.id, track=track1)

            em.title = "Playlist Enqueued:"
            em.description = f"{ctx.emojis('music.youtube')}" \
                             f" **[{results['playlistInfo']['name']}]({query})** -" \
                             f" {len(tracks)} tracks added to the queue!"
            await ctx.send(embed=em)
            if not player.is_playing:
                await player.play()
            return
        track = results["tracks"][0]

    if spotify_track:
        spotify = {
            "uri": spotify_track["external_urls"]["spotify"],
            "title": spotify_track["name"],
            "album_art": spotify_track["album"]["images"][0]["url"]
        }
        player.add(track=AudioTrack(track, ctx.author.id, **spotify),
                   requester=ctx.author.id)
    else:
        player.add(requester=ctx.author.id, track=track)
    queue_time = 0
    queue_time_fixed = "Now!"
    for song in player.queue:
        if song.stream:
            queue_time_fixed = "Unknown"
        queue_time += song.duration
    if player.is_playing:
        if player.current.stream:
            queue_time_fixed = "Unknown"
        queue_time += player.current.duration - player.position
        if queue_time_fixed != "Unknown":
            queue_time_fixed = format_time(queue_time)
    duration = "🔴 LIVE" if track["info"]["isStream"] else format_time(track["info"]["length"])
    if spotify:
        uri = spotify["uri"]
        title = spotify["title"]
        album_art = spotify["album_art"]
    else:
        uri = track["info"]["uri"]
        title = track["info"]["title"]
        album_art = get_thumbnail(uri)
    emoji = get_emoji(bot, uri)
    title_fixed = escape_markdown(title)
    em.title = "Track Enqueued:"
    em.description = f"{emoji} [**{title_fixed}**]({uri})"
    em.add_field(name="Requester:", value=ctx.author.mention)
    em.add_field(name="Position in queue:", value=str(len(player.queue)))
    em.add_field(name="Duration:", value=duration)
    em.add_field(name="Estimated time until playing:", value=queue_time_fixed)
    em.set_thumbnail(url=album_art)
    await ctx.send(embed=em)
    if not player.is_playing:
        await player.play()


def format_time(time):
    hours, remainder = divmod(int(time / 1000), 3600)
    minutes, seconds = divmod(remainder, 60)
    time_formatted = f"{minutes:02d}:{seconds:02d}"
    if hours:
        time_formatted = f"{hours:02d}:" + time_formatted
    return time_formatted


def emojis(bot, emoji: str):
    with open("config/emojis.yml", "r") as x:
        y = yaml.safe_load(x)
    return bot.get_emoji(dictor(y, emoji))


def get_emoji(bot, query: str):
    emoji = ""
    if "twitch.tv" in query:
        emoji = emojis(bot, "music.twitch")
    elif "soundcloud.com" in query:
        emoji = emojis(bot, "music.soundcloud")
    elif "vimeo.com" in query:
        emoji = emojis(bot, "music.vimeo")
    elif "mixer.com" in query or "beam.pro" in query:
        emoji = emojis(bot, "music.mixer")
    elif "youtube.com" in query or "youtu.be" in query or query.startswith("ytsearch:"):
        emoji = emojis(bot, "music.youtube")
    elif "spotify.com" in query:
        emoji = emojis(bot, "music.spotify")
    return emoji


def get_thumbnail(url):
    if "youtube" in url:
        return f"https://img.youtube.com/vi/{url.split('?v=')[1]}/default.jpg"
    return ""


async def guildcolor(bot, guild_id: int):
    con = await bot.pool.acquire()
    color = await con.fetchval("SELECT color FROM guilds WHERE guild_id=$1", guild_id)
    await bot.pool.release(con)
    return color


async def embed(bot, guild_id: int):
    em = discord.Embed(
        color=await guildcolor(bot, guild_id)
    ).set_author(
        name="Naila Music",
        icon_url=bot.user.avatar_url_as(static_format="png")
    ).set_footer(
        text="Music will be a premium feature soon! Enjoy it while it's here!"
    )
    return em


def draw_time(bot, ctx):
    player = bot.lavalink.player_manager.get(ctx.guild.id)
    time = Decimal(
        str((player.position / player.current.duration) * 13)
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    time = time or 1
    msg = "|"
    for i in range(13):
        i += 1
        msg += "🔘" if i == time else "▬"
    msg += "| "
    msg += "⏸ " if player.paused else "▶ "
    msg += "[🔴 LIVE]" if player.current.stream else \
        f"[{format_time(player.position)}/{format_time(player.current.duration)}]"
    return msg


def draw_vol(bot, ctx):
    player = bot.lavalink.player_manager.get(ctx.guild.id)
    volume = Decimal(
        str((player.volume / 200) * 13)
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    volume = volume or 1
    emoji = "🔇" if player.volume == 0 else "🔉" if player.volume <= 100 else "🔊"
    msg = "|"
    for i in range(13):
        i += 1
        msg += "🔘" if i == volume else "▬"
    msg += "| "
    msg += emoji
    msg += f" {int(player.volume / 2)}%"
    return msg


async def ensure_voice(bot, ctx):
    """ This check ensures that the bot and command author are in the same voicechannel. """
    player = bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
    # Create returns a player if one exists, otherwise creates.

    should_connect = ctx.command.name in ["play", "search"]  # Add commands that require joining voice to work.

    if not ctx.author.voice or not ctx.author.voice.channel:
        raise commands.CommandInvokeError("Join a voicechannel first.")

    if not player.is_connected:
        if not should_connect:
            raise commands.CommandInvokeError("Not connected.")

        permissions = ctx.author.voice.channel.permissions_for(ctx.me)

        if not permissions.connect or not permissions.speak:  # Check user limit too?
            raise commands.CommandInvokeError("I need the `CONNECT` and `SPEAK` permissions.")

        player.store("channel", ctx.channel.id)
        player.store("autoplay", AutoPlay())
        player.store("autoplay_enabled", True)
        await connect(bot, ctx.guild.id, ctx.author.voice.channel.id)
    else:
        if int(player.channel_id) != ctx.author.voice.channel.id:
            raise commands.CommandInvokeError("You need to be in my voicechannel.")


class AutoPlay:
    def __init__(self):
        self.history = []

    def store(self, title: str):
        if title in self.history:
            return

        self.history.append(title)  # .lower().strip("(lyrics)").strip("(official video)").strip()
        if len(self.history) > 5:
            self.history.pop(0)

    async def get_recommendation(self, bot):
        try:
            results = await bot.kclient.music.recommendations(tracks=self.history, provider="youtube_ids")
        # except NoResults:
        except Exception:
            return False
        return results[0].youtube_link


class CannotPaginate(Exception):
    pass


class Queue:
    # TODO: Rewrite
    def __init__(self, ctx, color):
        self.bot = ctx.bot
        self.ctx = ctx
        self.player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        self.entries = self.player.queue
        self.message = ctx.message
        self.current_page = None
        self.match = None
        pages, left_over = divmod(len(self.entries), 10)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.permissions = ctx.channel.permissions_for(ctx.guild.me)
        self.embed = discord.Embed(colour=color, title=f"Queue for {ctx.guild.name}")
        self.paginating = len(self.player.queue) > 10
        self.reaction_emojis = [
            ("⏮️", self.first_page),
            ("◀️", self.previous_page),
            ("▶️", self.next_page),
            ("⏭️", self.last_page),
            ("🔢", self.numbered_page),
            ("⏹️", self.stop_pages),
        ]

        if not self.permissions.embed_links:
            raise CannotPaginate("Bot does not have embed links permission.")

        if not self.permissions.send_messages:
            raise CannotPaginate("Bot cannot send messages.")

        if self.paginating:
            # verify we can actually use the pagination session
            if not self.permissions.add_reactions:
                raise CannotPaginate("Bot does not have add reactions permission.")

            if not self.permissions.read_message_history:
                raise CannotPaginate("Bot does not have Read Message History permission.")

    def get_page(self, page):
        base = (page - 1) * 10
        return self.entries[base:base + 10]

    async def show_page(self, page, *, first=False):
        self.current_page = page
        self.embed.set_author(icon_url=self.bot.user.avatar_url, name="Naila Music")
        entries = self.get_page(page)
        if self.player.current.extra:
            uri = self.player.current.extra["uri"]
            title = self.player.current.extra["title"]
            album_art = self.player.current.extra["album_art"]
        else:
            uri = self.player.current.uri
            title = self.player.current.title
            album_art = get_thumbnail(uri)
        self.embed.set_thumbnail(url=album_art)
        emoji = get_emoji(self.bot, uri)
        volume = draw_vol(self.bot, self.ctx)
        now_playing = draw_time(self.bot, self.ctx)
        requester = self.bot.get_user(self.player.current.requester)
        p = [f"**Now Playing:**\n"
             f"{emoji} [**{escape_markdown(title)}**]({uri})\n"
             f"Requested by: {requester.mention}\n"
             f"{now_playing}\n"
             f"**Volume:**\n"
             f"{volume}\n"
             f"**Next in queue:**\n"
             f"`Position` `length` **[Song Title](https://www.youtube.com)**"]
        queue_time = 0
        queue_time_fixed = ""
        for song in self.player.queue:
            if song.stream:
                queue_time_fixed = "Unknown"
            queue_time += song.duration
        if self.player.is_playing:
            if self.player.current.stream:
                queue_time_fixed = "Unknown"
            queue_time += self.player.current.duration - self.player.position
            if queue_time_fixed != "Unknown":
                queue_time_fixed = format_time(queue_time)
        for index, entry in enumerate(entries, 1 + ((page - 1) * 10)):
            duration = "🔴 LIVE" if entry.stream else format_time(entry.duration)
            if entry.extra:
                uri = entry.extra["uri"]
                title = entry.extra["title"]
            else:
                uri = entry.uri
                title = entry.title
            emoji = get_emoji(self.bot, uri)
            title_fixed = escape_markdown(title)
            cut = (title_fixed[:40] + "...") if len(title_fixed) > 27 else title_fixed
            p.append(f"`{index}.` `[{duration}]` {emoji} **[{cut}]({uri})**")

        text = f"Page {page}/{self.maximum_pages} • {len(self.entries)} tracks • {queue_time_fixed} remaining\n" \
               f"Shuffle: {'✅' if self.player.shuffle else '❌'} • Repeat: {'✅' if self.player.repeat else '❌'}"
        self.embed.set_footer(text=text)

        if not self.paginating:
            self.embed.description = "\n".join(p)
            return await self.ctx.channel.send(embed=self.embed)

        if not first:
            self.embed.description = "\n".join(p)
            await self.message.edit(embed=self.embed)
            return

        self.embed.description = "\n".join(p)
        self.message = await self.ctx.channel.send(embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ("⏮️", "⏭️"):
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """goes to the first page"""
        await self.show_page(1)

    async def last_page(self):
        """goes to the last page"""
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """goes to the next page"""
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """goes to the previous page"""
        await self.checked_show_page(self.current_page - 1)

    async def numbered_page(self):
        """lets you type a page number to go to"""
        to_delete = [await self.ctx.channel.send("What page do you want to go to?")]

        def message_check(m):
            return m.author.id == self.ctx.author.id and self.ctx.channel == m.channel and m.content.isdigit()

        try:
            msg = await self.bot.wait_for("message", check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            to_delete.append(await self.ctx.channel.send("Took too long."))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(await self.ctx.channel.send(f"Invalid page given. ({page}/{self.maximum_pages})"))
                await asyncio.sleep(5)

        await self.ctx.channel.delete_messages(to_delete)

    async def stop_pages(self):
        """stops the interactive pagination session"""
        await self.message.clear_reactions()
        self.paginating = False

    def react_check(self, reaction, user):
        if user is None or user.id != self.ctx.author.id:
            return False

        if reaction.message.id != self.message.id:
            return False

        for (emojis, func) in self.reaction_emojis:
            if reaction.emoji == emojis:
                self.match = func
                return True
        return False

    async def queueinate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        first_page = self.show_page(1, first=True)
        if not self.paginating:
            await first_page
        else:
            # allow us to react to reactions right away if we're paginating
            self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.react_check, timeout=120.0)
            except asyncio.TimeoutError:
                self.paginating = False
                try:
                    await self.message.clear_reactions()
                    break
                except (discord.HTTPException, discord.Forbidden):
                    break

            try:
                await self.message.remove_reaction(reaction, user)
            except (discord.HTTPException, discord.Forbidden):
                pass

            await self.match()
