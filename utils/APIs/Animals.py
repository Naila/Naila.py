import os
from random import choice

from utils.functions.api import raise_for_status
from utils.functions.text import pagify


class Animal:
    def __init__(self, ctx):
        self.session = ctx.session
        self.endpoints = {
            "images": {
                "bear": [{"url": "https://and-here-is-my-code.glitch.me/img/bear", "key": "Link"}],
                "bird": [{"url": "https://some-random-api.ml/img/birb", "key": "link"}],
                "dolphin": [{"url": "https://and-here-is-my-code.glitch.me/img/dolphin", "key": "Link"}],
                "duck": [{"url": "https://random-d.uk/api/v2/quack", "key": "url"}],  # {"url": "https://and-here-is-my-code.glitch.me/img/duck", "key": "Link"},
                "elephant": [{"url": "https://and-here-is-my-code.glitch.me/img/elephant", "key": "Link"}],
                "fox": [{"url": "https://some-random-api.ml/img/fox", "key": "link"}],
                "giraffe": [{"url": "https://and-here-is-my-code.glitch.me/img/giraffe", "key": "Link"}],
                "hippo": [{"url": "https://and-here-is-my-code.glitch.me/img/hippo", "key": "Link"}],
                "horse": [{"url": "https://and-here-is-my-code.glitch.me/img/horse", "key": "Link"}],
                "killerwhale": [{"url": "https://and-here-is-my-code.glitch.me/img/killerwhale", "key": "Link"}],
                "koala": [{"url": "https://some-random-api.ml/img/koala", "key": "link"}],
                "lion": [{"url": "https://and-here-is-my-code.glitch.me/img/lion", "key": "Link"}],
                "panda": [{"url": "https://some-random-api.ml/img/panda", "key": "link"}],  # {"url": "https://and-here-is-my-code.glitch.me/img/panda", "key": "Link"},
                "pig": [{"url": "https://and-here-is-my-code.glitch.me/img/pig", "key": "Link"}],
                "redpanda": [{"url": "https://some-random-api.ml/img/red_panda", "key": "link"}],
                "shark": [{"url": "https://and-here-is-my-code.glitch.me/img/shark", "key": "Link"}],
                "snake": [{"url": "https://and-here-is-my-code.glitch.me/img/snakes", "key": "Link"}],
                "spider": [{"url": "https://and-here-is-my-code.glitch.me/img/spiders", "key": "Link"}],
                "turtle": [{"url": "https://and-here-is-my-code.glitch.me/img/turtle", "key": "Link"}],
            },
            "facts": {
                "bear": [{"url": "https://and-here-is-my-code.glitch.me/facts/bear", "key": "Link"}],
                "bird": [{"url": "https://some-random-api.ml/facts/bird", "key": "fact"}],
                "fox": [{"url": "https://some-random-api.ml/facts/fox", "key": "fact"}],
                "giraffe": [{"url": "https://and-here-is-my-code.glitch.me/facts/giraffe", "key": "Link"}],
                "koala": [{"url": "https://some-random-api.ml/facts/koala", "key": "fact"}],
                "lion": [{"url": "https://and-here-is-my-code.glitch.me/facts/lion", "key": "Link"}],
                "panda": [{"url": "https://some-random-api.ml/facts/panda", "key": "fact"}],
                "shark": [{"url": "https://and-here-is-my-code.glitch.me/facts/shark", "key": "Link"}],
                "snake": [{"url": "https://and-here-is-my-code.glitch.me/facts/snake", "key": "Link"}]
            }
        }

    async def image(self, animal: str):
        endpoint = choice(self.endpoints["images"][animal])
        async with self.session.get(
                url=endpoint["url"]
        ) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            return (await resp.json())[endpoint["key"]]

    async def fact(self, animal: str):
        endpoint = choice(self.endpoints["facts"][animal])
        async with self.session.get(
                url=endpoint["url"]
        ) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            return (await resp.json())[endpoint["key"]]


