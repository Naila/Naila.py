import discord
from utils.functions.permissions import get_integer

bot_version = "0.0.1"

client_id = 337481187419226113

support_invite = "https://discord.gg/WXGHfHH"

permissions = discord.Permissions(get_integer(
    [
        "CREATE_INSTANT_INVITE",
        "READ_MESSAGE_HISTORY",
        "USE_EXTERNAL_EMOJIS",
        "CHANGE_NICKNAME",
        "VIEW_AUDIT_LOG",
        "SEND_MESSAGES",
        "ATTACH_FILES",
        "EMBED_LINKS",
        "CONNECT",
        "SPEAK",
    ]
))

owners = [
    173237945149423619  # Kanin | Please keep my ID here
]

colors = {
    "main": 0x009696,
    "error": 0xe74c3c
}

prefixes = {
    "main": [
        "n!"
    ],
    "debug": [
        "n!!"
    ]
}

# https://strftime.org/
time_format = "%A, %B %d %Y @ %I:%M%p %Z"
