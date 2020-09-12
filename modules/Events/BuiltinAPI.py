import os

import aiohttp_jinja2
import jinja2
from aiohttp import web
from discord.ext import commands

BLACKLISTED_EVENTS = ["presence_update"]


class BuiltinAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.runner = None
        self.app = web.Application()
        aiohttp_jinja2.setup(self.app, loader=jinja2.FileSystemLoader("utils/assets/templates"))
        self.routes = web.RouteTableDef()
        self.routes.static("/assets", "utils/assets/", show_index=True, name="Test")
        self.host = os.getenv("API_HOST", "localhost")
        self.port = os.getenv("API_PORT", 8080)
        self.bot.loop.create_task(self.server())
        self.events = {}

    def cog_unload(self):
        self.bot.log.info("Stopping api server")
        self.bot.loop.create_task(self.runner.cleanup())

    async def server(self):

        @self.routes.get("/")
        @aiohttp_jinja2.template("home.jinja2")
        async def home(request):
            return {}

        @self.routes.get("/commands")
        async def com_list(request):
            response_object = {}
            for command in self.bot.walk_commands():
                if command.hidden:
                    continue
                if command.enabled:
                    if command.cog_name not in response_object:
                        response_object[command.cog_name] = {}
                    cmd = str(command).replace(" ", "_")
                    response_object[command.cog_name].update({cmd: {}})
                    response_object[command.cog_name][cmd]["description"] = command.help
                    if "bot_perms" in dir(command.callback):
                        response_object[command.cog_name][cmd]["bot_perms"] = \
                            [x for x, y in command.callback.bot_perms.items()]
                    if "user_perms" in dir(command.callback):
                        response_object[command.cog_name][cmd]["user_perms"] = \
                            [x for x, y in command.callback.user_perms.items()]
            return web.json_response(data=response_object)

        # TODO: Make this a micro service
        @self.routes.get("/metrics/boobbot")
        async def boobbot_metrics(request):
            lines = []

            async with self.bot.session.get("https://stats.boob.bot/stats") as stats_resp:
                if stats_resp.status == 200:
                    stats_json = await stats_resp.json()

                    lines.append(f"audio_players,bot=bb count={int(stats_json['stats']['bb']['Audio_Players'])}i")
                    lines.append(f"guild_count,bot=bb count={int(stats_json['stats']['bb']['Guilds'])}i")
                    lines.append(f"user_count,bot=bb count={int(stats_json['stats']['bb']['Users'])}i")
                    lines.append(f"average_latency,bot=bb latency={stats_json['stats']['bb']['Average_Latency']}")
            # async with self.bot.session.get("https://stats.boob.bot/metrics") as metrics_resp:
            #     if metrics_resp.status == 200:
            #         metrics_json = await metrics_resp.json()
            # async with self.bot.session.get("https://stats.boob.bot/pings") as pings_resp:
            #     if pings_resp.status == 200:
            #         pings_json = await pings_resp.json()

            return web.Response(text="\n".join(lines))

        @self.routes.get("/metrics")
        async def metrics(request):
            lines = []

            for event, count in self.events.items():
                lines.append(f"event_counts,bot=naila,type={event} count={count}i")

            for command, count in self.bot.commands_used.items():
                lines.append(f"commands_ran,bot=naila,command={command} count={count}i")

            lines.append(f"guild_count,bot=naila count={len(self.bot.guilds)}i")
            return web.Response(text="\n".join(lines))

        self.app.add_routes(self.routes)
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        server = web.TCPSite(self.runner, self.host, self.port)
        await server.start()
        self.bot.log.info(f"API Server running on {server.name}")

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        if msg.get("op") != 0:
            # Not a dispatch (might be useful to track heartbeats, reconnects, invalid sessions etc. tho)
            return

        event = msg.get("t", "none").lower()
        if event not in BLACKLISTED_EVENTS:
            if event not in self.events.keys():
                self.events[event] = 1
            else:
                self.events[event] += 1


def setup(bot):
    bot.add_cog(BuiltinAPI(bot))
