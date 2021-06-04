import asyncio
from datetime import datetime

from discord import Embed, Guild, TextChannel, utils, Forbidden, HTTPException, NotFound
from discord.ext.commands import Cog, command, group, guild_only, check, cooldown, max_concurrency, NoPrivateMessage, \
    CheckFailure, BucketType

from bot import Bot
from utils.checks import checks
from utils.checks.bot_checks import can_manage_user
from utils.ctx import Context

roles = [
    "He/Him", "She/Her", "They/Them", "Mention", "No Mention", "18+", "<18",
    "Registered", "DMs NOT Allowed", "DMs Allowed", "Ask to DM"
]

default = [
    {
        "question": "What is your preferred pronoun?",
        "short": "Pronoun:",
        "options": {
            "he/him": {"aliases": ["male", "he", "him"], "role": "He/Him"},
            "they/them": {"aliases": ["they", "them"], "role": "They/Them"},
            "she/her": {"aliases": ["female", "she", "her"], "role": "She/Her"}
        }
    },
    {
        "question": "Are you okay with being Directly Messaged?",
        "short": "DMs open:",
        "options": {
            "yes": {"aliases": [], "role": "DMs Allowed"},
            "no": {"aliases": [], "role": "DMs NOT Allowed"},
            "ask": {"aliases": [], "role": "Ask to DM"}
        }
    },
    {
        "question": "Are you okay with being mentioned?",
        "short": "Mentions:",
        "options": {
            "yes": {"aliases": [], "role": "Mention"},
            "no": {"aliases": [], "role": "No Mention"}
        }
    }
]


