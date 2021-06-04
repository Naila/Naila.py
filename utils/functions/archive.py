import random
import re

from discord import WebhookType, MessageType


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
        if message.webhook_id:
            webhook = await ctx.bot.fetch_webhook(message.webhook_id)
            if str(message.webhook_id) not in users:
                badge = "server" if webhook.type is WebhookType.channel_follower else "bot"
                users[str(message.webhook_id)] = {
                    "avatar": str(webhook.avatar_url_as(format="png", size=1024)),
                    "username": str(webhook.name),
                    "discriminator": "0000",
                    "badge": badge
                }
        elif str(message.author.id) not in users:
            user = await ctx.bot.fetch_user(message.author.id)
            badge = "bot" if user.bot else None
            users[str(message.author.id)] = {
                "avatar": str(user.avatar_url_as(static_format="png", size=1024)),
                "username": str(user.name),
                "discriminator": str(user.discriminator),
                "badge": badge
            }
    return users


def get_messages(data):
    messages = []
    for message in data:
        message_dict = {
            "author": str(message.author.id),
            "id": str(message.id),
            "type": message.type.value,
            "time": int(message.created_at.timestamp() * 1000)
        }
        if message.content:
            message_dict["content"] = message.content
        if message.attachments:
            message_dict["attachments"] = []
            for attachment in message.attachments:
                message_dict["attachments"].append({
                    "id": attachment.id,
                    "filename": attachment.filename,
                    "size": attachment.size,
                    "height": attachment.height,
                    "width": attachment.width,
                    "url": attachment.url,
                    "proxy_url": attachment.proxy_url
                })
        if message.embeds:
            message_dict["embeds"] = []
            for embed in message.embeds:
                message_dict["embeds"].append(embed.to_dict())
        if message.type is MessageType.premium_guild_subscription:
            message_dict["content"] = f"{message.author.mention} just boosted the server!"
        messages.append(message_dict)
    return messages


async def format_data(ctx, data: list):
    channels, roles, users = await get_mentions(ctx, data)
    users.update(await get_users(ctx, data))
    return {
        "entities": {
            "users": users,
            "channels": channels,
            "roles": roles
        },
        "messages": get_messages(data)
    }
