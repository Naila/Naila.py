__author__ = "Kanin"
__date__ = "12/23/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


def get_channels(data):
    channels = {}
    for message in data:
        if message.channel_mentions:
            for channel_mention in message.channel_mentions:
                if str(channel_mention.id) not in channels:
                    channels[str(channel_mention.id)] = {"name": channel_mention.name}
    return channels


def get_roles(data):
    roles = {}
    for message in data:
        if message.role_mentions:
            for role_mention in message.role_mentions:
                if str(role_mention.id) not in roles:
                    roles[str(role_mention.id)] = {"name": role_mention.name, "color": role_mention.color}
    return roles


async def get_users(bot, data):
    users = {}
    for message in data:
        if str(message.author.id) not in users:
            user = await bot.fetch_user(message.author.id)
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
        message_dict = {
            "author": str(message.author.id),
            "time": int(round(message.created_at.timestamp() * 1000)),
            "content": [{}]
        }
        message_dict["content"][0]["msg"] = message.content if message.content else ""
        if message.attachments:
            message_dict["content"][0]["attachments"] = [x.url for x in message.attachments]
        if message.embeds:
            embed_dict = message.embeds[0].to_dict()
            if embed_dict["type"] == "rich":
                message_dict["content"][0]["embed"] = embed_dict
        messages.append(message_dict)
    return messages


async def format_data(bot, data: list):
    out = {
        "users": await get_users(bot, data),
        "channels": get_channels(data),
        "roles": get_roles(data),
        "messages": get_messages(data)
    }
    return out
