from io import BytesIO
import json

import discord
import re
from discord.ext import commands
import random
from utils.checks import checks
from utils.functions.archive import format_data
from PIL import Image, ImageDraw, ImageFont

__author__ = "Kanin"
__date__ = "12/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"

HEX_COLOR_RE = re.compile(r"^#?([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$")
COLOR_NAMES_TO_HEX = {
    "alice_blue": "#f0f8ff",
    "antique_white": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanched_almond": "#ffebcd",
    "blue": "#0000ff",
    "blue_violet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadet_blue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflower_blue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "dark_blue": "#00008b",
    "dark_cyan": "#008b8b",
    "dark_goldenrod": "#b8860b",
    "dark_gray": "#a9a9a9",
    "dark_grey": "#a9a9a9",
    "dark_green": "#006400",
    "dark_khaki": "#bdb76b",
    "dark_magenta": "#8b008b",
    "dark_olive_green": "#556b2f",
    "dark_orange": "#ff8c00",
    "dark_orchid": "#9932cc",
    "dark_red": "#8b0000",
    "dark_salmon": "#e9967a",
    "dark_sea_green": "#8fbc8f",
    "dark_slate_blue": "#483d8b",
    "dark_slate_gray": "#2f4f4f",
    "dark_slate_grey": "#2f4f4f",
    "dark_turquoise": "#00ced1",
    "dark_violet": "#9400d3",
    "deep_pink": "#ff1493",
    "capri": "#00bfff",
    "dim_gray": "#696969",
    "dim_grey": "#696969",
    "dodger_blue": "#1e90ff",
    "firebrick": "#b22222",
    "floral_white": "#fffaf0",
    "forest_green": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghost_white": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "green-yellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hot_pink": "#ff69b4",
    "chestnut": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavender_blush": "#fff0f5",
    "lawn_green": "#7cfc00",
    "lemon_chiffon": "#fffacd",
    "light_blue": "#add8e6",
    "light_coral": "#f08080",
    "light_cyan": "#e0ffff",
    "light_goldenrod_yellow": "#fafad2",
    "light_gray": "#d3d3d3",
    "light_grey": "#d3d3d3",
    "light_green": "#90ee90",
    "light_pink": "#ffb6c1",
    "light_salmon": "#ffa07a",
    "light_sea_green": "#20b2aa",
    "light_sky_blue": "#87cefa",
    "light_slate_gray": "#778899",
    "light_slate_grey": "#778899",
    "pastel_blue": "#b0c4de",
    "light_yellow": "#ffffe0",
    "lime": "#00ff00",
    "lime_green": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "medium_aquamarine": "#66cdaa",
    "medium_blue": "#0000cd",
    "medium_orchid": "#ba55d3",
    "medium_purple": "#9370db",
    "medium_sea_green": "#3cb371",
    "medium_slate_blue": "#7b68ee",
    "medium_spring_green": "#00fa9a",
    "medium_turquoise": "#48d1cc",
    "medium_violet-red": "#c71585",
    "midnight_blue": "#191970",
    "mint_cream": "#f5fffa",
    "misty_rose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajo_white": "#ffdead",
    "navy": "#000080",
    "old_lace": "#fdf5e6",
    "olive": "#808000",
    "olive_drab": "#6b8e23",
    "orange": "#ffa500",
    "orange-red": "#ff4500",
    "orchid": "#da70d6",
    "pale_goldenrod": "#eee8aa",
    "pale_green": "#98fb98",
    "pale_turquoise": "#afeeee",
    "pale_violet-red": "#db7093",
    "papaya_whip": "#ffefd5",
    "peach_puff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powder_blue": "#b0e0e6",
    "purple": "#800080",
    "red": "#ff0000",
    "rosy_brown": "#bc8f8f",
    "royal_blue": "#4169e1",
    "saddle_brown": "#8b4513",
    "salmon": "#fa8072",
    "sandy_brown": "#f4a460",
    "sea_green": "#2e8b57",
    "seashell": "#fff5ee",
    "medium_carmine": "#a0522d",
    "silver": "#c0c0c0",
    "sky_blue": "#87ceeb",
    "slate_blue": "#6a5acd",
    "slate_gray": "#708090",
    "slate_grey": "#708090",
    "snow": "#fffafa",
    "spring_green": "#00ff7f",
    "steel_blue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "white_smoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellow-green": "#9acd32",
}


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    # @commands.command()
    # async def upload(self, ctx):
    #     """{"user": [], "bot": []}"""
    #     data = FormData()
    #     data.add_field("file", open("utils/assets/ship/heart1.png", "rb"), filename="test/testing.png")
    #     async with ctx.session.post(
    #         url="https://cdn.naila.bot/upload/archive",
    #         headers={"Authorization": "6c878e5f-6f10-4502-abff-be50cdf6e6f4"},
    #         data=data
    #     ) as resp:
    #         if resp.status != 204:
    #             resp = await resp.json()
    #             return await ctx.send(resp)
    #         await ctx.send("Uploaded!")

    @checks.is_owner()
    @commands.command(description="TEST: Archive messages")
    async def archive(self, ctx, messages: int):
        if messages > 1000:
            return await ctx.send_error("lol no")
        message_list = []
        async for message in ctx.channel.history(limit=messages):
            message_list.append(message)
        message_list = message_list[::-1]
        data = await format_data(ctx, message_list)
        data["channel_name"] = ctx.channel.name
        df = BytesIO()
        df.write(json.dumps(data, indent=2).encode("utf8"))
        df.seek(0)
        await ctx.send(file=discord.File(df, filename="data.json"))
        data = json.loads(json.dumps(data).encode("utf8"))
        resp = await self.session.post(
            "https://archive.naila.bot",
            json=data
        )
        if resp.status != 200:
            return await ctx.send_error("Something went wrong")
        resp = await resp.text(encoding="utf8")
        file = BytesIO()
        file.write(resp.encode("utf8"))
        file.seek(0)
        await ctx.send(file=discord.File(file, filename=f"{ctx.channel.name}.html"))

    @checks.is_owner()
    @commands.command(description="An embed")
    async def embed(self, ctx):
        chan = "<#483061332766097419>"
        em = discord.Embed(description=chan, title=chan)
        em.set_author(name=chan)
        em.add_field(name=chan, value=chan)
        em.set_footer(text=chan)
        await ctx.send(embed=em)

    @staticmethod
    def interpolate(color_a: tuple, color_b: tuple, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

    @staticmethod
    def closest_colour(requested_colour):
        min_colours = {}
        for name, hexa in COLOR_NAMES_TO_HEX.items():
            hexa = hexa.strip("#")
            r_c, g_c, b_c = tuple(int(hexa[i:i+2], 16) for i in (0, 2, 4))
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_colour_name(self, requested_colour):
        try:
            hexa = "#{:02x}{:02x}{:02x}".format(*requested_colour)
            color_keys = list(COLOR_NAMES_TO_HEX.keys())
            color_values = list(COLOR_NAMES_TO_HEX.values())
            closest_name = actual_name = color_keys[color_values.index(hexa)].capitalize().replace("_", " ")
        except ValueError:
            closest_name = self.closest_colour(requested_colour).capitalize().replace("_", " ")
            actual_name = None
        return actual_name, closest_name

    @checks.is_owner()
    @commands.command()
    @checks.custom_user_has_permissions(bot_owner=True)
    @checks.custom_bot_has_permissions(embed_links=True, attach_files=True)
    async def color(self, ctx, *, color: str = None):
        color = color.strip("#") if color else f"{random.randint(0, 0xFFFFFF):06x}"
        match = HEX_COLOR_RE.match(color)
        if not match:
            if color.lower().replace(" ", "_") not in COLOR_NAMES_TO_HEX:
                return await ctx.send_error("Color must be a valid hex code!")
            color = COLOR_NAMES_TO_HEX[color.lower().replace(" ", "_")]
        hex_digits = match.group(1) if match else color.strip("#")
        if len(hex_digits) == 3:
            hex_digits = "".join(2 * d for d in hex_digits)
        integer = int(hex_digits, 16)
        rgb = tuple(int(hex_digits[i:i+2], 16) for i in (0, 2, 4))
        color_name, closest_name = self.get_colour_name(rgb)
        author_name = color_name if color_name else f"Closest named color: {closest_name}"
        em = discord.Embed(color=integer)
        em.set_author(name=author_name)
        em.add_field(name="HEX:", value=f"#{hex_digits}")
        em.add_field(name="RGB:", value=str(rgb))
        em.add_field(name="Integer:", value=str(integer))
        em.set_thumbnail(url="attachment://color.png")
        em.set_image(url="attachment://gradient.png")
        color_image_create = Image.new("RGB",  (200, 200), rgb)
        color_image = BytesIO()
        color_image_create.save(color_image, "PNG")
        color_image.seek(0)
        blank = Image.new("RGB", (2200, 400), (0, 0, 0))
        dark_gradient = [self.interpolate(rgb, (0, 0, 0), t/10) for t in range(11)]
        light_gradient = [self.interpolate(rgb, (255, 255, 255), t/10) for t in range(11)]
        for i in range(11):
            coord = i * 200
            font = ImageFont.truetype("utils/assets/fonts/Smithsonian.ttf", size=32)
            dark_color = dark_gradient[i]
            dark_r, dark_g, dark_b = dark_color
            dark_hex = "#{:02x}{:02x}{:02x}".format(*dark_color)
            light_color = light_gradient[i]
            light_r, light_g, light_b = light_color
            light_hex = "#{:02x}{:02x}{:02x}".format(*light_color)
            dark_font = (0, 0, 0) if (dark_r * 0.299 + dark_g * 0.587 + dark_b * 0.114) > 186 else (255, 255, 255)
            light_font = (0, 0, 0) if (light_r * 0.299 + light_g * 0.587 + light_b * 0.114) > 186 else (255, 255, 255)
            dark_image = Image.new("RGB", (200, 200), dark_color)
            light_image = Image.new("RGB", (200, 200), light_color)
            dark_draw = ImageDraw.Draw(dark_image)
            light_draw = ImageDraw.Draw(light_image)
            dark_w, dark_h = dark_draw.textsize(dark_hex, font=font)
            light_w, light_h = light_draw.textsize(light_hex, font=font)
            dark_draw.text(((200-dark_w)/2, (200-dark_h)), dark_hex, dark_font, font)
            light_draw.text(((200-light_w)/2, (200-light_h)), light_hex, light_font, font)
            blank.paste(dark_image, (coord, 0))
            blank.paste(light_image, (coord, 200))
        gradient_image = BytesIO()
        blank.save(gradient_image, "PNG")
        gradient_image.seek(0)
        await ctx.send(
            embed=em,
            files=[
                discord.File(fp=color_image, filename="color.png"),
                discord.File(fp=gradient_image, filename="gradient.png")
            ]
        )


def setup(bot):
    bot.add_cog(Testing(bot))
