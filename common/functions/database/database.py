import os
from typing import List, Sequence, Union

import aiohttp
import discord

BASE_URL = "https://nai.la/bot/api/v1/"
HEADERS = {"Authorization": "Bearer " + os.getenv("NAILA_KEY"), "Content-Type": "application/json"}


async def call_api(url: str, method: str, data: Union[dict, list] = None):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=HEADERS, json=data) as response:
            return response, await response.json()


async def add_user(user: Union[discord.User, discord.Member]):
    url = BASE_URL + f"users/{user.id}/add"
    data = {
        "username": str(user.name),
        "display_name": str(user.global_name) if user.global_name else None,
        "avatar": str(user.avatar.key) if user.avatar else None,
    }
    _, content = await call_api(url, "POST", data)
    return content


async def add_user_bulk(users: Union[List[discord.User], Sequence[discord.Member]]):
    url = BASE_URL + "users/bulk/add"
    data = [
        {
            "id": str(user.id),
            "username": str(user.name),
            "display_name": str(user.global_name) if user.global_name else None,
            "avatar": str(user.avatar.key) if user.avatar else None,
        }
        for user in users
    ]
    _, content = await call_api(url, "POST", data)
    return content


async def get_user(user: discord.User):
    url = BASE_URL + f"users/{user.id}"
    _, content = await call_api(url, "GET")
    if content["success"]:
        return content
    return await add_user(user)


async def increment_user(user: discord.User):
    url = BASE_URL + f"users/{user.id}/increment"
    _, content = await call_api(url, "PATCH")
    if content["success"]:
        return content
    return await add_user(user)


async def update_user(user: discord.User, data: dict):
    url = BASE_URL + f"users/{user.id}/update"
    _, content = await call_api(url, "PATCH", data)
    if content["success"]:
        return content
    return await add_user(user)


async def add_guild(guild: discord.Guild):
    url = BASE_URL + f"guilds/{guild.id}/add"
    data = {
        "name": str(guild.name),
        "icon": str(guild.icon.key) if guild.icon else None,
        "owner_id": str(guild.owner.id),
    }
    _, content = await call_api(url, "POST", data)
    return content


async def get_guild(guild: discord.Guild):
    url = BASE_URL + f"guilds/{guild.id}"
    _, content = await call_api(url, "GET")
    if content["success"]:
        return content
    return await add_guild(guild)


async def increment_guild(guild: discord.Guild):
    url = BASE_URL + f"guilds/{guild.id}/increment"
    _, content = await call_api(url, "PATCH")
    if content["success"]:
        return content
    return await add_guild(guild)


async def update_guild(guild: discord.Guild, data: dict):
    url = BASE_URL + f"guilds/{guild.id}/update"
    _, content = await call_api(url, "PATCH", data)
    if content["success"]:
        return content
    return await add_guild(guild)


async def update_presence(guild: discord.Guild, presence: bool):
    url = BASE_URL + f"guilds/{guild.id}/presence"
    data = {"presence": presence}
    _, content = await call_api(url, "PATCH", data)
    return content