class DB:

    @staticmethod
    async def check(bot, guild: Guild):
        data = await bot.pool.fetch("SELECT * FROM registration WHERE guild_id=$1", guild.id)
        if not data:
            await bot.pool.execute("INSERT INTO registration (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild.id)
            bot.log.info(f"Added {guild.name} to the (registration) database")

    @staticmethod
    async def data(ctx: Context):
        await DB.check(ctx.bot, ctx.guild)
        data = await ctx.pool.fetchrow(
            "SELECT enabled, channel, age::json, questions::json, role FROM registration WHERE guild_id=$1",
            ctx.guild.id
        )
        return data

    @staticmethod
    async def toggle(ctx: Context):
        data = await DB.data(ctx)
        await ctx.pool.execute("UPDATE registration SET enabled = NOT enabled WHERE guild_id=$1", ctx.guild.id)
        return not data["enabled"]

    @staticmethod
    async def update_channel(ctx: Context, channel: TextChannel):
        data = await DB.data(ctx)
        if data["channel"] and data["channel"] == channel.id:
            return False
        await ctx.pool.execute("UPDATE registration SET channel=$1 WHERE guild_id=$2", channel.id, ctx.guild.id)
        return True

    @staticmethod
    async def update_banage(ctx: Context, age: int):
        await ctx.pool.execute(
            "UPDATE registration SET age=jsonb_set(age, '{ban_age}', $1::jsonb) WHERE guild_id=$2",
            str(age),
            ctx.guild.id
        )


def registration_check():
    async def predicate(ctx: Context):
        guild, author = ctx.guild, ctx.author
        if not guild:
            raise NoPrivateMessage
        data = await DB.data(ctx)
        if not data["enabled"]:
            ctx.command.reset_cooldown(ctx)
            await ctx.send_error("Registration is not enabled here!")
            return False

        if not data["channel"] or not guild.get_channel(data["channel"]):
            ctx.command.reset_cooldown(ctx)
            await ctx.send_error("Either you don't have a channel set up or I could not find it!")
            return False

        if not can_manage_user(ctx, author):
            ctx.command.reset_cooldown(ctx)
            await ctx.send_error("I don't have a role above you which means I can't manage your roles,"
                                 " please have someone with permissions move my role up!")
            return False
        roles_found = 0
        for role in roles:
            role = utils.get(guild.roles, name=role)
            if role in guild.roles:
                roles_found += 1
        if roles_found < len(roles):
            ctx.command.reset_cooldown(ctx)
            await ctx.send_error(f"It looks like you haven't set up the roles here, you must have all roles in"
                                 f" the server to use this function:\n"
                                 f"{await ctx.bot.get_prefix(ctx.message)}setreg roles")
            return False

        registered_role = utils.get(guild.roles, name="Registered")
        if registered_role in author.roles:
            ctx.command.reset_cooldown(ctx)
            await ctx.send_error(f"It looks like you've already registered on this server!\n"
                                 f"Please run `{await ctx.bot.get_prefix(ctx.message)}unregister`"
                                 f" if you wish to re-register.")
            return False
        return True

    return check(predicate)


class Registration(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @group(case_insensitive=True, description="Registration management")
    @guild_only()
    @checks.admin()
    async def setreg(self, ctx: Context):
        if not ctx.invoked_subcommand:
            return await ctx.send_help(ctx.command)

    @setreg.command(name="channel", description="Set the output channel")
    @checks.bot_has_permissions(embed_links=True)
    async def setreg_channel(self, ctx: Context, channel: TextChannel):
        update = await DB.update_channel(ctx, channel)
        if not update:
            return await ctx.send_error("That channel is already set!")
        await ctx.reply(f"Set the channel {channel.mention} as the output for registration.")

    @setreg.command(name="toggle", description="Toggle registration")
    @checks.bot_has_permissions(embed_links=True)
    async def setreg_toggle(self, ctx: Context):
        update = await DB.toggle(ctx)
        if update:
            return await ctx.reply("Registration enabled.")
        await ctx.reply("Registration disabled.")

    @setreg.command(name="roles", description="Create the roles required for registration")
    @checks.bot_has_permissions(embed_links=True, manage_roles=True)
    async def setreg_roles(self, ctx: Context):
        guild = ctx.guild

        def mcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            await ctx.reply("This will create the roles needed for this cog to function.\n```md\n"
                            "[Pronoun Roles](He/Him, She/Her, They/Them)\n"
                            "[DM Roles](DMs Allowed, DMs NOT Allowed, Ask to DM)\n"
                            "[Mention](Mention, No Mention)\n"
                            "[Misc Roles](18+, Registered, <18)\n"
                            "These roles are required for the cog to function correctly.\n"
                            "DO NOT CHANGE THE NAME OF THESE ROLES\n"
                            "They will be made with no permissions. You can modify this later through Role"
                            " Management if you "
                            "Need/Want to.\nDo you wish to continue? [This command will time out in 60s]```")
            try:
                setrole = await ctx.bot.wait_for("message", timeout=60.0, check=mcheck)
            except asyncio.TimeoutError:
                return await ctx.reply("Timed out")
            if setrole.content.lower() == "no":
                await ctx.reply("Okay, this must be done before the command will work correctly!")
            elif setrole.content.lower() == "yes":
                created = 0
                await ctx.reply("Okay, this will just take a moment")
                for role in roles:
                    role = utils.get(guild.roles, name=role)
                    if role not in guild.roles:
                        await guild.create_role(name=role)
                        created += 1
                await ctx.reply(f"All done! Created {created} roles.")
            else:
                await ctx.reply("You have entered an invalid response. Valid responses include `yes` and `no`.")
        except (HTTPException, Forbidden):
            await ctx.reply("Creation of roles has failed, The most common problem is that I do not have Manage Roles "
                            "Permissions on the server. Please check this and try again.")

    @setreg.command(name="banage",
                    description="Set the age in which the bot will ban the user if they are less than (Default: 13)")
    @checks.bot_has_permissions(embed_links=True, ban_members=True)
    async def setreg_banage(self, ctx: Context, age: int):
        if age < 13:
            age = 13
            await ctx.reply("You tried to set the age lower than the minimum (13) so I have set it to 13!")
        await DB.update_banage(ctx, age)
        await ctx.reply(f"I will now ban users who are less than {age}!")

    @command(description="Unregister, allowing you to register again!")
    @guild_only()
    @checks.bot_has_permissions(embed_links=True, manage_roles=True)
    async def unregister(self, ctx: Context):
        guild, author = ctx.guild, ctx.author
        if not can_manage_user(ctx, author):
            return await ctx.reply("I don't have a role above you which means I can't manage your roles,"
                                   " please have someone with permissions move my role up!")
        remove = []
        for role in roles:
            role = utils.get(guild.roles, name=role)
            if role in author.roles:
                remove.append(check)
        await author.remove_roles(*remove, reason="[ Registration ] User unregistered")
        await ctx.reply("Done, you may now register again!")

    # TODO: Rewrite
    @registration_check()
    @command(description="Register in this guild!")
    @cooldown(1, 300, BucketType.user)
    @max_concurrency(1, BucketType.user)
    @checks.bot_has_permissions(embed_links=True, manage_roles=True)
    async def register(self, ctx: Context):
        guild, author = ctx.guild, ctx.author

        # Data
        data = await DB.data(ctx)
        ch = guild.get_channel(data["channel"])

        # Setting default embeds and creating role list
        out = Embed(color=await ctx.guildcolor())
        out.set_author(name=f"Introduction for {author}:",
                       icon_url=author.avatar_url if author.avatar else author.default_avatar_url)
        out.set_footer(text=f"ID: {author.id} | {datetime.utcnow().strftime(self.bot.config.time_format)}")
        em = Embed(color=await ctx.guildcolor())
        roles_to_add = []
        x = 0
        questions = default if not data["questions"] else data["questions"]
        total_questions = len(questions) + 1
        try:
            # Should we check the user's age?
            if data["age"]["enabled"]:
                total_questions += 1
                x += 1

                # Update question embed and send it
                em.set_author(name=f"Question #{x}/{total_questions}:")
                em.description = "How old are you?"
                em.add_field(name="Options:", value="Whole number: keep in mind that lying about your age is bannable!")
                await author.send(embed=em)

                # Manage answer and role parsing/banning for underage users
                answer = int(await self.ask_question(ctx, "age"))
                if answer < data["age"]["ban_age"]:
                    await author.send("You are under this guilds auto ban age, therefore I have to ban you!")
                    return await guild.ban(author, reason="[ Registration ] Underage")
                    # return await ctx.reply(f"🇫 | {author} was too young to be in the server")

                role = data["age"]["roles"]["over"] if answer >= 18 else data["age"]["roles"]["under"]
                roles_to_add.append(self.get_role(ctx, role))
                out.add_field(name="Age:", value=str(answer))

            # Loop through questions
            for question in questions:
                x += 1

                # Update question embed and send it
                em.clear_fields()
                em.set_author(name=f"Question #{x}/{total_questions}:")
                em.description = question["question"]
                options = [x for x in question["options"]]
                em.add_field(
                    name="Options:",
                    value=f"{', '.join(options[:-1])}, or {options[-1]}" if len(options) > 2 else " or ".join(options)
                )
                await author.send(embed=em)

                # Manage answer and role parsing
                answer = await self.ask_question(ctx, question)
                out.add_field(name=question["short"], value=answer.capitalize())

                role = question["options"][answer]["role"]
                roles_to_add.append(self.get_role(ctx, role))

            # Allow the user to introduce themselves
            x += 1
            em.clear_fields()
            em.set_author(name=f"Question #{x}/{total_questions}:")
            em.description = "Introduce yourself!"
            em.add_field(name="Options:", value="Long intro or `no` if you would rather not")
            await author.send(embed=em)
            answer = await self.ask_question(ctx, "intro")
            if answer:
                out.description = answer

            # Registration complete, add roles and do all of that stuff
            roles_to_add.append(utils.get(guild.roles, name="Registered"))
            await author.add_roles(*roles_to_add, reason="[ Registration ] User has registered")

            await author.send("Thank you for registering!")
            await ch.send(embed=out)

        # Handle exceptions
        except Forbidden:
            return await ctx.send_error(f"{author.mention} I cannot DM you!")
        except asyncio.TimeoutError:
            ctx.command.reset_cooldown(ctx)
            try:
                return await author.send("Timed out!")
            except Forbidden:
                return
        except NotFound:
            return await ctx.send_error(f"I could not find {author}! Perhaps they left?")

    @staticmethod
    def get_role(ctx: Context, role):
        guild = ctx.guild
        if isinstance(role, int):
            return guild.get_role(role)
        return utils.get(guild.roles, name=role)

    @staticmethod
    async def ask_question(ctx: Context, question):
        guild, author = ctx.guild, ctx.author
        answer = ""

        def mcheck(m):
            return m.channel == author.dm_channel and m.author == author

        while True:
            answered = False
            response = await ctx.bot.wait_for("message", timeout=300 if question == "intro" else 60, check=mcheck)
            resp = response.content.lower()
            if question == "intro":
                if resp == "no":
                    return None
                answer = response.content
                answered = True
            elif question == "age":
                if response.content.isdigit():
                    answer = response.content
                    answered = True
            else:
                for option, data in question["options"].items():
                    if resp == option or resp in data["aliases"]:
                        answer = option
                        answered = True
                        break
            if answered:
                return answer
            await author.send("Invalid response!")

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CheckFailure):
            return


def setup(bot):
    bot.add_cog(Registration(bot))
