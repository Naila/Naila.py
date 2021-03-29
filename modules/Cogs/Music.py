import asyncio
import os
import re

import lavalink
from discord.ext import commands
from discord.utils import escape_markdown
from lavalink import AudioTrack

from utils.functions.music import Queue, draw_time, draw_vol, ensure_voice, enqueue_and_send, disconnect, \
    format_time, get_emoji, embed, get_thumbnail

url_rx = re.compile("https?://(?:www\\.)?.+")
emojis = {
    "numbers": ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"],
    "utility": ["❌"]
}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(bot.user.id)
            host = os.getenv("LAVALINK_HOST")
            port = int(os.getenv("LAVALINK_PORT"))
            password = os.getenv("LAVALINK_PASS")
            bot.lavalink.add_node(host=host, port=port, password=password, region="us", name="DEFAULT US")
            bot.lavalink.add_node(host=host, port=port, password=password, region="eu", name="DEFAULT EU")
            bot.lavalink.add_node(host=host, port=port, password=password, region="asia", name="DEFAULT ASIA")
            bot.add_listener(bot.lavalink.voice_update_handler, "on_socket_response")

        bot.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check:
            await ensure_voice(self.bot, ctx)

        return guild_check

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            channel = self.bot.get_channel(event.player.fetch("channel"))

            if not channel:
                return

            await asyncio.sleep(1)

            autoplay_enabled = event.player.fetch("autoplay_enabled")
            if autoplay_enabled:
                autoplay = event.player.fetch("autoplay")
                recommendation = await autoplay.get_recommendation(self.bot)
                if not recommendation:
                    return await channel.send("AutoPlay couldn't find a track based off of your last 5 songs played.."
                                              " sorry for the inconvenience!")
                results = await event.player.node.get_tracks(recommendation)
                if not results:
                    return await channel.send("AutoPlay couldn't find a track based off of your last 5 songs played.."
                                              " sorry for the inconvenience!")
                await event.player.play(AudioTrack(results["tracks"][0], requester=self.bot.user.id))
            # await channel.send("Queue ended")
            # return await disconnect(self.bot, int(event.player.guild_id))
        elif isinstance(event, lavalink.events.TrackStartEvent):
            channel = self.bot.get_channel(event.player.fetch("channel"))

            if not channel:
                return

            duration = "🔴 LIVE" if event.track.stream else format_time(event.track.duration)
            if event.track.extra:
                uri = event.track.extra["uri"]
                title = event.track.extra["title"]
                album_art = event.track.extra["album_art"]
            else:
                uri = event.track.uri
                title = event.track.title
                album_art = get_thumbnail(uri)
            emoji = get_emoji(self.bot, uri)
            requester = self.bot.get_user(event.track.requester)
            em = await embed(self.bot, channel.guild.id)
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
                for embd in message.embeds:
                    if message.author == self.bot.user and embd.title == "Now Playing:":
                        return await message.edit(embed=em)
            return await channel.send(embed=em)
        elif isinstance(event, lavalink.events.TrackEndEvent):
            if "https://www.youtube.com" in event.track.uri or "https://youtu.be/" in event.track.uri:
                autoplay = event.player.fetch("autoplay")
                autoplay.store(event.track.identifier)

    @commands.command(description="Play some music! Or resumes the queue")
    async def play(self, ctx, *, query: str = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)
        if query is None:
            if player.paused:
                await player.set_pause(False)
                em.description = "⏯ | Resumed"
                return await ctx.send(embed=em)
            return await ctx.send_help(ctx.command)

        await enqueue_and_send(self.bot, ctx, query=query)

    @commands.command(description="Search for a track on YouTube")
    async def search(self, ctx, *, query):
        query = query.strip("<>")
        if url_rx.match(query):
            return await ctx.send_error("Search must be a string! Not a url!")
        query = f"ytsearch:{query}"
        results = await self.bot.lavalink.get_tracks(query)
        if not results or not results["tracks"]:
            return await ctx.send("Nothing found!")
        tracks = results["tracks"]
        tracks_len = 10 if len(tracks) >= 10 else len(tracks)
        search_list = ""
        for i, track in enumerate(tracks[0:10], start=0):
            emoji = emojis["numbers"][i]
            track_title = escape_markdown(tracks[i]["info"]["title"])
            search_list += f"{emoji} [**{track_title}**]({tracks[i]['info']['uri']})\n"
        em = await embed(self.bot, ctx.guild.id)
        em.title = "Tracks Found:"
        em.description = search_list
        em.set_footer(text=f"Showing top {tracks_len} results, ❌ to cancel.")
        message = await ctx.send(embed=em)
        for emoji in range(tracks_len):
            await message.add_reaction(emojis["numbers"][emoji])
        for emoji in emojis["utility"]:
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
            if reaction.emoji in emojis["numbers"]:
                await message.clear_reactions()
                return await enqueue_and_send(self.bot, ctx, track=tracks[emojis["numbers"].index(reaction.emoji)])

    @commands.command(aliases=["resume"], description="Pauses or resumes the queue")
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)
        if not player.is_playing:
            em.description = "Not playing!"
        elif player.paused:
            await player.set_pause(False)
            em.description = "⏯ | Resumed"
        else:
            await player.set_pause(True)
            em.description = "⏯ | Paused"
        await ctx.send(embed=em)

    @commands.command(description="Seek through a track in seconds or by time string")
    async def seek(self, ctx, time):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.send(embed=em)

        time_list = time.split(":")
        if len(time_list) >= 5:
            em.description = "Cannot seek this far!"
            return await ctx.send(embed=em)

        seconds = sum(x * int(t) for x, t in zip([1, 60, 3600, 86400], reversed(time_list)))
        milliseconds = seconds * 1000
        if milliseconds > player.current.duration:
            em.description = "Time cannot be longer than the song!"
        else:
            await player.seek(milliseconds)
            em.description = f"Moved track to **{format_time(milliseconds)}**"
        await ctx.send(embed=em)

    @commands.command(description="Skip the currently playing song")
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.send(embed=em)

        await player.skip()
        em.description = "⏭ | Skipped"
        await ctx.send(embed=em)

    @commands.command(description="Stop the queue")
    async def stop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.send(embed=em)

        player.queue.clear()
        await player.stop()
        em.description = "⏹ | Stopped"
        await ctx.send(embed=em)

    @commands.command(aliases=['np', 'song'], description="Check what's playing right now!")
    async def now(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)
        if not player.current:
            em.description = "Not playing!"
        else:
            requester = self.bot.get_user(player.current.requester)
            emoji = get_emoji(self.bot, player.current.uri)
            status = draw_time(self.bot, ctx)
            em.description = f"{emoji} **[{player.current.title}]({player.current.uri})**\n" \
                             f"**Requested by:** {requester.mention}\n" \
                             f"{status}"
            em.set_thumbnail(url=get_thumbnail(player.current.uri))
        await ctx.send(embed=em)

    @commands.command(description="Get information on a song in the queue")
    async def songinfo(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)
        if not player.queue:
            em.description = "There's nothing in the queue! Why not queue something?"
            return await ctx.send(embed=em)
        if index > len(player.queue) or index < 1:
            em.description = "Index has to be > 1 and < the queue size!"
            return await ctx.send(embed=em)
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
            estimated_time = format_time(estimated_time)
        song = player.queue[index]
        requester = self.bot.get_user(song.requester)
        duration = "🔴 LIVE" if song.stream else format_time(song.duration)
        emoji = get_emoji(self.bot, song.uri)
        em.title = "Track info:"
        em.description = f"{emoji} [**{escape_markdown(song.title)}**]({song.uri})"
        em.add_field(name="Requester:", value=requester.mention)
        em.add_field(name="Duration:", value=duration)
        em.add_field("Estimated time until playing:", value=estimated_time)
        em.set_thumbnail(url=get_thumbnail(song.uri))
        await ctx.send(embed=em)

    @commands.command(aliases=["vol"], description="View or set the volume")
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)
        if not volume and volume != 0:
            em.add_field(name="Volume:", value=draw_vol(self.bot, ctx))
            return await ctx.send(embed=em)
        if volume == 0:
            await player.set_volume(volume)
        elif volume >= 100:
            await player.set_volume(200)
        else:
            await player.set_volume(volume * 2)
        em.add_field(name="Volume set:", value=draw_vol(self.bot, ctx))
        await ctx.send(embed=em)

    @commands.command(description="Toggle the queues shuffle status")
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.send(embed=em)

        player.shuffle = not player.shuffle
        em.description = f"🔀 | Shuffle {'enabled' if player.shuffle else 'disabled'}"
        await ctx.send(embed=em)

    @commands.command(aliases=["loop"], description="Toggle the queues repeat status")
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.send(embed=em)

        player.repeat = not player.repeat
        em.description = f"🔁 | Repeat {'enabled' if player.repeat else 'disabled'}"
        await ctx.send(embed=em)

    @commands.command(description="Toggle the queues autoplay status | ONLY WORKS WITH YOUTUBE TRACKS")
    async def autoplay(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_playing:
            em.description = "Not playing!"
            return await ctx.send(embed=em)

        autoplay = player.fetch("autoplay_enabled")
        player.store("autoplay_enabled", not autoplay)
        em.description = f"🔄 | AutoPlay {'enabled' if not autoplay else 'disabled'}"
        await ctx.send(embed=em)

    @commands.command(description="Remove a track from the queue")
    async def remove(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.queue:
            em.description = "Nothing queued!"
            return await ctx.send(embed=em)

        if index > len(player.queue) or index < 1:
            em.description = f"Index has to be **between** 1 and {len(player.queue)}!"
            return await ctx.send(embed=em)

        removed = player.queue.pop(index - 1)
        em.description = f"Removed **{removed.title}** from the queue!"
        await ctx.send(embed=em)

    @commands.command(aliases=["q"], description="View the queue")
    async def queue(self, ctx):
        """View the queue"""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.queue:
            em.description = "There's nothing in the queue! Why not queue something?"
            return await ctx.send(embed=em)

        queue = Queue(ctx=ctx, color=await ctx.guildcolor())
        await queue.queueinate()

    @commands.command(name="disconnect", aliases=["dc"], description="Disconnect the bot from the voice channel")
    async def music_disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        em = await embed(self.bot, ctx.guild.id)

        if not player.is_connected:
            em.description = "Not connected."
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("You're not in my voice channel!")
        player.queue.clear()
        await player.stop()
        await disconnect(self.bot, ctx.guild.id)
        em.description = "Disconnected."
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Music(bot))
