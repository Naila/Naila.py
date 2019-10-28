import time

import discord
from rethinkdb import r

grammar_words = [{"word": "grammer", "fix": "grammar"},
                 {"word": "youre", "fix": "you're"},
                 {"word": "cant", "fix": "can't"},
                 {"word": "im", "fix": "I'm"},
                 {"word": "isnt", "fix": "isn't"},
                 {"word": "dont", "fix": "don't"},
                 {"word": "wont", "fix": "won't"},
                 {"word": "shouldnt", "fix": "shouldn't"},
                 {"word": "wouldnt", "fix": "wouldn't"},
                 {"word": "couldnt", "fix": "couldn't"},
                 {"word": "wasnt", "fix": "wasn't"},
                 {"word": "aint", "fix": "ain't"}]


async def addtodb(bot, guild: discord.Guild = None, user: discord.User = None):
    if user:
        if not await r.table("users").get(str(user.id)).run(bot.conn):
            await r.table("users").insert({
                "id": str(user.id),
                "blacklisted": False,
                "prefixes": [],
                "away": False,
                "last_seen": None,
                "xp": 0,
                "name_history": [],
                "discriminator_history": [],
                "registration_date": time.strftime(bot.config()["time_format"])
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {user} to the (users) database")
    if guild:
        if not await r.table("guilds").get(str(guild.id)).run(bot.conn):
            await r.table("guilds").insert({
                "id": str(guild.id),
                "prefixes": [],
                "fox_channels": [],
                "fox_messages": {},
                "triggers": {},
                "color": 0x80f5ff,
                "hex": "80f5ff",
                "grammar": False,
                "grammar_words": grammar_words
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {guild} to the (guilds) database")
        if not await r.table("music").get(str(guild.id)).run(bot.conn):
            await r.table("music").insert({
                "id": str(guild.id),
                "dj_role": None,
                "waiting": False
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {guild} to the (music) database")
        if not await r.table("invitemirror").get(str(guild.id)).run(bot.conn):
            await r.table("invitemirror").insert({
                "id": str(guild.id),
                "channel": None,
                "invites": {}
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {guild} to the (invitemirror) database")
        if not await r.table("welcomer").get(str(guild.id)).run(bot.conn):
            await r.table("welcomer").insert({
                "id": str(guild.id),
                "content": None,
                "enabled": True,
                "embed": True,
                "channel": None,
                "color": None,
                "background": "Transparent",
                "type": 2,
                "user_roles": [],
                "bot_roles": [],
                "banned_role": None
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {guild} to the (welcomer) database")
        if not await r.table("ReactCommands").get(str(guild.id)).run(bot.conn):
            if guild.id == 365260338851086346:
                await r.table("ReactCommands").insert({
                    "id": str(guild.id),
                    "messages": {},
                    "error_channel": None,
                    "enabled": False
                }, conflict="update").run(bot.conn)
                bot.log.info(f"Added {guild} to the (ReactCommands) database")
        if not await r.table("ModLogs").get(str(guild.id)).run(bot.conn):
            if guild.id == 365260338851086346:
                await r.table("ModLogs").insert({
                    "id": str(guild.id),
                    "channels":
                        {
                            "all": None,
                            "member": None,
                            "message": None,
                            "guild": None,
                            "mod": None
                        },
                    "embed": True
                }, conflict="update").run(bot.conn)
                bot.log.info(f"Added {guild} to the (ModLogs) database.")
        if not await r.table("Registration").get(str(guild.id)).run(bot.conn):
            await r.table("Registration").insert({
                "id": str(guild.id),
                "channel": None,
                "autoban_age": 12,
                "enabled": False
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {guild} to the (Registration) database.")
        if not await r.table("Leveler").get(str(guild.id)).run(bot.conn):
            await r.table("Leveler").insert({
                "id": str(guild.id),
                "announce": False,
                "whisper": False,
                "announce_message": "GG {USER_MENTION} on leveling up! Level: {LEVEL}",
                "level_up_channel": None,
                "banned": {
                    "roles": [],
                    "channels": []
                },
                "users": {},
                "rewards": {"default": {}}
            }, conflict="update").run(bot.conn)
            bot.log.info(f"Added {guild} to the (Leveler) database.")
