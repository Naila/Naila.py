import os
import random
from io import BytesIO

import requests
from PIL import Image

__author__ = "Kanin"
__date__ = "11/24/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class Images:

    @staticmethod
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
