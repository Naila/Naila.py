from pprint import pprint

import discord


def pagify(text: str, delims: list = None, shorten_by=8, page_length=1900):
    delims = delims or ["\n"]
    in_text = text
    page_length -= shorten_by
    while len(in_text) > page_length:
        closest_delim = max(in_text.rfind(d, 0, page_length) for d in delims)
        closest_delim = closest_delim if closest_delim != -1 else page_length
        yield in_text[:closest_delim]
        in_text = in_text[closest_delim:]
    yield in_text


#  1 = SUB_COMMAND
#  2 = SUB_COMMAND_GROUP
#  3 = STRING
#  4 = INTEGER - Any integer between -2^53 and 2^53
#  5 = BOOLEAN
#  6 = USER
#  7 = CHANNEL - Includes all channel types + categories
#  8 = ROLE
#  9 = MENTIONABLE - Includes users and roles
# 10 = NUMBER - Any double between -2^53 and 2^53
# 11 = ATTACHMENT
# noinspection PyTypeChecker
def options_to_string(interaction: discord.Interaction, code: bool = False):
    data = interaction.data
    pprint(data, indent=4)
    out = ""
    for option in data["options"]:
        match option["type"]:
            case 1 | 2 | 9:
                continue
            case 3 | 4 | 5 | 10:
                if code:
                    out += f" `{option['name']}: {option['value']}`"
                else:
                    out += f" {option['name']}: {option['value']}"
            case 6:
                resolved = data["resolved"]
                user = resolved["users"][option["value"]]
                if code:
                    out += f" `{option['name']}: {user['username']} ({option["value"]})`"
                else:
                    out += f" {option['name']}: {user['username']} ({option["value"]})"
            case 7:
                resolved = data["resolved"]
                channel = resolved["channels"][option["value"]]
                if code:
                    out += f" `{option['name']}: {channel['name']} ({option["value"]})`"
                else:
                    out += f" {option['name']}: {channel['name']} ({option["value"]})"
            case 8:
                resolved = data["resolved"]
                role = resolved["roles"][option["value"]]
                if code:
                    out += f" `{option['name']}: {role['name']} ({option["value"]})`"
                else:
                    out += f" {option['name']}: {role['name']} ({option["value"]})"
            case 11:
                if code:
                    out += f" `{option['name']}: attachment`"
                else:
                    out += f" {option['name']}: attachment"
    return out
