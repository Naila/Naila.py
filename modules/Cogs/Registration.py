import asyncio
from datetime import datetime

import discord
from discord.ext import commands
from rethinkdb import r

from utils.checks import checks
from utils.checks.bot_checks import can_manage_user
from utils.functions import pagify

# TODO: Make registration great again

roles = [
    "He/Him", "She/Her", "They/Them", "Mention", "No Mention", "18+", "<18",
    "Registered", "DMs NOT Allowed", "DMs Allowed", "Ask to DM"
]


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(case_insensitive=True, description="Registration management")
    async def setreg(self, ctx):
        """{"permissions": {"user": ["manage_guild"], "bot": ["embed_links"]}}"""
        if not ctx.invoked_subcommand:
            return await ctx.group_help()

    @setreg.command(description="Set the output channel")
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """{"permissions": {"user": ["manage_guild"], "bot": ["embed_links"]}}"""
        if not channel:
            channel = ctx.channel
        db = await r.table("Registration").get(str(ctx.guild.id)).run(self.bot.conn)
        db["channel"] = str(channel.id)
        await r.table("Registration").insert(db, conflict="update").run(self.bot.conn)
        await ctx.send(f"Set the channel {channel.mention} as the output for registration.")

    @setreg.command(description="Toggle registration")
    async def toggle(self, ctx):
        """{"permissions": {"user": ["manage_guild"], "bot": ["embed_links"]}}"""
        db = await r.table("Registration").get(str(ctx.guild.id)).run(self.bot.conn)
        db["enabled"] = not db["enabled"]
        await r.table("Registration").insert(db, conflict="update").run(self.bot.conn)
        if db["enabled"]:
            await ctx.send("Registration enabled.")
        else:
            await ctx.send("Registration disabled.")

    @setreg.command(description="Create the roles required for registration")
    async def roles(self, ctx):
        """{"permissions": {"user": ["manage_guild"], "bot": ["embed_links", "manage_roles"]}}"""
        guild = ctx.guild

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            await ctx.send("This will create the roles needed for this cog to function.\n```md\n"
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
                setrole = await ctx.bot.wait_for("message", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Timed out")
            if setrole.content.lower() == "no":
                await ctx.send("Okay, this must be done before the command will work correctly!")
            elif setrole.content.lower() == "yes":
                created = 0
                await ctx.send("Okay, this will just take a moment")
                for role in roles:
                    check = discord.utils.get(guild.roles, name=role)
                    if check not in guild.roles:
                        await guild.create_role(name=role)
                        created += 1
                await ctx.send(f"All done! Created {created} roles.")
            else:
                await ctx.send("You have entered an invalid response. Valid responses include `yes` and `no`.")
        except (discord.HTTPException, discord.Forbidden):
            await ctx.send("Creation of roles has failed, The most common problem is that I do not have Manage Roles "
                           "Permissions on the server. Please check this and try again.")

    @setreg.command(name="autoban",
                    description="Set the age in which the bot will ban the user if they are less than (Default: 13)")
    async def setreg_autoban(self, ctx, age: int):
        """{"permissions": {"user": ["manage_guild"], "bot": ["embed_links", "ban_members"]}}"""
        guild = ctx.guild
        db = await r.table("Registration").get(str(guild.id)).run(self.bot.conn)
        if age < 13:
            age = 13
            await ctx.send("You tried to set the age lower than the minimum (13) so I have set it to 13!")
        db["autoban_age"] = age
        await r.table("Registration").insert(db, conflict="update").run(self.bot.conn)
        await ctx.send(f"I will now try to ban users who say they are less than {age}!")

    @commands.guild_only()
    @commands.command(description="Unregister, allowing you to register again!")
    async def unregister(self, ctx):
        """{"permissions": {"user": [], "bot": ["embed_links", "manage_roles"]}}"""
        guild = ctx.guild
        author = ctx.author
        if not can_manage_user(ctx, author):
            return await ctx.send("I don't have a role above you which means I can't manage your roles,"
                                  " please have someone with permissions move my role up!")
        remove = []
        for role in roles:
            check = discord.utils.get(guild.roles, name=role)
            if check in author.roles:
                remove.append(check)
        await author.remove_roles(*remove, reason="User ran unregister command")
        await ctx.send("Done, you may now register again!")

    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.command(description="Register in this guild!")
    async def register(self, ctx):
        """{"permissions": {"user": [], "bot": ["embed_links", "manage_roles"]}}"""
        guild = ctx.guild
        author = ctx.author
        db = await r.table("Registration").get(str(ctx.guild.id)).run(self.bot.conn)
        if not db["enabled"]:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("Registration isn't currently enabled here!")
        if not db["channel"]:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("No channel is set for the introduction to be sent to!")
        channel = self.bot.get_channel(int(db["channel"]))
        if not channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("I can't find the output channel!")
        if not can_manage_user(ctx, author):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("I don't have a role above you which means I can't manage your roles,"
                                  " please have someone with permissions move my role up!")
        no_role = 0
        for role in roles:
            check = discord.utils.get(guild.roles, name=role)
            if check not in guild.roles:
                no_role += 1
        if no_role > 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"It looks like you haven't set up the roles here, you must have all roles in the"
                                  f" server to use this function:\n{await ctx.bot.get_prefix(ctx.message)}setreg roles")
        registered_role = discord.utils.get(guild.roles, name="Registered")
        if registered_role in author.roles:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"It looks like you've already registered on this server!"
                                  f" Please run `{await ctx.bot.get_prefix(ctx.message)}unregister`"
                                  f" if you wish to re-register.")
        em = discord.Embed(description=f"**{author.mention}**,\nI will DM you to collect your info!",
                           color=await ctx.guildcolor(str(guild.id)))
        await ctx.send(embed=em)
        try:
            await author.send("What is your preferred pronoun? Please choose from:\n`He/Him`, `She/Her`, `They/Them`.")
        except discord.Forbidden:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("It looks like you have your DMs disabled! Please enable them so I can register you.")

        def check(m):
            return m.channel == author.dm_channel and m.author == author

        em = discord.Embed(color=await ctx.guildcolor(str(guild.id)))
        avatar = author.avatar_url if author.avatar else author.default_avatar_url
        em.set_author(name=f"Introduction for {author}:", icon_url=avatar)
        em.set_footer(text=f"ID: {author.id} | {datetime.now().strftime(self.bot.config()['time_format'])}")
        roles_to_add = []
        while True:
            options = ["he/him", "she/her", "they/them"]
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                try:
                    ctx.command.reset_cooldown(ctx)
                    return await author.send("Registration has timed out.")
                except discord.Forbidden:
                    return ctx.command.reset_cooldown(ctx)
            if response.content.lower() not in options:
                try:
                    await author.send("Invalid response.")
                except discord.Forbidden:
                    return
            else:
                if response.content.lower() == "he/him":
                    role = discord.utils.get(guild.roles, name="He/Him")
                    roles_to_add.append(role)
                    em.add_field(name="Pronoun:", value="He/Him")
                elif response.content.lower() == "she/her":
                    role = discord.utils.get(guild.roles, name="She/Her")
                    roles_to_add.append(role)
                    em.add_field(name="Pronoun:", value="She/Her")
                elif response.content.lower() == "they/them":
                    role = discord.utils.get(guild.roles, name="They/Them")
                    roles_to_add.append(role)
                    em.add_field(name="Pronoun:", value="They/Them")
                break
            if not response:
                break
        while True:
            options = ["yes", "no", "ask"]
            try:
                await author.send("Are you okay with being Directly Messaged? Please chose from:\n"
                                  "`Yes`, `No`, or `Ask`.")
            except discord.Forbidden:
                return ctx.command.reset_cooldown(ctx)
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                try:
                    ctx.command.reset_cooldown(ctx)
                    return await author.send("Registration has timed out.")
                except discord.Forbidden:
                    return
            if response.content.lower() not in options:
                try:
                    await author.send("Invalid response.")
                except discord.Forbidden:
                    return ctx.command.reset_cooldown(ctx)
            else:
                if response.content.lower() == "yes":
                    role = discord.utils.get(guild.roles, name="DMs Allowed")
                    roles_to_add.append(role)
                    em.add_field(name="DMs open:", value="Yes")
                elif response.content.lower() == "no":
                    role = discord.utils.get(guild.roles, name="DMs NOT Allowed")
                    roles_to_add.append(role)
                    em.add_field(name="DMs open:", value="No")
                elif response.content.lower() == "ask":
                    role = discord.utils.get(guild.roles, name="Ask to DM")
                    roles_to_add.append(role)
                    em.add_field(name="DMs open:", value="Ask first")
                break
            if not response:
                break
        while True:
            options = ["yes", "no"]
            try:
                await author.send("Are you okay with being mentioned? Please chose from:\n`Yes` or `No`.")
            except discord.Forbidden:
                return ctx.command.reset_cooldown(ctx)
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                try:
                    ctx.command.reset_cooldown(ctx)
                    return await author.send("Registration has timed out.")
                except discord.Forbidden:
                    return ctx.command.reset_cooldown(ctx)
            if response.content.lower() not in options:
                try:
                    await author.send("Invalid response.")
                except discord.Forbidden:
                    return ctx.command.reset_cooldown(ctx)
            else:
                if response.content.lower() == "yes":
                    role = discord.utils.get(guild.roles, name="Mention")
                    roles_to_add.append(role)
                    em.add_field(name="Mentions:", value="Yes")
                elif response.content.lower() == "no":
                    role = discord.utils.get(guild.roles, name="No Mention")
                    roles_to_add.append(role)
                    em.add_field(name="Mentions:", value="No")
                break
            if not response:
                break
        while True:
            try:
                await author.send("What is your age? Please be truthful! Lying will get your account BANNED!")
            except discord.Forbidden:
                return ctx.command.reset_cooldown(ctx)
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                try:
                    ctx.command.reset_cooldown(ctx)
                    return await author.send("Registration has timed out.")
                except discord.Forbidden:
                    return ctx.command.reset_cooldown(ctx)
            autoban_age = await r.table("Registration").get(str(guild.id)).get_field("autoban_age").run(self.bot.conn)
            if response.content.isdigit():
                if int(response.content) < autoban_age:
                    try:
                        return await guild.ban(author, reason="Underage (Registration autoban)")
                    except (discord.Forbidden, discord.HTTPException):
                        return await ctx.send(f"{author}"'s age is less than the required autoban age!'
                                              ' I do not have permissions to ban them!')
                if int(response.content) > 100:
                    try:
                        await author.send("Please enter a real age.")
                    except discord.Forbidden:
                        return ctx.command.reset_cooldown(ctx)
                else:
                    if int(response.content) >= 18:
                        role = discord.utils.get(guild.roles, name="18+")
                        roles_to_add.append(role)
                        em.add_field(name="Age:", value=response.content)
                    elif int(response.content) <= 17:
                        role = discord.utils.get(guild.roles, name="<18")
                        roles_to_add.append(role)
                        em.add_field(name="Age:", value=response.content)
                    break
            else:
                try:
                    await author.send("Age must be a number!")
                except discord.Forbidden:
                    return ctx.command.reset_cooldown(ctx)
            if not response:
                break
        try:
            await author.send("Introduce yourself!")
        except discord.Forbidden:
            return ctx.command.reset_cooldown(ctx)
        try:
            response = await ctx.bot.wait_for("message", timeout=300, check=check)
        except asyncio.TimeoutError:
            em.add_field(name="Info:", value="A mysterious person...")
        else:
            pagenum = 0
            pages = pagify(response.content, None, 0, 1000)
            for page in pages:
                pagenum += 1
                em.add_field(name=f"About{' (continued):' if pagenum > 1 else ':'}", value=page, inline=False)
        roles_to_add.append(registered_role)
        try:
            await author.add_roles(*roles_to_add, reason="Registration")
        except discord.NotFound:
            return await ctx.send("I could not find the member registering! Perhaps they left?")
        try:
            await author.send("Thank you, Registration is now complete!")
        except discord.Forbidden:
            pass
        await channel.send(embed=em)
        em = discord.Embed(color=await ctx.guildcolor(str(guild.id)),
                           description=f"Thank you for registering, {author.mention}!")
        return await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Registration(bot))
