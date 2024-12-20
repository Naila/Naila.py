import os
from typing import Union

import aiohttp
import discord

BASE_URL = "https://nai.la/bot/api/v1/"
HEADERS = {"Authorization": "Bearer " + os.getenv("NAILA_KEY"), "Content-Type": "application/json"}


async def call_api(url: str, method: str, data: dict = None):
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
    return content["data"]


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
