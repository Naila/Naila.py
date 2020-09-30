import os
import random
from io import BytesIO

import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont


def ship(avatar_1, avatar_2):
    path = "utils/assets/ship/"
    background = Image.new("RGBA", (600, 200), (0, 0, 0, 0))
    avatar_1 = Image.open(requests.get(avatar_1, stream=True).raw).resize((200, 200), Image.LANCZOS).convert("RGBA")
    avatar_2 = Image.open(requests.get(avatar_2, stream=True).raw).resize((200, 200), Image.LANCZOS).convert("RGBA")
    heart = Image.open(path + random.choice([x for x in os.listdir(path)])).convert("RGBA")
    background.paste(avatar_1, (0, 0), avatar_1)
    background.paste(heart, (201, 0), heart)
    background.paste(avatar_2, (401, 0), avatar_2)
    temp_image = BytesIO()
    background.save(temp_image, "PNG")
    temp_image.seek(0)
    return temp_image


def getSuffix(num):
    return "th" if 10 <= num % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")


def getImage(url):
    return Image.open(requests.get(url, stream=True).raw)


# TODO: Rewrite this shit
def createWelcomeImage(fmt, user_name, guild_name, url, member_count, color=None):
    if not color:
        color = (255, 255, 255)
    else:
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    if fmt == "1":
        background = Image.new("RGBA", (1000, 300), (0, 0, 0, 0))
        # Initialize Image
        WelcomePicture = ImageOps.fit(background, (2000, 600))
        # Insert Background Image
        WelcomePicture = WelcomePicture.resize((2000, 600), Image.NEAREST)
        # Create Profile Picture Mask
        ProfileArea = Image.new("L", (512, 512), 0)
        draw = ImageDraw.Draw(ProfileArea)
        draw.ellipse(((0, 0), (512, 512)), fill=255)
        ProfilePicture = getImage(url)
        ProfileAreaOutput = ImageOps.fit(ProfilePicture, (512, 512))
        ProfileAreaOutput.putalpha(ProfileArea)
        drawtwo = ImageDraw.Draw(WelcomePicture)
        drawtwo.ellipse(((28, 28), (572, 572)), fill=color)
        WelcomePicture.paste(ProfileAreaOutput, (44, 44), ProfileArea)
        defaultFont = ImageFont.truetype("utils/assets/fonts/NotoSans-Bold.ttf", 80)
        smallFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", 40)
        WelcomePicture = WelcomePicture.resize((1000, 300), resample=Image.ANTIALIAS)
        drawtwo = ImageDraw.Draw(WelcomePicture)
        # CustomText
        size = 84
        text = "Welcome to {}".format(guild_name).encode("utf8")
        while defaultFont.getsize(text.decode())[0] > 700:
            size -= 1
            defaultFont = ImageFont.truetype("utils/assets/fonts/NotoSans-Bold.ttf", size)
        defaultFont = ImageFont.truetype("utils/assets/fonts/NotoSans-Bold.ttf", size)
        drawtwo.text((300, 30), text.decode(), font=defaultFont, fill=color)
        size = 60
        italicFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", size)
        text = "{}".format(user_name).encode("utf8")
        while italicFont.getsize(text.decode())[0] > 600:
            size -= 1
            italicFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", size)
        drawtwo.text((315, 125), text.decode(), font=italicFont, fill=color)
        size = 40
        text = "You are the {}{} user!".format(member_count, getSuffix(int(member_count))).encode("utf8")
        while smallFont.getsize(text.decode())[0] > 700:
            size -= 1
            smallFont = ImageFont.truetype("utils/assets/fonts/NotoSans-Regular.ttf", size)
        size -= 1
        smallFont = ImageFont.truetype("utils/assets/fonts/NotoSans-Regular.ttf", size)
        drawtwo.text((300, 220), text.decode(), font=smallFont, fill=color)
        # Save Image
        ImageObject = BytesIO()
        WelcomePicture.save(ImageObject, format="PNG")
        ImageObject.seek(0)
        return ImageObject
    elif fmt == "2":
        background = Image.new("RGBA", (1000, 500), (0, 0, 0, 0))
        bgx = 2000
        bgy = 1000
        # Find, resize, center the image
        WelcomePicture = ImageOps.fit(background, (bgx, bgy))
        WelcomePicture = WelcomePicture.resize((bgx, bgy), Image.NEAREST)
        # Create profile picture
        drawlwh = 400
        ellipsize = 28
        drawtwo1x = ((bgx / 2) - (drawlwh / 2)) - ellipsize / 2
        drawtwo1y = ellipsize
        drawtwo2x = ((bgx / 2) + (drawlwh / 2)) + ellipsize / 2
        drawtwo2y = drawlwh + ellipsize * 2
        ProfileArea = Image.new("L", (drawlwh, drawlwh), 0)
        draw = ImageDraw.Draw(ProfileArea)
        draw.ellipse(((0, 0), (drawlwh, drawlwh)), fill=255)
        ProfilePicture = getImage(url)
        ProfileAreaOutput = ImageOps.fit(ProfilePicture, (drawlwh, drawlwh))
        # WelcomePicture.paste(ProfileAreaOutput, (44, 44), ProfileArea)
        drawtwo = ImageDraw.Draw(WelcomePicture)
        # Draw ellipse behind profile picture
        drawtwo.ellipse(((drawtwo1x, drawtwo1y), (drawtwo2x, drawtwo2y)), fill=color)
        pastex = int((bgx / 2) - (drawlwh / 2))
        pastey = int(ellipsize * 1.5)
        WelcomePicture.paste(ProfileAreaOutput, (pastex, pastey), ProfileArea)
        # Resize image again
        bgx = 1000
        bgy = 500
        W, H = (bgx, bgy)
        WelcomePicture = WelcomePicture.resize((bgx, bgy), resample=Image.ANTIALIAS)
        # Custom text
        draw = ImageDraw.Draw(WelcomePicture)
        userFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", 60)
        welcomeFont = ImageFont.truetype("utils/assets/fonts/Discord.otf", 60)
        countFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", 40)
        size = 60
        text = f"{user_name}"
        while userFont.getsize(text)[0] > 500:
            size -= 1
            userFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", size)
        w, h = userFont.getsize(text)
        draw.text(((W - w) / 2, (H - h) / 2 + 20), text, font=userFont, fill=color)
        size = 60
        text = f"Welcome to {guild_name}"
        while welcomeFont.getsize(text)[0] > 800:
            size -= 1
            welcomeFont = ImageFont.truetype("utils/assets/fonts/Discord.otf", size)
        w, h = welcomeFont.getsize(text)
        draw.text(((W - w) / 2, (H - h) / 2 + 120), text, font=welcomeFont, fill=color)
        size = 40
        text = f"You are the {member_count}{getSuffix(int(member_count))} member!"
        while countFont.getsize(text)[0] > 800:
            size -= 1
            countFont = ImageFont.truetype("utils/assets/fonts/OpenSansEmoji.ttf", size)
        w, h = countFont.getsize(text)
        draw.text(((W - w) / 2, 430), text, font=countFont, fill=color)
        ImageObject = BytesIO()
        WelcomePicture.save(ImageObject, format="PNG")
        ImageObject.seek(0)
        return ImageObject
