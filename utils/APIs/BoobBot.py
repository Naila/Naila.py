import os

from utils.functions.api import raise_for_status

headers = {"key": os.getenv("BOOBBOT"), "User-Agent": "Naila Discord Bot - By Kanin#0001"}


class BoobBotApi:

    @staticmethod
    async def get_image(ctx, image_type):
        url = f"https://boob.bot/api/v2/img/{image_type}"
        async with ctx.session.get(url=url, headers=headers) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            return (await resp.json())["url"]
