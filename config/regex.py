import re


invite_url: re.Pattern = re.compile(r"(?:https?://)?(?:www\.)?discord(?:(?:app)?\.com/invite|\.gg)/([A-Za-z0-9-]+)")
