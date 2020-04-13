import re

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


def pagify(text: str, delims: list = None, shorten_by=8, page_length=1900):
    delims = delims or ["\n"]
    in_text = text
    page_length -= shorten_by
    while len(in_text) > page_length:
        closest_delim = max([in_text.rfind(d, 0, page_length) for d in delims])
        closest_delim = closest_delim if closest_delim != -1 else page_length
        to_send = in_text[:closest_delim]
        yield to_send
        in_text = in_text[closest_delim:]
    yield in_text


def single_quote(text: str = None):
    return f"'{text}'" if text else None


def double_quote(text: str = None):
    return f"\"{text}\"" if text else None


def bold(text: str):
    return f"**{text}**"


def escape(text: str, user_mentions: bool = True, role_mentions: bool = True, channel_mentions: bool = True):
    regex = r"@(everyone|here"
    if user_mentions:
        regex += r"|[!]?[0-9]{17,21}"
    if role_mentions:
        regex += r"|[&]?[0-9]{17,21}"
    if channel_mentions:
        regex += r"|[#]?[0-9]{17,21}"
    regex += r")"
    return re.sub(regex, "@\u200b\\1", text)


def filesize_fix(num):
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}"
        num /= 1024.0
    return f"{num:.1f}YiB"
