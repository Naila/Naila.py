import os

from requests.exceptions import HTTPError


# https://docs.weeb.sh/
async def weeb(ctx, endpoint):
    async with ctx.session.get(
            url=f"https://api.weeb.sh/images/random?nsfw=False&type={endpoint}",
            headers={"Authorization": os.getenv("WEEB")}
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
        return raise_for_status(resp)


async def boobbot(ctx, endpoint):
    async with ctx.session.get(
            url=f"https://boob.bot/api/v2/img/{endpoint}",
            headers={"key": os.getenv("BOOBBOT")}
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
        return raise_for_status(resp)


# https://sheri.bot/api/
async def sheri(ctx, endpoint):
    async with ctx.session.get(
            url=f"https://sheri.bot/api/{endpoint}",
            headers={"Authorization": os.getenv("SHERI")}
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
    return raise_for_status(resp)


# https://nekos.life/api/v2/endpoints
async def nekos(ctx, endpoint):
    async with ctx.session.get(
            url=f"https://nekos.life/api/v2/img/{endpoint}",
    ) as resp:
        if resp.status == 200:
            return (await resp.json())["url"]
    return raise_for_status(resp)


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
