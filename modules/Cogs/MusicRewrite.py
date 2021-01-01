# import asyncio
# import os
# import re
# from decimal import Decimal, ROUND_HALF_UP
#
# import discord
# import lavalink
# import requests
# import yaml
# from dictor import dictor
# from discord.ext import commands
# from discord.utils import escape_markdown
# from ksoftapi import NoResults
# from lavalink import AudioTrack
# from bs4 import BeautifulSoup
#
# from utils.ctx import CustomContext
# from utils.functions import argparser
# from utils.functions.text import pagify
#
# url_rx = re.compile(r"https?://(?:www\.)?.+")
#
#
# class MusicRewrite(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#         if not hasattr(bot, "lavalink"):
#             bot.lavalink = lavalink.Client(bot.user.id, shard_count=bot.shard_count)
#             host = os.getenv("LAVALINK_HOST")
#             port = int(os.getenv("LAVALINK_PORT"))
#             password = os.getenv("LAVALINK_PASS")
#             bot.lavalink.add_node(host=host, port=port, password=password, region="us", name="DEFAULT US")
#             bot.lavalink.add_node(host=host, port=port, password=password, region="eu", name="DEFAULT EU")
#             bot.lavalink.add_node(host=host, port=port, password=password, region="asia", name="DEFAULT ASIA")
#             bot.add_listener(bot.lavalink.voice_update_handler, "on_socket_response")
#         bot.lavalink.add_event_hook(self.track_hook)
#
#     async def track_hook(self, event):
#         em = self.embed()
#         if isinstance(event, lavalink.events.QueueEndEvent):
#             channel = self.bot.get_channel(event.player.fetch("channel"))
#             if not channel:
#                 return
#
#             if event.player.fetch("autoplay_enabled"):
#                 autoplay = event.player.fetch("autoplay")
#                 recommendation = await autoplay.get_recommendation(self.bot)
#                 if not recommendation:
#                     return await channel.send("AutoPlay couldn't find a track based off of your last 5 songs played..")
#                 results = await event.player.node.get_tracks(recommendation)
#                 if not results:
#                     return await channel.send("AutoPlay couldn't find a track based off of your last 5 songs played..")
#
#                 track = results["tracks"][0]
#
#                 queue_time = self.get_queue_time(event.player)
#                 duration = "🔴 LIVE" if track["info"]["isStream"] else self.format_time(track["info"]["length"])
#                 emoji = self.get_emoji(track["info"]["uri"])
#                 title_fixed = escape_markdown(track["info"]["title"])
#                 em.title = "Autoplay Track Enqueued:"
#                 em.description = f"{emoji} [**{title_fixed}**]({track['info']['uri']})"
#                 em.add_field(name="Requester:", value=self.bot.user.mention)
#                 em.add_field(name="Position in queue:", value=str(len(event.player.queue)))
#                 em.add_field(name="Duration:", value=duration)
#                 em.add_field(name="Estimated time until playing:", value=queue_time)
#                 em.set_thumbnail(url=self.get_thumbnail(track["info"]["uri"]))
#                 await channel.send(embed=em)
#                 await event.player.play(AudioTrack(track, requester=self.bot.user.id))
#             else:
#                 await channel.send("Queue Ended.")
#         elif isinstance(event, lavalink.events.TrackEndEvent):
#             if "https://www.youtube.com" in event.track.uri or "https://youtu.be/" in event.track.uri:
#                 autoplay = event.player.fetch("autoplay")
#                 autoplay.store(event.track.identifier)
#         elif isinstance(event, lavalink.events.TrackStartEvent):
#             channel = self.bot.get_channel(event.player.fetch("channel"))
#
#             if not channel:
#                 return
#
#             duration = "🔴 LIVE" if event.track.stream else self.format_time(event.track.duration)
#             if event.track.extra:
#                 uri = event.track.extra["uri"]
#                 title = event.track.extra["title"]
#                 album_art = event.track.extra["album_art"]
#             else:
#                 uri = event.track.uri
#                 title = event.track.title
#                 album_art = self.get_thumbnail(uri)
#             emoji = self.get_emoji(uri)
#             requester = self.bot.get_user(event.track.requester)
#             em = self.embed()
#             em.title = "Now Playing:"
#             em.description = f"{emoji} **[{title}]({uri})**"
#             em.add_field(
#                 name="Duration:",
#                 value=duration
#             ).add_field(
#                 name="Requested by:",
#                 value=requester.mention
#             ).set_thumbnail(
#                 url=album_art
#             )
#             async for message in channel.history(limit=5):
#                 for embed in message.embeds:
#                     if message.author == self.bot.user and embed.title == "Now Playing:":
#                         return await message.edit(embed=em)
#             await channel.send(embed=em)
#
#     def cog_unload(self):
#         self.bot.lavalink._event_hooks.clear()
#
#     async def cog_before_invoke(self, ctx):
#         guild_check = ctx.guild is not None
#
#         if guild_check:
#             await self.ensure_voice(ctx)
#         return guild_check
#
#     async def ensure_voice(self, ctx):
#         player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
#         # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
#         # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
#         should_connect = ctx.command.name in ["play"]
#         no_vc = ctx.command.name in ["lyrics"]
#
#         if no_vc:
#             return True
#
#         if not ctx.author.voice or not ctx.author.voice.channel:
#             raise commands.CommandInvokeError("Join a Voice Channel first.")
#
#         channel: discord.VoiceChannel = ctx.author.voice.channel
#         permissions: discord.Permissions = channel.permissions_for(ctx.me)
#
#         if not player.is_connected:
#             if not should_connect:
#                 raise commands.CommandInvokeError("Not connected.")
#
#             if not permissions.connect:
#                 raise commands.CommandInvokeError("I need permission to connect!")
#             if not permissions.speak:
#                 raise commands.CommandInvokeError("I need permission to speak!")
#             if len(channel.members) >= channel.user_limit and not permissions.move_members:
#                 raise commands.CommandInvokeError("There's not enough room for me!")
#
#             player.store("channel", ctx.channel.id)
#             player.store("autoplay", AutoPlay())
#             player.store("autoplay_enabled", False)
#             await self.connect_to(ctx.guild, channel)
#         else:
#             if int(player.channel_id) != channel.id:
#                 raise commands.CommandInvokeError("You need to be in my Voice Channel!")
#
#     @staticmethod
#     async def connect_to(guild: discord.Guild, channel: discord.VoiceChannel = None):
#         await guild.change_voice_state(channel=channel, self_deaf=True)
#
#     @commands.command()
#     async def lyrics(self, ctx: CustomContext, *, search: str):
#         parser = argparser.Arguments()
#         parser.add_argument("search", nargs="*")
#         parser.add_argument("--spotify", "-s", action="store_true")
#         parser.add_argument("--nowplaying", "-np", action="store_true")
#         args, valid_check = parser.parse_args(search)
#         if not valid_check:
#             return await ctx.send(args)
#
#         em = discord.Embed(color=self.bot.color)
#         if args.spotify:
#             spotify = [x for x in ctx.author.activities if isinstance(x, discord.Spotify)]
#             if not spotify:
#                 return await ctx.send_error("You either don't have Spotify linked or you're not listening to anything.")
#             artists = spotify[0].artist
#             title = spotify[0].title.split("(feat.")[0]
#             search = f'{title} {artists}'
#         elif args.nowplaying:
#             player = self.bot.lavalink.player_manager.get(ctx.guild.id)
#             if not player or not player.is_playing or not player.current:
#                 return await ctx.send_error("I'm not currently playing anything!")
#             if player.current.stream:
#                 return await ctx.send_error("I can't get the lyrics of a stream..")
#             search = player.current.title
#         base_url = "http://api.genius.com"
#         url = base_url + f"/search?q={search}&page=1&per_page=1"
#         async with self.bot.session.get(url, headers={"Authorization": os.getenv("GENIUS")}) as resp:
#             result = await resp.json()
#         try:
#             result = result["response"]["hits"][0]["result"]
#         except (KeyError, IndexError):
#             return await ctx.send_error("Song not found")
#
#         response = requests.get(base_url + result["api_path"], headers={"Authorization": os.getenv("GENIUS")})
#         json = response.json()
#
#         page_url = "http://genius.com" + json["response"]["song"]["path"]
#         verif = ctx.emojis("music.checky") if result["primary_artist"]["is_verified"] is True else ""
#
#         desc = f"**Artist:** [{result['primary_artist']['name']} {verif}]({result['primary_artist']['url']})\n" \
#                f"**Song:** [{result['title_with_featured']}]({page_url})\n"
#
#         if "pageviews" in result["stats"]:
#             views = f"{result['stats']['pageviews']:,}"
#             desc += f"**Views:** {views}\n"
#
#         desc += f"**Lyric state:** {result['lyrics_state']}"
#         page = requests.get(page_url)
#         html = BeautifulSoup(page.text, "html.parser")
#         [h.extract() for h in html("script")]
#         lyrics = html.find("div", class_="lyrics").get_text()
#         desc += lyrics.replace("[", "**[").replace("]", "]**")
#         first_message = True
#         pages = list(pagify(desc))
#         pages_length = len(pages)
#         if pages_length > 5:
#             return await ctx.send("Too long to send.. will have a fix for this in the future!")
#         for index, page in enumerate(pages):
#             em.description = page
#             if first_message:
#                 em.set_thumbnail(url=result["header_image_url"])
#                 em.set_author(name=f"{result['title_with_featured']} lyrics")
#                 if pages_length == 1:
#                     em.set_footer(text="Not the song you were looking for? Add the author to your query.")
#                     if args.spotify or args.nowplaying:
#                         em.set_footer(text="")
#                     header = result["primary_artist"]["header_image_url"]
#                     if header and not header.startswith("https://assets.genius.com/images/default_avatar_"):
#                         em.set_image(url=header)
#                 first_message = False
#             else:
#                 em.set_thumbnail(url="")
#                 em.set_author(name="", icon_url="")
#                 em.set_footer(text="")
#                 em.set_image(url="")
#                 if index == pages_length - 1:
#                     em.set_footer(text="Not the song you were looking for? Add the author to your query.")
#                     if args.spotify or args.nowplaying:
#                         em.set_footer(text="")
#                     header = result["primary_artist"]["header_image_url"]
#                     if header and not header.startswith("https://assets.genius.com/images/default_avatar_"):
#                         em.set_image(url=header)
#         await ctx.send(embed=em)
#
#     @commands.command(description="Toggle the queues autoplay status | ONLY WORKS WITH YOUTUBE TRACKS")
#     async def autoplay(self, ctx):
#         player = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#
#         if not player.is_playing:
#             em.description = "Not playing!"
#             return await ctx.send(embed=em)
#
#         autoplay = player.fetch("autoplay_enabled")
#         player.store("autoplay_enabled", not autoplay)
#         em.description = f"🔄 | AutoPlay {'enabled' if not autoplay else 'disabled'}"
#         await ctx.send(embed=em)
#
#     @commands.command(aliases=['p'])
#     async def play(self, ctx, *, query: str = None):
#         player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#
#         if not query:
#             if player.paused:
#                 await player.set_pause(False)
#                 em.description = "⏯ | Resumed"
#                 return await ctx.send(embed=em)
#             return await ctx.send_help(ctx.command)
#
#         # SoundCloud searching is possible by prefixing "scsearch:" instead.
#         query = query.strip("<>")
#         if not url_rx.match(query):
#             query = f"ytsearch:{query}"
#         results = await player.node.get_tracks(query)
#
#         # Valid loadTypes are:
#         #   TRACK_LOADED    - single video/direct URL)
#         #   PLAYLIST_LOADED - direct URL to playlist)
#         #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
#         #   NO_MATCHES      - query yielded no results
#         #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
#         if not results or results["loadType"] == "NO_MATCHES":
#             em.description = "Nothing found!"
#         elif results["loadType"] == "LOAD_FAILED":
#             em.description = "Failed to load track"
#         elif results["loadType"] == "PLAYLIST_LOADED":
#             tracks = results["tracks"]
#
#             for track in tracks:
#                 player.add(requester=ctx.author.id, track=track)
#
#             em.title = "Playlist Enqueued:"
#             em.description = f"{ctx.emojis('music.youtube')}" \
#                              f" **[{results['playlistInfo']['name']}]({query})** -" \
#                              f" {len(tracks)} tracks added to the queue!"
#         elif results["loadType"] in ["TRACK_LOADED", "SEARCH_RESULT"]:
#             track = results["tracks"][0]
#
#             queue_time = self.get_queue_time(player)
#             duration = "🔴 LIVE" if track["info"]["isStream"] else self.format_time(track["info"]["length"])
#             emoji = self.get_emoji(track["info"]["uri"])
#             title_fixed = escape_markdown(track["info"]["title"])
#             em.title = "Track Enqueued:"
#             em.description = f"{emoji} [**{title_fixed}**]({track['info']['uri']})"
#             em.add_field(name="Requester:", value=ctx.author.mention)
#             em.add_field(name="Position in queue:", value=str(len(player.queue)))
#             em.add_field(name="Duration:", value=duration)
#             em.add_field(name="Estimated time until playing:", value=queue_time)
#             em.set_thumbnail(url=self.get_thumbnail(track["info"]["uri"]))
#
#             track = lavalink.models.AudioTrack(track, ctx.author.id)
#             player.add(requester=ctx.author.id, track=track)
#
#         await ctx.send(embed=em)
#
#         if not player.is_playing:
#             await player.play()
#
#     @commands.command(aliases=["resume"], description="Pauses or resumes the queue")
#     async def pause(self, ctx):
#         player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#         if not player.is_playing:
#             em.description = "Not playing!"
#         elif player.paused:
#             await player.set_pause(False)
#             em.description = "⏯ | Resumed"
#         else:
#             await player.set_pause(True)
#             em.description = "⏯ | Paused"
#         await ctx.send(embed=em)
#
#     @commands.command(description="Stop the queue")
#     async def stop(self, ctx):
#         player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#
#         if not player.is_playing:
#             em.description = "Not playing!"
#             return await ctx.send(embed=em)
#
#         player.queue.clear()
#         await player.stop()
#         em.description = "⏹ | Stopped"
#         await ctx.send(embed=em)
#
#     @commands.command(aliases=["dc"])
#     async def disconnect(self, ctx):
#         player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         player.queue.clear()
#         await player.stop()
#         await self.connect_to(ctx.guild)
#
#     @commands.command(aliases=['np', 'song'], description="Check what's playing right now!")
#     async def now(self, ctx):
#         player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#
#         if not player.current:
#             em.description = "Not playing!"
#         else:
#             requester = self.bot.get_user(player.current.requester)
#             emoji = self.get_emoji(player.current.uri)
#             status = self.draw_time(player)
#             em.description = f"{emoji} **[{player.current.title}]({player.current.uri})**\n" \
#                              f"**Requested by:** {requester.mention}\n" \
#                              f"{status}"
#             em.set_thumbnail(url=self.get_thumbnail(player.current.uri))
#         await ctx.send(embed=em)
#
#     @commands.command(description="Skip the currently playing song")
#     async def skip(self, ctx):
#         player = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#
#         if not player.is_playing:
#             em.description = "Not playing!"
#             return await ctx.send(embed=em)
#
#         await player.skip()
#         em.description = "⏭ | Skipped"
#         await ctx.send(embed=em)
#
#     @commands.command(aliases=["q"], description="View the queue")
#     async def queue(self, ctx):
#         player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         em = self.embed()
#
#         if not player.queue:
#             em.description = "There's nothing in the queue! Why not queue something?"
#             if player.fetch("autoplay_enabled"):
#                 em.description = "There's nothing in the queue but you have AutoPlay enabled!"
#             return await ctx.send(embed=em)
#
#         queue = Queue(ctx=ctx, color=self.bot.color)
#         await queue.queueinate()
#
#     def embed(self):
#         return discord.Embed(
#             color=self.bot.color
#         ).set_author(
#             name=f"{self.bot.user.name} Music",
#             icon_url=self.bot.user.avatar_url_as(static_format="png")
#         ).set_footer(
#             text="Music will be a premium feature soon! Enjoy it while it's here!"
#         )
#
#     def get_queue_time(self, player: lavalink.DefaultPlayer):
#         queue_time = 0
#         queue_time_fixed = "Now!"
#         for song in player.queue:
#             if song.stream:
#                 queue_time_fixed = "Unknown"
#             queue_time += song.duration
#         if player.is_playing:
#             if player.current.stream:
#                 queue_time_fixed = "Unknown"
#             queue_time += player.current.duration - player.position
#             if queue_time_fixed != "Unknown":
#                 queue_time_fixed = self.format_time(queue_time)
#         return queue_time_fixed
#
#     @staticmethod
#     def get_thumbnail(url):
#         if "youtube" in url:
#             return f"https://img.youtube.com/vi/{url.split('?v=')[1]}/default.jpg"
#         return ""
#
#     def get_emoji(self, query: str):
#         def emojis(path: str):
#             with open("config/emojis.yml", "r") as emoji_dict:
#                 emoji_list = yaml.safe_load(emoji_dict)
#             return self.bot.get_emoji(dictor(emoji_list, path))
#
#         emoji = "❓"
#         if "twitch.tv" in query:
#             emoji = emojis("music.twitch")
#         elif "soundcloud.com" in query or query.startswith("scsearch:"):
#             emoji = emojis("music.soundcloud")
#         elif "vimeo.com" in query:
#             emoji = emojis("music.vimeo")
#         elif "mixer.com" in query or "beam.pro" in query:
#             emoji = emojis("music.mixer")
#         elif "youtube.com" in query or "youtu.be" in query or query.startswith("ytsearch:"):
#             emoji = emojis("music.youtube")
#         elif "spotify.com" in query:
#             emoji = emojis("music.spotify")
#         return emoji
#
#     @staticmethod
#     def format_time(time):
#         hours, remainder = divmod(int(time / 1000), 3600)
#         minutes, seconds = divmod(remainder, 60)
#         time_formatted = f"{minutes:02d}:{seconds:02d}"
#         if hours:
#             time_formatted = f"{hours:02d}:" + time_formatted
#         return time_formatted
#
#     def draw_time(self, player: lavalink.DefaultPlayer):
#         time = Decimal(
#             str((player.position / player.current.duration) * 13)
#         ).quantize(
#             Decimal("1"),
#             rounding=ROUND_HALF_UP
#         )
#         time = time or 1
#         msg = "|"
#         for i in range(13):
#             i += 1
#             msg += "🔘" if i == time else "▬"
#         msg += "| "
#         msg += "⏸ " if player.paused else "▶ "
#         msg += "[🔴 LIVE]" if player.current.stream else \
#             f"[{self.format_time(player.position)}/{self.format_time(player.current.duration)}]"
#         return msg
#
#     @staticmethod
#     def draw_vol(player: lavalink.DefaultPlayer):
#         volume = Decimal(
#             str((player.volume / 200) * 13)
#         ).quantize(
#             Decimal("1"),
#             rounding=ROUND_HALF_UP
#         )
#         volume = volume or 1
#         emoji = "🔇" if player.volume == 0 else "🔉" if player.volume <= 100 else "🔊"
#         msg = "|"
#         for i in range(13):
#             i += 1
#             msg += "🔘" if i == volume else "▬"
#         msg += "| "
#         msg += emoji
#         msg += f" {int(player.volume / 2)}%"
#         return msg
#
#
# def setup(bot):
#     bot.add_cog(MusicRewrite(bot))
#
#
# class AutoPlay:
#     def __init__(self):
#         self.history = []
#
#     def store(self, title: str):
#         if title in self.history:
#             return
#
#         self.history.append(title)
#         if len(self.history) > 5:
#             self.history.pop(0)
#
#     async def get_recommendation(self, bot):
#         try:
#             results = await bot.kclient.music.recommendations(tracks=self.history, provider="youtube_ids")
#         except (Exception, NoResults):
#             return False
#         return results[0].youtube_link
#
#
# class CannotPaginate(Exception):
#     pass
#
#
# class Queue:
#     # TODO: Rewrite
#     def __init__(self, ctx, color):
#         self.main = MusicRewrite(ctx.bot)
#         self.bot = ctx.bot
#         self.ctx = ctx
#         self.player = self.bot.lavalink.player_manager.get(ctx.guild.id)
#         self.entries = self.player.queue
#         self.message = ctx.message
#         self.current_page = None
#         self.match = None
#         pages, left_over = divmod(len(self.entries), 10)
#         if left_over:
#             pages += 1
#         self.maximum_pages = pages
#         self.permissions = ctx.channel.permissions_for(ctx.guild.me)
#         self.embed = discord.Embed(colour=color, title=f"Queue for {ctx.guild.name}")
#         self.paginating = len(self.player.queue) > 10
#         self.reaction_emojis = [
#             ("⏮️", self.first_page),
#             ("◀️", self.previous_page),
#             ("▶️", self.next_page),
#             ("⏭️", self.last_page),
#             ("🔢", self.numbered_page),
#             ("⏹️", self.stop_pages),
#         ]
#
#         if self.paginating:
#             # verify we can actually use the pagination session
#             if not self.permissions.add_reactions:
#                 raise CannotPaginate("Bot does not have add reactions permission.")
#
#             if not self.permissions.read_message_history:
#                 raise CannotPaginate("Bot does not have Read Message History permission.")
#
#     def get_page(self, page):
#         base = (page - 1) * 10
#         return self.entries[base:base + 10]
#
#     async def show_page(self, page, *, first=False):
#         self.current_page = page
#         self.embed.set_author(icon_url=self.bot.user.avatar_url, name="Naila Music")
#         entries = self.get_page(page)
#         if self.player.current.extra:
#             uri = self.player.current.extra["uri"]
#             title = self.player.current.extra["title"]
#             album_art = self.player.current.extra["album_art"]
#         else:
#             uri = self.player.current.uri
#             title = self.player.current.title
#             album_art = self.main.get_thumbnail(uri)
#         self.embed.set_thumbnail(url=album_art)
#         emoji = self.main.get_emoji(uri)
#         volume = self.main.draw_vol(self.player)
#         now_playing = self.main.draw_time(self.player)
#         requester = self.bot.get_user(self.player.current.requester)
#         p = [f"**Now Playing:**\n"
#              f"{emoji} [**{escape_markdown(title)}**]({uri})\n"
#              f"Requested by: {requester.mention}\n"
#              f"{now_playing}\n"
#              f"**Volume:**\n"
#              f"{volume}\n"
#              f"**Next in queue:**\n"
#              f"`Position` `length` **[Song Title](https://www.youtube.com)**"]
#         for index, entry in enumerate(entries, 1 + ((page - 1) * 10)):
#             duration = "🔴 LIVE" if entry.stream else self.main.format_time(entry.duration)
#             if entry.extra:
#                 uri = entry.extra["uri"]
#                 title = entry.extra["title"]
#             else:
#                 uri = entry.uri
#                 title = entry.title
#             emoji = self.main.get_emoji(uri)
#             title_fixed = escape_markdown(title)
#             cut = (title_fixed[:40] + "...") if len(title_fixed) > 27 else title_fixed
#             p.append(f"`{index}.` `[{duration}]` {emoji} **[{cut}]({uri})**")
#
#         self.embed.set_footer(
#             text=f"Page {page}/{self.maximum_pages} •"
#                  f" {len(self.entries)} tracks • {self.main.get_queue_time(self.player)} remaining\n"
#                  f"Shuffle: {'✔️' if self.player.shuffle else '❌'} • Repeat: {'✔️' if self.player.repeat else '❌'} •"
#                  f" Autoplay: {'✔️' if self.player.fetch('autoplay_enabled') else '❌'}"
#         )
#
#         if not self.paginating:
#             self.embed.description = "\n".join(p)
#             return await self.ctx.channel.send(embed=self.embed)
#
#         if not first:
#             self.embed.description = "\n".join(p)
#             await self.message.edit(embed=self.embed)
#             return
#
#         self.embed.description = "\n".join(p)
#         self.message = await self.ctx.channel.send(embed=self.embed)
#         for (reaction, _) in self.reaction_emojis:
#             if self.maximum_pages == 2 and reaction in ("⏮️", "⏭️"):
#                 continue
#
#             await self.message.add_reaction(reaction)
#
#     async def checked_show_page(self, page):
#         if page != 0 and page <= self.maximum_pages:
#             await self.show_page(page)
#
#     async def first_page(self):
#         """goes to the first page"""
#         await self.show_page(1)
#
#     async def last_page(self):
#         """goes to the last page"""
#         await self.show_page(self.maximum_pages)
#
#     async def next_page(self):
#         """goes to the next page"""
#         await self.checked_show_page(self.current_page + 1)
#
#     async def previous_page(self):
#         """goes to the previous page"""
#         await self.checked_show_page(self.current_page - 1)
#
#     async def numbered_page(self):
#         """lets you type a page number to go to"""
#         to_delete = [await self.ctx.channel.send("What page do you want to go to?")]
#
#         def message_check(m):
#             return m.author.id == self.ctx.author.id and self.ctx.channel == m.channel and m.content.isdigit()
#
#         try:
#             msg = await self.bot.wait_for("message", check=message_check, timeout=30.0)
#         except asyncio.TimeoutError:
#             to_delete.append(await self.ctx.channel.send("Took too long."))
#             await asyncio.sleep(5)
#         else:
#             page = int(msg.content)
#             to_delete.append(msg)
#             if page != 0 and page <= self.maximum_pages:
#                 await self.show_page(page)
#             else:
#                 to_delete.append(await self.ctx.channel.send(f"Invalid page given. ({page}/{self.maximum_pages})"))
#                 await asyncio.sleep(5)
#
#         await self.ctx.channel.delete_messages(to_delete)
#
#     async def stop_pages(self):
#         """stops the interactive pagination session"""
#         await self.message.clear_reactions()
#         self.paginating = False
#
#     def react_check(self, reaction, user):
#         if user is None or user.id != self.ctx.author.id:
#             return False
#
#         if reaction.message.id != self.message.id:
#             return False
#
#         for (emojis, func) in self.reaction_emojis:
#             if reaction.emoji == emojis:
#                 self.match = func
#                 return True
#         return False
#
#     async def queueinate(self):
#         """Actually paginate the entries and run the interactive loop if necessary."""
#         first_page = self.show_page(1, first=True)
#         if not self.paginating:
#             await first_page
#         else:
#             # allow us to react to reactions right away if we're paginating
#             self.bot.loop.create_task(first_page)
#
#         while self.paginating:
#             try:
#                 reaction, user = await self.bot.wait_for('reaction_add', check=self.react_check, timeout=120.0)
#             except asyncio.TimeoutError:
#                 self.paginating = False
#                 try:
#                     await self.message.clear_reactions()
#                     break
#                 except (discord.HTTPException, discord.Forbidden):
#                     break
#
#             try:
#                 await self.message.remove_reaction(reaction, user)
#             except (discord.HTTPException, discord.Forbidden):
#                 pass
#
#             await self.match()
