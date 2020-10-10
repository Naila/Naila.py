import os
from io import BytesIO

import aiohttp
from requests.exceptions import HTTPError


# https://docs.weeb.sh/
async def weeb(session, endpoint):
    async with session.get(
            url=f"https://api.weeb.sh/images/random?nsfw=False&type={endpoint}",
            headers={"Authorization": os.getenv("WEEB"),
                     "User-Agent": "Naila Discord Bot - By Kanin#0001"}
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
        return raise_for_status(resp)


async def boobbot(session, endpoint):
    async with session.get(
            url=f"https://boob.bot/api/v2/img/{endpoint}",
            headers={"key": os.getenv("BOOBBOT"),
                     "User-Agent": "Naila Discord Bot - By Kanin#0001"}
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
        return raise_for_status(resp)


# https://sheri.bot/api/
async def sheri(session, endpoint):
    async with session.get(
            url=f"https://sheri.bot/api/{endpoint}",
            headers={"Authorization": os.getenv("SHERI"),
                     "User-Agent": "Naila Discord Bot - By Kanin#0001"}
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
    return raise_for_status(resp)


# https://nekos.life/api/v2/endpoints
async def nekos(session, endpoint):
    async with session.get(
            url=f"https://nekos.life/api/v2/img/{endpoint}",
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
    return raise_for_status(resp)


async def welcomer(session, params: dict = None):
    if params:
        params = "?" + "&".join([f"{x}={y}" for x, y in params.items()])
    async with session.get(
            url=f"https://ourmainfra.me/api/v2/welcomer/{params}",
            headers={"Authorization": os.getenv("MAINFRAME_TOKEN")}
    ) as resp:
        if resp.status == 200:
            return BytesIO(await resp.read())
        return raise_for_status(resp)


async def upload_to_cdn(session, files: dict = None):
    async with session.post(
            url="https://cdn.naila.bot/upload/archive",
            headers={"Authorization": os.getenv("NAILA_CDN")},
            files=files
    ) as resp:
        if not resp.status == 200:
            return raise_for_status(resp)
        return True


async def session_get(session, url, allowed_statuses: list = None, headers: dict = None):
    allowed_statuses = allowed_statuses or [200]
    try:
        async with session.post(url, headers=headers) as resp:
            if resp.status not in allowed_statuses:
                return raise_for_status(resp)
            return resp
    except aiohttp.ClientConnectionError:
        return None


async def session_post(session, url, allowed_statuses: list = None, headers: dict = None, json: dict = None):
    allowed_statuses = allowed_statuses or [200]
    async with session.post(url, headers=headers, json=json) as resp:
        if not resp:
            return None
        if resp.status not in allowed_statuses:
            print(resp.reason)
            return None
        return resp


# Modified from https://3.python-requests.org/_modules/requests/models/#Response.raise_for_status
def raise_for_status(response, reason: str = None, status: str = None):
    reason = reason or response.reason
    status = status or response.status
    http_error_msg = ""

    if isinstance(reason, bytes):
        try:
            reason = reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = reason.decode("iso-8859-1")

    if 400 <= status < 500:
        http_error_msg = f"{status} Client Error: {reason} for url: {response.url}"

    elif 500 <= status < 600:
        http_error_msg = f"{status} Server Error: {reason} for url: {response.url}"

    if http_error_msg:
        raise HTTPError(http_error_msg, response=response)
