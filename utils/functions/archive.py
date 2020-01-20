import discord
import re
import random

__author__ = "Kanin"
__date__ = "12/23/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


def find_mentions(messages, mention):
    mentions = []
    regex = {
        "channel": r"<#([0-9]+)>",
        "role": r"<@&([0-9]+)>",
        "user": r"<@!?([0-9]+)>"
    }

    mention = regex[mention]

    for message in messages:
        if message.content:
            content_mentions = [int(x) for x in re.findall(mention, message.content)]
            mentions.extend(content_mentions)
        if message.embeds:
            embed_dict = message.embeds[0].to_dict()
            if embed_dict["type"] == "rich":
                embed_mentions = []
                if "description" in embed_dict:
                    embed_mentions.extend([int(x) for x in re.findall(mention, embed_dict["description"])])
                if "fields" in embed_dict:
                    for field in embed_dict["fields"]:
                        embed_mentions.extend([int(x) for x in re.findall(mention, field["value"])])
                mentions.extend(embed_mentions)
    return list(set(mentions))


async def get_mentions(ctx, messages, mention_type: str = None):
    mentions = {"channels": {}, "roles": {}, "users": {}}
    mention_type = [mention_type] if mention_type else ["channel", "role", "user"]
    for mention in mention_type:
        id_list = find_mentions(messages, mention)
        if mention == "channel":
            for channel_id in id_list:
                channel = ctx.bot.get_channel(channel_id)
                if not channel:
                    mentions["channels"][str(channel_id)] = {"name": "deleted-channel"}
                else:
                    mentions["channels"][str(channel.id)] = {"name": channel.name}
        if mention == "role":
            for role_id in id_list:
                role = ctx.guild.get_role(role_id)
                if not role:
                    mentions["roles"][str(role_id)] = {"name": "deleted-role"}
                else:
                    mentions["roles"][str(role.id)] = {"name": role.name, "color": role.color.value or 7506394}
        if mention == "user":
            for user_id in id_list:
                user = await ctx.bot.fetch_user(user_id)
                if not user:
                    mentions["users"][str(user_id)] = {
                        "username": "deleted-user",
                        "discriminator": "0000",
                        "avatar": f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 4)}.png",
                        "badge": None
                    }
                else:
                    mentions["users"][str(user_id)] = {
                        "username": str(user.name).replace('"', '\"'),
                        "discriminator": str(user.discriminator),
                        "avatar": str(user.avatar_url_as(static_format="png")),
                        "badge": "bot" if user.bot else None
                    }
    return mentions["channels"], mentions["roles"], mentions["users"]


async def get_users(ctx, data):
    users = {}
    for message in data:
        if str(message.author.id) not in users:
            user = await ctx.bot.fetch_user(message.author.id)
            badge = "bot" if user.bot else None
            users[str(message.author.id)] = {
                "avatar": str(user.avatar_url_as(static_format="png", size=1024)),
                "username": user.name,
                "discriminator": user.discriminator,
                "badge": badge
            }
    return users


def get_messages(data):
    messages = []
    for message in data:
        if message.type is discord.MessageType.default:
            message_dict = {
                "author": str(message.author.id),
                "time": int(round(message.created_at.timestamp() * 1000)),
                "content": [{}]
            }
            message_dict["content"][0]["msg"] = message.content if message.content else "Temp content, API errors if none atm"
            if message.attachments:
                message_dict["content"][0]["attachments"] = [x.url for x in message.attachments]
            if message.embeds:
                embed_dict = message.embeds[0].to_dict()
                if embed_dict["type"] == "rich":
                    message_dict["content"][0]["embed"] = embed_dict
            messages.append(message_dict)
    return messages


async def format_data(ctx, data: list):
    channels, roles, users = await get_mentions(ctx, data)
    users.update(await get_users(ctx, data))
    out = {
        "users": users,
        "channels": channels,
        "roles": roles,
        "messages": get_messages(data)
    }
    return out
