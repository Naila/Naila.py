import discord
from utils.functions.permissions import get_integer

bot_version = "0.0.1"

client_id = 337481187419226113

support_invite = "https://discord.gg/mUA6Kse"

intents = discord.Intents().all()

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

presences = [
    {
        "status": discord.Status.online,
        "activity": {
            "type": discord.Activity,
            "prefix": discord.ActivityType.playing,
            "text": "n!help | {GUILDS} guilds"
        }
    },
    {
        "status": discord.Status.online,
        "activity": {
            "type": discord.Activity,
            "prefix": discord.ActivityType.watching,
            "text": "you type n!help"
        }
    },
    {
        "status": discord.Status.online,
        "activity": {
            "type": discord.Activity,
            "prefix": discord.ActivityType.playing,
            "text": "n!help | {SUPPORT_INVITE}"
        }
    },
    # {
    #     "status": discord.Status.online,
    #     "activity": {
    #         "type": discord.Streaming,
    #         "url": "https://twitch.tv/KaninDev",
    #         "text": "Testing"
    #     }
    # },
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
time_format = "%A, %B %d %Y @ %I:%M%p"
