import asyncio
import os
import re
from decimal import Decimal, ROUND_HALF_UP

import discord
import ksoftapi
import lavalink
import yaml
from bs4 import BeautifulSoup
from dictor import dictor
from discord.ext import commands
from discord.utils import escape_markdown
from lavalink import AudioTrack

from bot import Bot
from utils.checks import checks
from utils.ctx import Context
from utils.functions import argparser
from utils.functions.text import pagify

url_rx = re.compile(r"https?://(?:www\.)?.+")
search_emojis = {
    "numbers": ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"],
    "utility": ["❌"]
}


# TODO: DJ roles, spotify playing, playlists, and just cleaning this all up a bit
class Music(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.handles: dict = {}

        if not hasattr(bot, "lavalink"):
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.ksoftapi = ksoftapi.Client(api_key=os.getenv("KSOFT"))
            host = os.getenv("LAVALINK_HOST", "localhost")
            port = int(os.getenv("LAVALINK_PORT", "4437"))
            password = os.getenv("LAVALINK_PASS")
            bot.lavalink.add_node(host=host, port=port, password=password, region="us", name="DEFAULT US")
            bot.lavalink.add_node(host=host, port=port, password=password, region="eu", name="DEFAULT EU")
            bot.lavalink.add_node(host=host, port=port, password=password, region="asia", name="DEFAULT ASIA")
            bot.add_listener(bot.lavalink.voice_update_handler, "on_socket_response")

        if len(bot.lavalink._event_hooks["Generic"]) == 0:  # Seems something is going wrong with cog_unload
            lavalink.add_event_hook(self.track_hook, self.autoplay_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx: Context):
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def autoplay_hook(self, event):
        if not isinstance(event, (lavalink.events.QueueEndEvent, lavalink.events.TrackEndEvent)):
            return

        if not event.player.fetch("autoplay_enabled"):
            return

        autoplay = event.player.fetch("autoplay")
        em = self.embed()

        if isinstance(event, lavalink.events.QueueEndEvent):
            channel = self.bot.get_channel(event.player.fetch("channel"))
            if not channel:
                return

            recommendation = await autoplay.get_recommendation(self.bot)
            if not recommendation:
                return await channel.send("AutoPlay couldn't find a track based off of your last 5 songs played..")

            results = await event.player.node.get_tracks(recommendation)
            if not results:
                return await channel.send("AutoPlay couldn't find a track based off of your last 5 songs played..")

            track = results["tracks"][0]
            queue_time = self.get_queue_time(event.player)
            duration = "🔴 LIVE" if track["info"]["isStream"] else self.format_time(track["info"]["length"])
            emoji = self.get_emoji(track["info"]["uri"])
            title_fixed = escape_markdown(track["info"]["title"])
            em.title = "Autoplay Track Enqueued:"
            em.description = f"{emoji} [**{title_fixed}**]({track['info']['uri']})"
            em.add_field(name="Requester:", value=self.bot.user.mention)
            em.add_field(name="Position in queue:", value=str(len(event.player.queue)))
            em.add_field(name="Duration:", value=duration)
            em.add_field(name="Estimated time until playing:", value=queue_time)
            em.set_thumbnail(url=self.get_thumbnail(track["info"]["uri"]))
            await channel.send(embed=em)
            await event.player.play(AudioTrack(track, requester=self.bot.user.id))

        elif isinstance(event, lavalink.events.TrackEndEvent):
            if "https://www.youtube.com" in event.track.uri or "https://youtu.be/" in event.track.uri:
                autoplay = event.player.fetch("autoplay")
                autoplay.store(event.track.identifier)

    async def track_hook(self, event):
        if not isinstance(event, (lavalink.events.QueueEndEvent, lavalink.events.TrackStartEvent)):
            return

        em = self.embed()
        channel = self.bot.get_channel(event.player.fetch("channel"))
        if not channel:
            return

        if isinstance(event, lavalink.events.QueueEndEvent):
            if not event.player.fetch("autoplay_enabled"):
                await channel.send("Queue Ended.")

        elif isinstance(event, lavalink.events.TrackStartEvent):
            duration = "🔴 LIVE" if event.track.stream else self.format_time(event.track.duration)
            if event.track.extra:
                uri = event.track.extra["uri"]
                title = event.track.extra["title"]
                album_art = event.track.extra["album_art"]
            else:
                uri = event.track.uri
                title = event.track.title
                album_art = self.get_thumbnail(uri)
            emoji = self.get_emoji(uri)
            requester = self.bot.get_user(event.track.requester)
            em.title = "Now Playing:"
            em.description = f"{emoji} **[{title}]({uri})**"
            em.add_field(
                name="Duration:",
                value=duration
            ).add_field(
                name="Requested by:",
                value=requester.mention
            ).set_thumbnail(
                url=album_art
            )
            async for message in channel.history(limit=5):
                for embed in message.embeds:
                    if message.author == self.bot.user and embed.title == "Now Playing:":
                        return await message.edit(embed=em)
            await channel.send(embed=em)

    async def ensure_voice(self, ctx: Context):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # These are commands that require the bot to join a voice channel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voice channel so don't need listing here.
        should_connect = ctx.command.name in ["play", "search"]
        no_vc = ctx.command.name in ["lyrics"]

        if no_vc:
            return True

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError("Join a Voice Channel first.")

        channel: discord.VoiceChannel = ctx.author.voice.channel
        permissions: discord.Permissions = channel.permissions_for(ctx.me)

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError("Not connected.")

            if not permissions.connect:
                raise commands.CommandInvokeError("I need permission to connect!")
            if not permissions.speak:
                raise commands.CommandInvokeError("I need permission to speak!")
            if len(channel.members) >= channel.user_limit and not permissions.move_members:
                raise commands.CommandInvokeError("There's not enough room for me!")

            player.store("channel", ctx.channel.id)
            player.store("autoplay", AutoPlay())
            player.store("autoplay_enabled", False)
            await self.connect_to(ctx.guild, channel)
        else:
            if int(player.channel_id) != channel.id:
                raise commands.CommandInvokeError("You need to be in my Voice Channel!")

    @staticmethod
    async def connect_to(guild: discord.Guild, channel: discord.VoiceChannel = None):
        await guild.change_voice_state(channel=channel, self_deaf=True)

    # TODO: Rewrite, potentially move off of the bot
    @commands.command()
    @checks.bot_has_permissions(embed_links=True)
    @checks.bot_has_permissions(embed_links=True)
    async def lyrics(self, ctx: Context, *, search: str):
        parser = argparser.Arguments()
        parser.add_argument("search", nargs="*")
        parser.add_argument("--spotify", "-s", action="store_true")
        parser.add_argument("--nowplaying", "-np", action="store_true")
        args, valid_check = parser.parse_args(search)
        if not valid_check:
            return await ctx.reply(args)

        em = discord.Embed(color=self.bot.color)
        if args.spotify:
            spotify = [x for x in ctx.author.activities if isinstance(x, discord.Spotify)]
            if not spotify:
                return await ctx.send_error("You either don't have Spotify linked or you're not listening to anything.")
            artists = spotify[0].artist
            title = spotify[0].title.split("(feat.")[0]
            search = f'{title} {artists}'
        elif args.nowplaying:
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            if not player or not player.is_playing or not player.current:
                return await ctx.send_error("I'm not currently playing anything!")
            if player.current.stream:
                return await ctx.send_error("I can't get the lyrics of a stream..")
            search = player.current.title
        base_url = "https://api.genius.com"
        url = base_url + f"/search?q={search}&page=1&per_page=1"
        async with self.bot.session.get(url=url, headers={"Authorization": os.getenv("GENIUS")}) as resp:
            result = await resp.json()
        try:
            result = result["response"]["hits"][0]["result"]
        except (KeyError, IndexError):
            return await ctx.send_error("Song not found")

        async with self.bot.session.get(
                url=base_url + result["api_path"],
                headers={"Authorization": os.getenv("GENIUS")}
        ) as resp:
            json = await resp.json()

        page_url = "https://genius.com" + json["response"]["song"]["path"]
        verif = ctx.emojis("music.checky") if result["primary_artist"]["is_verified"] is True else ""

        desc = f"**Artist:** [{result['primary_artist']['name']} {verif}]({result['primary_artist']['url']})\n" \
               f"**Song:** [{result['title_with_featured']}]({page_url})\n"

        if "pageviews" in result["stats"]:
            views = f"{result['stats']['pageviews']:,}"
            desc += f"**Views:** {views}\n"

        desc += f"**Lyric state:** {result['lyrics_state']}"
        page = await self.bot.session.get(page_url)
        html = BeautifulSoup(await page.text(), "html.parser")
        [h.extract() for h in html("script")]
        lyrics = html.find("div", class_="lyrics").get_text()
        desc += lyrics.replace("[", "**[").replace("]", "]**")
        first_message = True
        pages = list(pagify(desc))
        pages_length = len(pages)
        if pages_length > 5:
            return await ctx.reply("Too long to send.. will have a fix for this in the future!")
        for index, page in enumerate(pages):
            em.description = page
            if first_message:
                em.set_thumbnail(url=result["header_image_url"])
                em.set_author(name=f"{result['title_with_featured']} lyrics")
                if pages_length == 1:
                    em.set_footer(text="Not the song you were looking for? Add the author to your query.")
                    if args.spotify or args.nowplaying:
                        em.set_footer(text="")
                    header = result["primary_artist"]["header_image_url"]
                    if header and not header.startswith("https://assets.genius.com/images/default_avatar_"):
                        em.set_image(url=header)
                first_message = False
            else:
                em.set_thumbnail(url="")
                em.set_author(name="", icon_url="")
                em.set_footer(text="")
                em.set_image(url="")
                if index == pages_length - 1:
                    em.set_footer(text="Not the song you were looking for? Add the author to your query.")
                    if args.spotify or args.nowplaying:
                        em.set_footer(text="")
                    header = result["primary_artist"]["header_image_url"]
                    if header and not header.startswith("https://assets.genius.com/images/default_avatar_"):
                        em.set_image(url=header)
            await ctx.reply(embed=em)

    @commands.command(description="Toggle the queues autoplay status | ONLY WORKS WITH YOUTUBE TRACKS")
    @checks.bot_has_permissions(embed_links=True)
    async def autoplay(self, ctx: Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.reply(embed=em)

        autoplay = player.fetch("autoplay_enabled")
        player.store("autoplay_enabled", not autoplay)
        em.description = f"🔄 | AutoPlay {'enabled' if not autoplay else 'disabled'}"
        await ctx.reply(embed=em)

    # TODO: Limit queue length, longer for patrons
    @commands.command(aliases=['p'])
    @checks.bot_has_permissions(embed_links=True)
    async def play(self, ctx: Context, *, query: str = None):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not query:
            if player.paused:
                await player.set_pause(False)
                em.description = "⏯ | Resumed"
                return await ctx.reply(embed=em)
            return await ctx.send_help(ctx.command)

        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        query = query.strip("<>")
        if not url_rx.match(query):
            query = f"ytsearch:{query}"
        results = await player.node.get_tracks(query)

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL
        #   PLAYLIST_LOADED - direct URL to playlist
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if not results or results["loadType"] == "NO_MATCHES":
            em.description = "Nothing found!"
        elif results["loadType"] == "LOAD_FAILED":
            em.description = "Failed to load track"
        elif results["loadType"] == "PLAYLIST_LOADED":
            tracks = results["tracks"]

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            em.title = "Playlist Enqueued:"
            em.description = f"{ctx.emojis('music.youtube')}" \
                             f" **[{results['playlistInfo']['name']}]({query})** -" \
                             f" {len(tracks)} tracks added to the queue!"
        elif results["loadType"] in ["TRACK_LOADED", "SEARCH_RESULT"]:
            track = results["tracks"][0]

            queue_time = self.get_queue_time(player)
            duration = "🔴 LIVE" if track["info"]["isStream"] else self.format_time(track["info"]["length"])
            emoji = self.get_emoji(track["info"]["uri"])
            title_fixed = escape_markdown(track["info"]["title"])
            em.title = "Track Enqueued:"
            em.description = f"{emoji} [**{title_fixed}**]({track['info']['uri']})"
            em.add_field(name="Requester:", value=ctx.author.mention)
            em.add_field(name="Position in queue:", value=str(len(player.queue)))
            em.add_field(name="Duration:", value=duration)
            em.add_field(name="Estimated time until playing:", value=queue_time)
            em.set_thumbnail(url=self.get_thumbnail(track["info"]["uri"]))

            track = lavalink.models.AudioTrack(track, ctx.author.id)
            player.add(requester=ctx.author.id, track=track)

        await ctx.reply(embed=em)

        if not player.is_playing:
            await player.play()

    # TODO: Handle permissions on reactions to not need manage_messages
    @commands.command(description="Search for a track on YouTube")
    @checks.bot_has_permissions(embed_links=True, add_reactions=True, manage_messages=True)
    async def search(self, ctx: Context, *, query):
        query = query.strip("<>")
        if url_rx.match(query):
            return await ctx.send_error("Search must be a string! Not a url!")
        query = f"ytsearch:{query}"
        results = await self.bot.lavalink.get_tracks(query)
        if not results or not results["tracks"]:
            return await ctx.reply("Nothing found!")
        tracks = results["tracks"]
        tracks_len = 10 if len(tracks) >= 10 else len(tracks)
        search_list = ""
        for i, track in enumerate(tracks[0:10], start=0):
            emoji = search_emojis["numbers"][i]
            track_title = escape_markdown(tracks[i]["info"]["title"])
            search_list += f"{emoji} [**{track_title}**]({tracks[i]['info']['uri']})\n"
        em = self.embed()
        em.title = "Tracks Found:"
        em.description = search_list
        em.set_footer(text=f"Showing top {tracks_len} results, ❌ to cancel.")
        message = await ctx.reply(embed=em)
        for emoji in range(tracks_len):
            await message.add_reaction(search_emojis["numbers"][emoji])
        for emoji in search_emojis["utility"]:
            await message.add_reaction(emoji)

        def check(reacted, author):
            return reacted.message.id == message.id and author == ctx.author

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
            except asyncio.TimeoutError:
                return await message.clear_reactions()
            if reaction.emoji == "❌":
                return await message.clear_reactions()
            if reaction.emoji in search_emojis["numbers"]:
                player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
                await message.clear_reactions()
                track = tracks[search_emojis["numbers"].index(reaction.emoji)]

                queue_time = self.get_queue_time(player)
                duration = "🔴 LIVE" if track["info"]["isStream"] else self.format_time(track["info"]["length"])
                emoji = self.get_emoji(track["info"]["uri"])
                title_fixed = escape_markdown(track["info"]["title"])
                em.title = "Track Enqueued:"
                em.description = f"{emoji} [**{title_fixed}**]({track['info']['uri']})"
                em.add_field(name="Requester:", value=ctx.author.mention)
                em.add_field(name="Position in queue:", value=str(len(player.queue)))
                em.add_field(name="Duration:", value=duration)
                em.add_field(name="Estimated time until playing:", value=queue_time)
                em.set_thumbnail(url=self.get_thumbnail(track["info"]["uri"]))

                track = lavalink.models.AudioTrack(track, ctx.author.id)
                player.add(requester=ctx.author.id, track=track)

                await ctx.reply(embed=em)

                if not player.is_playing:
                    await player.play()

    @commands.command(aliases=["resume"], description="Pauses or resumes the queue")
    @checks.bot_has_permissions(embed_links=True)
    async def pause(self, ctx: Context):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()
        if not player.is_playing:
            em.description = "Not playing!"
        elif player.paused:
            await player.set_pause(False)
            em.description = "⏯ | Resumed"
        else:
            await player.set_pause(True)
            em.description = "⏯ | Paused"
        await ctx.reply(embed=em)

    @commands.command(aliases=["vol"], description="View or set the volume")
    @checks.bot_has_permissions(embed_links=True)
    async def volume(self, ctx: Context, volume: int = None):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()
        if not volume and volume != 0:
            em.add_field(name="Volume:", value=self.draw_vol(player))
            return await ctx.reply(embed=em)
        if volume == 0:
            await player.set_volume(volume)
        elif volume >= 100:
            await player.set_volume(200)
        else:
            await player.set_volume(volume * 2)
        em.add_field(name="Volume set:", value=self.draw_vol(player))
        await ctx.reply(embed=em)

    @commands.command(description="Seek through a track in seconds or by time string")
    @checks.bot_has_permissions(embed_links=True)
    async def seek(self, ctx: Context, time):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.reply(embed=em)

        time_list = time.split(":")
        if len(time_list) >= 5:
            em.description = "Cannot seek this far!"
            return await ctx.reply(embed=em)

        seconds = sum(x * int(t) for x, t in zip([1, 60, 3600, 86400], reversed(time_list)))
        milliseconds = seconds * 1000
        if milliseconds > player.current.duration:
            em.description = "Time cannot be longer than the song!"
        else:
            await player.seek(milliseconds)
            em.description = f"Moved track to **{self.format_time(milliseconds)}**"
        await ctx.reply(embed=em)

    @commands.command(description="Get information on a song in the queue")
    @checks.bot_has_permissions(embed_links=True)
    async def songinfo(self, ctx: Context, index: int):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()
        if not player.queue:
            em.description = "There's nothing in the queue! Why not queue something?"
            return await ctx.reply(embed=em)
        if index > len(player.queue) or index < 1:
            em.description = "Index has to be > 1 and < the queue size!"
            return await ctx.reply(embed=em)
        index -= 1
        i = 0
        estimated_time = 0
        for track in player.queue:
            if i < index:
                i += 1
                if track.stream:
                    estimated_time = "Unknown"
                    break
                estimated_time += track.duration
        if estimated_time != "Unknown":
            estimated_time += player.current.duration - player.position
            estimated_time = self.format_time(estimated_time)
        song = player.queue[index]
        requester = self.bot.get_user(song.requester)
        duration = "🔴 LIVE" if song.stream else self.format_time(song.duration)
        emoji = self.get_emoji(song.uri)
        em.title = "Track info:"
        em.description = f"{emoji} [**{escape_markdown(song.title)}**]({song.uri})"
        em.add_field(name="Requester:", value=requester.mention)
        em.add_field(name="Duration:", value=duration)
        em.add_field(name="Estimated time until playing:", value=estimated_time)
        em.set_thumbnail(url=self.get_thumbnail(song.uri))
        await ctx.reply(embed=em)

    @commands.command(description="Toggle the queues shuffle status")
    @checks.bot_has_permissions(embed_links=True)
    async def shuffle(self, ctx: Context):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.reply(embed=em)

        player.shuffle = not player.shuffle
        em.description = f"🔀 | Shuffle {'enabled' if player.shuffle else 'disabled'}"
        await ctx.reply(embed=em)

    @commands.command(aliases=["loop"], description="Toggle the queues repeat status")
    @checks.bot_has_permissions(embed_links=True)
    async def repeat(self, ctx: Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.reply(embed=em)

        player.repeat = not player.repeat
        em.description = f"🔁 | Repeat {'enabled' if player.repeat else 'disabled'}"
        await ctx.reply(embed=em)

    @commands.command(description="Remove a track from the queue")
    @checks.bot_has_permissions(embed_links=True)
    async def remove(self, ctx: Context, index: int):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.queue:
            em.description = "Nothing queued!"
            return await ctx.reply(embed=em)

        if index > len(player.queue) or index < 1:
            em.description = f"Index has to be **between** 1 and {len(player.queue)}!"
            return await ctx.reply(embed=em)

        removed = player.queue.pop(index - 1)
        em.description = f"Removed **{removed.title}** from the queue!"
        await ctx.reply(embed=em)

    @commands.command(description="Stop the queue")
    @checks.bot_has_permissions(embed_links=True)
    async def stop(self, ctx: Context):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.reply(embed=em)

        player.queue.clear()
        await player.stop()
        em.description = "⏹ | Stopped"
        await ctx.reply(embed=em)

    @commands.command(aliases=["dc"])
    @checks.bot_has_permissions(embed_links=True)
    async def disconnect(self, ctx: Context):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild)

    @commands.command(aliases=['np', 'song'], description="Check what's playing right now!")
    @checks.bot_has_permissions(embed_links=True)
    async def now(self, ctx: Context):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.current:
            em.description = "Not playing!"
        else:
            requester = self.bot.get_user(player.current.requester)
            emoji = self.get_emoji(player.current.uri)
            status = self.draw_time(player)
            em.description = f"{emoji} **[{player.current.title}]({player.current.uri})**\n" \
                             f"**Requested by:** {requester.mention}\n" \
                             f"{status}"
            em.set_thumbnail(url=self.get_thumbnail(player.current.uri))
        await ctx.reply(embed=em)

    @commands.command(description="Skip the currently playing song")
    @checks.bot_has_permissions(embed_links=True)
    async def skip(self, ctx: Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.reply(embed=em)

        await player.skip()
        em.description = "⏭ | Skipped"
        await ctx.reply(embed=em)

    @commands.command(aliases=["q"], description="View the queue")
    @checks.bot_has_permissions(embed_links=True)
    async def queue(self, ctx: Context):
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = self.embed()

        if not player.queue:
            em.description = "**Now Playing:**\n"
            if player.current:
                requester = self.bot.get_user(player.current.requester)
                emoji = self.get_emoji(player.current.uri)
                status = self.draw_time(player)
                em.description += f"{emoji} [**{escape_markdown(player.current.title)}**]({player.current.uri})\n" \
                                  f"Requested by: {requester.mention}\n" \
                                  f"{status}\n"
                em.set_thumbnail(url=self.get_thumbnail(player.current.uri))
            else:
                em.description += "Nothing!\n"

            em.description += f"**Volume:**\n" \
                              f"{self.draw_vol(player)}\n" \
                              f"**Next in queue:**\n"

            if player.fetch("autoplay_enabled"):
                em.description += "There's nothing in the queue but you have AutoPlay enabled!"
            else:
                em.description += "There's nothing in the queue! Why not queue something?"
            em.set_footer(
                text=f"Page 1/1 •"
                     f" 1 track • {self.get_queue_time(player)} remaining\n"
                     f"Shuffle: {'✔️' if player.shuffle else '❌'} • Repeat: {'✔️' if player.repeat else '❌'} •"
                     f" Autoplay: {'✔️' if player.fetch('autoplay_enabled') else '❌'}"
            )
            return await ctx.reply(embed=em)

        queue = Queue(ctx=ctx, color=self.bot.color)
        await queue.queueinate()

    def embed(self):
        return discord.Embed(
            color=self.bot.color
        ).set_author(
            name=f"{self.bot.user.name} Music",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )

    def get_queue_time(self, player: lavalink.DefaultPlayer):
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
                queue_time_fixed = self.format_time(queue_time)
        return queue_time_fixed

    @staticmethod
    def get_thumbnail(url):
        if "youtube" in url:
            return f"https://img.youtube.com/vi/{url.split('?v=')[1]}/hqdefault.jpg"
        return ""

    def get_emoji(self, query: str):
        def emojis(path: str):
            with open("config/emojis.yml", "r") as emoji_dict:
                emoji_list = yaml.safe_load(emoji_dict)
            return self.bot.get_emoji(dictor(emoji_list, path))

        emoji = "❓"
        if "twitch.tv" in query:
            emoji = emojis("music.twitch")
        elif "soundcloud.com" in query or query.startswith("scsearch:"):
            emoji = emojis("music.soundcloud")
        elif "vimeo.com" in query:
            emoji = emojis("music.vimeo")
        elif "youtube.com" in query or "youtu.be" in query or query.startswith("ytsearch:"):
            emoji = emojis("music.youtube")
        elif "spotify.com" in query:
            emoji = emojis("music.spotify")
        return emoji

    @staticmethod
    def format_time(time):
        hours, remainder = divmod(int(time / 1000), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_formatted = f"{minutes:02d}:{seconds:02d}"
        if hours:
            time_formatted = f"{hours:02d}:" + time_formatted
        return time_formatted

    def draw_time(self, player: lavalink.DefaultPlayer):
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
            f"[{self.format_time(player.position)}/{self.format_time(player.current.duration)}]"
        return msg

    @staticmethod
    def draw_vol(player: lavalink.DefaultPlayer):
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

    def call_later(self, time, func, *args, **kwargs):
        return self.bot.loop.call_later(time, lambda: self.bot.loop.create_task(func(*args, **kwargs)))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        guild: discord.Guild = member.guild
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(guild.id)
        waiting: bool = guild.id in self.handles
        em = self.embed()
        if player and player.is_connected and before.channel != after.channel:
            if (
                    before.channel is not None
                    and before.channel.id == int(player.channel_id)
                    and len(before.channel.members) == 1
                    and not waiting
            ):
                channel: discord.TextChannel = self.bot.get_channel(player.fetch("channel"))
                await player.set_pause(True)
                em.description = "Looks like everyone has left, I  have paused and will disconnect in 1 minute!"
                msg = await channel.send(embed=em)

                handle = self.call_later(60, self.leave_vc, before.channel, player, msg)
                self.handles[guild.id] = {"future": handle, "message": msg}
            elif (
                    after.channel is not None
                    and after.channel.id == int(player.channel_id)
                    and len(after.channel.members) >= 1
                    and waiting
            ):
                await player.set_pause(False)
                em.description = "Welcome back! I have resumed the queue."
                msg = self.handles[guild.id]["message"]
                await msg.edit(embed=em)
                self.handles[guild.id]["future"].cancel()
                del self.handles[guild.id]

    async def leave_vc(self, channel, player, message):
        guild: discord.Guild = channel.guild
        em = self.embed()
        player.queue.clear()
        await player.stop()
        await player.set_pause(False)
        await self.connect_to(guild)
        em.description = "Disconnected due to inactivity."
        await message.edit(embed=em)
        del self.handles[guild.id]


def setup(bot):
    bot.add_cog(Music(bot))


class AutoPlay:
    def __init__(self):
        self.history = []

    def store(self, title: str):
        if title in self.history:
            return

        self.history.append(title)
        if len(self.history) > 5:
            self.history.pop(0)

    async def get_recommendation(self, bot):
        try:
            results = await bot.ksoftapi.music.recommendations(tracks=self.history, provider="youtube_ids")
        except (Exception, ksoftapi.NoResults):
            return False
        return results[0].youtube_link


class CannotPaginate(Exception):
    pass


class Queue:
    # TODO: Rewrite
    def __init__(self, ctx: Context, color):
        self.main = Music(ctx.bot)
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
            album_art = self.main.get_thumbnail(uri)
        self.embed.set_thumbnail(url=album_art)
        emoji = self.main.get_emoji(uri)
        volume = self.main.draw_vol(self.player)
        now_playing = self.main.draw_time(self.player)
        requester = self.bot.get_user(self.player.current.requester)
        p = [f"**Now Playing:**\n"
             f"{emoji} [**{escape_markdown(title)}**]({uri})\n"
             f"Requested by: {requester.mention}\n"
             f"{now_playing}\n"
             f"**Volume:**\n"
             f"{volume}\n"
             f"**Next in queue:**\n"
             f"`Position` `length` **[Song Title](https://www.youtube.com)**"]
        for index, entry in enumerate(entries, 1 + ((page - 1) * 10)):
            duration = "🔴 LIVE" if entry.stream else self.main.format_time(entry.duration)
            if entry.extra:
                uri = entry.extra["uri"]
                title = entry.extra["title"]
            else:
                uri = entry.uri
                title = entry.title
            emoji = self.main.get_emoji(uri)
            title_fixed = escape_markdown(title)
            cut = (title_fixed[:40] + "...") if len(title_fixed) > 27 else title_fixed
            p.append(f"`{index}.` `[{duration}]` {emoji} **[{cut}]({uri})**")

        self.embed.set_footer(
            text=f"Page {page}/{self.maximum_pages} •"
                 f" {len(self.entries)} tracks • {self.main.get_queue_time(self.player)} remaining\n"
                 f"Shuffle: {'✔️' if self.player.shuffle else '❌'} • Repeat: {'✔️' if self.player.repeat else '❌'} •"
                 f" Autoplay: {'✔️' if self.player.fetch('autoplay_enabled') else '❌'}"
        )

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