class Cat:
    def __init__(self, ctx):
        self.session = ctx.session
        self.base = "https://api.thecatapi.com/v1/"
        self.traits = [
            "Experimental",
            "Hairless",
            "Natural",
            "Rare",
            "Rex",
            "Suppressed tail",
            "Short legs",
            "Hypoallergenic",
            "Indoor",
            "Lap"
        ]
        self.scale = [
            "Adaptability",
            "Affection level",
            "Child friendly",
            "Dog friendly",
            "Energy level",
            "Grooming",
            "Health issues",
            "Intelligence",
            "Shedding level",
            "Social needs",
            "Stranger friendly",
            "Vocalisation"
        ]

    async def image(self, breed: str = None):
        url = self.base + "images/search?has_breeds=1"
        if breed:
            breeds = {}
            async with self.session.get(
                    url=self.base + "breeds",
                    headers={"x-api-key": os.getenv("CAT")}
            ) as resp:
                if resp.status != 200:
                    return raise_for_status(resp)
                breed_list = await resp.json()
            for x in breed_list:
                breeds[x["name"].lower()] = x["id"]
            if breed.lower() not in breeds:
                return None, None, None
            url += f"&breed_id={breeds[breed.lower()]}"
        async with self.session.get(
                url=url,
                headers={"x-api-key": os.getenv("CAT")}
        ) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            resp = (await resp.json())[0]
            details = ""
            traits = []
            urls = {}
            for x, y in resp["breeds"][0].items():
                if x not in ["id", "name", "country_codes", "country_code"]:
                    x = x.capitalize().replace("_", " ")
                    if x in ["Cfa url", "Vetstreet url", "Vcahospitals url", "Wikipedia url"]:
                        x = x.split(" ")[0].replace("Cfa", "CFA").replace("Vcahospitals", "VCA Hospitals")
                        urls[x] = y.replace("(", "").replace(")", "")
                    elif x == "Origin":
                        origin = f"**{x}:** {y} ({resp['breeds'][0]['country_code']})\n"
                    elif x == "Weight":
                        weight = f"**{x}:** {y['imperial']}lb ({y['metric']}kg)\n"
                    elif x == "Life span":
                        details += f"**{x}:** {y} years\n"
                    elif x in self.traits:
                        if y == 1:
                            traits.append(x)
                    elif x in self.scale:
                        y = str(y).replace("1", "Bad").replace("2", "Poor").replace("3", "Average") \
                            .replace("4", "Above average").replace("5", "Good")
                        details += f"**{x}:** {y}\n"
                    else:
                        details += f"**{x}:** {y}\n"
            details = origin + details
            details += f"**Traits:** {', '.join(traits)}\n" if traits else ""
            details += weight
            if urls:
                details += f"**URLs:** {' • '.join([f'[{x}]({y})' for x, y in urls.items()])}"
            return resp["url"], resp["breeds"][0]["name"], details

    async def breeds(self):
        async with self.session.get(
                url=self.base + "breeds",
                headers={"x-api-key": os.getenv("CAT")}
        ) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            breed_list = await resp.json()
        breeds = [x["name"] for x in breed_list]
        breed_count = len(breeds)
        breeds = ", ".join(breeds)
        pages = pagify(breeds, delims=[" "], page_length=2048)
        pages = [x for x in pages]
        return pages, breed_count


class Dog:
    def __init__(self, ctx):
        self.session = ctx.session
        self.base = "https://api.thedogapi.com/v1/"

    async def image(self, breed: str = None):
        url = self.base + "images/search?has_breeds=1"
        if breed:
            breeds = {}
            async with self.session.get(
                    url=self.base + "breeds",
                    headers={"x-api-key": os.getenv("DOG")}
            ) as resp:
                if resp.status != 200:
                    return raise_for_status(resp)
                breed_list = await resp.json()
            for x in breed_list:
                breeds[x["name"].lower()] = x["id"]
            if breed.lower() not in breeds:
                return None, None, None
            url += f"&breed_id={breeds[breed.lower()]}"
        async with self.session.get(
                url=url,
                headers={"x-api-key": os.getenv("DOG")}
        ) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            resp = (await resp.json())[0]
            details = ""
            for x, y in resp["breeds"][0].items():
                if x not in ["id", "name"]:
                    x = x.capitalize().replace('_', ' ')
                    if x == "Height":
                        height = f"**{x}:** {y['imperial']}in ({y['metric']}cm)\n"
                        continue
                    if x == "Weight":
                        weight = f"**{x}:** {y['imperial']}lb ({y['metric']}kg)\n"
                        continue
                    details += f"**{x}:** {y}\n"
            details += height + weight
            return resp["url"], resp["breeds"][0]["name"], details

    async def breeds(self):
        async with self.session.get(
                url=self.base + "breeds",
                headers={"x-api-key": os.getenv("DOG")}
        ) as resp:
            if resp.status != 200:
                return raise_for_status(resp)
            breed_list = await resp.json()
        breeds = [x["name"] for x in breed_list]
        breed_count = len(breeds)
        breeds = ", ".join(breeds)
        pages = pagify(breeds, delims=[" "], page_length=2048)
        pages = [x for x in pages]
        return pages, breed_count
