import asyncio
import discord
import traceback
import urllib.request
from datetime import datetime
from datetime import timedelta

from discord.ext import commands

from utils.checks import checks
from utils.database.BanSettings import Banlist


class Banlists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    async def banned(self, user):
        lookup = await Banlist.lookup(self, user)
        if lookup['banned'] is True:
            desc = f'**ID:** {user.id}\n**Date:** {lookup["date"]}\n**Reason:** {lookup["reason"]}\n**Proof:** {lookup["proof"]}'
            title = f'{user} was found on Global Banlist!'
            color = discord.Color.red()
        else:
            title = f'{user} was not found on Global Banlist!'
            desc = ' '
            color = discord.Color.green()
        embed = discord.Embed(title=title, description=desc, color=color)
        embed.set_thumbnail(url=user.avatar_url)
        return embed

    @commands.command(name= "Bancheck", description="Checks if the user is globally banned. n!bancheck")
    async def bancheck(self, ctx, member):
        user = None
        embed = ""
        if member is None:
            user = ctx.author
        if member is discord.Member:
            user = member
        if member is int():
            try:
                user = await self.bot.get_user_info(member)
            except discord.errors.NotFound:
                await ctx.send('No user with the id `{}` found.'.format(id))
        await self.banned(user)
        embedperm = ctx.guild.me.permissions_in(ctx.channel).embed_links
        if embedperm:
            await ctx.send(embed=embed)
        else:
            await ctx.send('It seems that I do not have embed permissions in this channel. Please correct and try again!')

    @commands.group(case_insensitive=True, description="Banlist Commands")
    async def banlist(self, ctx):
        """Checks for global bans on Discord.Services"""
        if not ctx.invoked_subcommand:
            return await ctx.send_help(ctx.command)

    @banlist.command(name="checkall", description="Checks all members in the server to see if they appear on the ban list! `n!banlist checkall`")
    async def checkall(self, ctx):
        guild = ctx.guild
        ctx.channel.send("This may take a bit depending on the number of users in the server!")
        list2 = []
        em = discord.Embed(title=f'Full Server Bancheck results!')
        for r in guild.members:
            data = await Banlist.lookup(self, r)
            if data['banned']:
                list2.append(f"``{str(r)}`` -- ``{str(r.id)}`` \n")
                em.add_field(name=r, value=r.id, inline=False)
        em.description(f'I have checked all users in the server and there are {len(list2)} users currently listed!')
        embedperm = ctx.guild.me.permissions_in(ctx.channel).embed_links
        if embedperm is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(f'I have checked all members in the server and found {len(list2)} members listed. However I cannot '
                           f'display the results due to not having embed permissions in this channel!')

    @commands.command(name= "mban", description='Bans all users that are listed on the global banlist!')
    @commands.cooldown(1, 5000, type=commands.BucketType.guild)
    @checks.admin_or_permissions(ban_members=True)
    async def mban(self, ctx):
        guild = ctx.guild
        channel = ctx.channel
        me = guild.me
        if not channel.permissions_for(me).ban_members:
            await ctx.send("❌ I don't have **ban_members** permissions.\nHow am i supposed to ban Hmmm?")
            return
        await ctx.send('Please wait this will take a while 🕙')
        count = 0
        for r in guild.members:
            data = await Banlist.lookup(self, r)
            if data['banned']:
                uids = data['id']
                try:
                    await self.bot.http.ban(uids, guild, 7, f"MASS BAN, User was listed on Discord.Services global ban list! Command ran by {ctx.author}")
                    count += 1
                    await asyncio.sleep(2)
                except:
                    traceback.print_exc()
        await ctx.send(f'You have banned 🔨 {count} bad users👌')


    @mban.error
    async def mban_error(self, error, ctx):
        if type(error) is commands.CommandOnCooldown:
            fmt = str(error).split()
            word = fmt[7].strip('s')
            time = float(word)
            timer = round(time, 0)
            tdelta = str(timedelta(seconds=int(timer))).lstrip('0').lstrip(':')
            await ctx.send(f'You can ban again in `{tdelta}`')

    @commands.command(description='Clears and Resets your Server banlist!')
    @checks.admin_or_permissions(ban_members=True)
    async def munban(self, ctx):
        guild = ctx.guild
        channel = ctx.channel
        me = guild.me
        if not channel.permissions_for(me).ban_members:
            await ctx.send("❌ I don't have **ban_members** permissions.\nHow am i supposed to ban Hmmm?")
            return
        counter = 0
        await ctx.send('just a sec')
        for ban in (await guild.bans()):
            try:
                await guild.unban(ban.user)
                counter += 1
                await asyncio.sleep(1.5)
            except:
                pass
                traceback.print_exc()
        await ctx.send(f'You have unbanned 🔨 {counter} users👌')

#TODO Change to pull image from upload and post to cdn for Naila, allow multiple uploads, 60 secs accept done with finished.

    async def post_image(self, image_url):
        if "/a/" in image_url:
            return image_url
        try:
            req = urllib.request.Request(
                image_url,
                data=None,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            resp = await self.session.post('https://cdn.discord.services/', headers={'key': 'T6iMJ0GAuLdJmzFkb'},
                                           data={'uploaded_file': urllib.request.urlopen(req)})
            return await resp.text()
        except urllib.request.HTTPError:
            return image_url

    @commands.command()
    @checks.is_owner()
    async def aban(self, ctx, member, proof: str, *, reason: str):
        reporter = ctx.author
        user = None
        if member is discord.Member:
            user = member
        if member is int():
            try:
                user = await self.bot.get_user_info(member)
            except discord.errors.NotFound:
                ctx.send(f'No user with ID of {member} was found. Please try again')
                return
        proof = await self.post_image(proof)
        date = datetime.now().strftime(self.bot.config()['time_format'])
        await Banlist.approve(self, user, reason, proof, reporter)
        await Banlist.logch.send(f"`{user.id}` | `{user.name}` has been banned by developer **{ctx.author.name}**")
        await ctx.message.delete()

# TODO add appeal command,
    @commands.cooldown(1, 90, type=commands.BucketType.user)
    @commands.command(aliases=["submit"], name="sban", description="Submits report for review by Banlist Admins")
    async def sban(self, ctx):
        author = ctx.message.author
        data = await Banlist.lookup(self, ctx.message.author)
        if data['banned'] is True:
            await ctx.message.add_reaction('❌')
            return await ctx.send('Oops! Looks like you are already listed on the banlist! Sorry but this means you '
                                  'cannot report others.')
        else:
            await ctx.message.add_reaction('✅')
        desc = 'Please send the users ID that you are reporting.'
        em = discord.Embed(color=discord.Color.blue(), description=desc)
        em.set_author(name='Submit a report')
        userid = ""
        reportinfo = {}
        try:
            await author.send(embed=em)
        except discord.Forbidden:
            return await ctx.send('😱 Ooops, Looks like you either have your Dms disabled or have me blocked. 😭')
        while True:

            def mcheck(m):
                return m.author == author and m.channel == author.dm_channel

            try:
                uid = await ctx.bot.wait_for('message', timeout=60, check=mcheck)
            except asyncio.TimeoutError:
                return await author.send('Oops, I think I have lost you. The command has timed out, please try again!')
            else:
                try:
                    user = await self.bot.get_user_info(uid.content)
                    userid += uid.content
                    break
                except discord.errors.NotFound or ValueError:
                    await author.send(f"No user with the ID {userid} was found.")
                except discord.HTTPException:
                    await author.send('Response must be a users ID!')
        useri = await self.bot.get_user_info(int(userid))
        desc = f'You are submitting a report for the following user {useri}\n\n' \
               f'Please select one of the following report reasons that match the proof you are going to submit.\n' \
               f':one: Raiding or Threat of Raid: (Please note nuking is not against ToS and therefor is not accepted\n' \
               f':two: **MASS** DM advertising (Meaning multiple DMs with invite links from the same person\n' \
               f':three: Harassment, Including self-harm encouragement\n' \
               f':four: Ban, Mute, or Block Evading (Creating an alternate account with the sole purpose of bypassing discord safeguards\n' \
               f':five: Underage User (Meaning either user has admitted to being under the age of 13, or under 18 and ' \
               f'lied about their age in order to gain access to NSFW content\n' \
               f':six: Inappropriate content (Meaning something that is forbidden by the ToS or Community Guidelines)\n' \
               f':seven: Sealing ones personal information (This includes doxing and phishing, Ip loggers, ect)'
        em = discord.Embed(color=discord.Color.blue(), description=desc)
        em.set_author(name='Submit a report')
        reason = await author.send(embed=em)
        await reason.add_reaction('1⃣')
        await reason.add_reaction('2⃣')
        await reason.add_reaction('3⃣')
        await reason.add_reaction('4⃣')
        await reason.add_reaction('5⃣')
        await reason.add_reaction('6⃣')
        await reason.add_reaction('7⃣')
        while True:

            def rcheck(reaction, user):
                return user == author and str(reaction.emoji) in ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣']

            try:
                reason = await ctx.bot.wait_for('reaction_add', timeout=60, check=rcheck)
            except asyncio.TimeoutError:
                return await author.send('Oops, I think I have lost you. The command has timed out, please try again!')
            if reason[0].emoji == '1⃣':
                reportinfo['reason'] = 'Raid or Threat of raid'
                break
            elif reason[0].emoji == '2⃣':
                reportinfo['reason'] = 'DM Advertising Spam'
                break
            elif reason[0].emoji == '3⃣':
                reportinfo['reason'] = 'Harassment'
                break
            elif reason[0].emoji == '4⃣':
                reportinfo['reason'] = 'Ban, Mute, Block Evading'
                break
            elif reason[0].emoji == '5⃣':
                reportinfo['reason'] = 'Underage user'
                break
            elif reason[0].emoji == '6⃣':
                reportinfo['reason'] = 'Inappropriate content'
                break
            elif reason[0].emoji == '7⃣':
                reportinfo['reason'] = 'Stealing personal information'
                break
        desc = f'You are submitting a report with the following details\n' \
               f'Reported User: {useri}\n' \
               f'Reason for report: {reason}\n' \
               f'Please upload any supporting proof you have for this report.'
        em = discord.Embed(color=discord.Color.blue(), description=desc)
        reason2 = reportinfo['reason']
        em.set_author(name='Submit a report')
        #todo change proof to use direct uploads from discord and not imgur
        await author.send(embed=em)
        while True:
            def pcheck(p):
                return p.author == author and p.channel == author.dm_channel
            try:
                proof = await ctx.bot.wait_for('message', timeout=120, check=pcheck)
            except asyncio.TimeoutError:
                return await author.send('Oops, I think I have lost you. The command has timed out, please try again!')
            if 'imgur.com' not in proof.content.lower():
                await author.send('Can you read? I need an IMGUR link to continue.')
            else:
                reportinfo['proof'] = str(proof.content)
                break
        desc = f"You are submitting a report for: {useri}\nWith reason: {reason2}\nWith Proof: {proof}\n" \
               f"Is this information correct?"
        em = discord.Embed(color=discord.Color.blue(), description=desc)
        verifem = await author.send(embed=em)
        await verifem.add_reaction('✅')
        await verifem.add_reaction('❌')
        while True:
            def okcheck(reaction, user):
                return user == author and str(reaction.emoji) in ['✅', '❌']
            try:
                verif = await ctx.bot.wait_for('reaction_add', timeout=60, check=okcheck)
            except asyncio.TimeoutError:
                return await author.send('Oops, I think I have lost you. The command has timed out, please try again!')
# todo Change to post to new Temp channel in Reports category for voting/judging. and after judging post to Judgements
            if verif[0].emoji == '✅':
                channel = self.bot.get_channel(Banlist.reportchan)
                desc = '🔨 **__Ban Report__** 🔨 \n'
                desc += f'**__Reason__**: {reason2} \n'
                desc += f'**__Proof__**: {proof} \n'
                em = discord.Embed(description=desc, color=discord.Color.blue())
                em.set_author(name='Ban Report',
                              icon_url='http://media2.intoday.in/indiatoday/images/stories/thumb-image_031015040724.jpg')
                em.add_field(name='**Info:**', value=f'**Name:** {user}\n**ID:** {user.id}')
                if useri.avatar_url:
                    em.set_thumbnail(url=useri.avatar_url)
                else:
                    em.set_thumbnail(url=useri.default_avatar_url)
                em.set_footer(text=('Reported by: ' + str(author.name)), icon_url=author.avatar_url)
                message = await channel.send(embed=em)
                await message.add_reaction(':VoteYay:308281470659592192')
                await message.add_reaction(':VoteNay:308281382675677194')
                messageid = message.id
                reporter = author.id
                await Banlist.report(self, messageid, useri, reason, proof, reporter)
                msg2 = await author.send('🔨 Ban reported! 🔨\nThanks for helping make discord a better place ❤')
                await msg2.add_reaction('❤')
                ch = self.bot.get_channel(Banlist.logch)
                await Banlist.logch.send(f"`{str(useri.name)}` | {useri.id} has been reported by **{author}**")
                break
            elif verif[0].emoji == '❌':
                return await author.send('Okay, you can submit again when you\'re ready!')

    @sban.error
    async def daily_error(self, ctx, error):
        if type(error) is commands.CommandOnCooldown:
            fmt = (str(error)).split()
            word = fmt[7].strip("s")
            time = float(word)
            timer = round(time, 0)
            tdelta = str(timedelta(seconds=int(timer))).lstrip("0").lstrip(":")
            em = discord.Embed(color=0xFF0000)
            em.set_author(name='You can report another user in {}'.format(tdelta))
            await ctx.send(embed=em)

# TODO, Change to look for reactions in Reports Category instead of just one channel.
    async def on_raw_reaction_add(self, emoji, message_id, channel_id, user_id):
        if channel_id == Banlist.reportchan:
            yay = self.bot.get_emoji(308281470659592192)
            nay = self.bot.get_emoji(308281382675677194)
            if emoji.id == yay.id:
                user = await self.bot.get_user_info(user_id)
                guild = self.bot.get_guild(Banlist.ds_server)
                if Banlist.banlist_judge in [ro.id for ro in [x for x in guild.members if x.id == user.id][0].roles]:
                    c = self.bot.get_channel(channel_id)
                    jch = self.bot.get_channel(Banlist.judgement)
                    msg = await c.get_message(message_id)
                    for x in msg.embeds:
                        rinfo = await Banlist.callreport(self, messageid=message_id)
                        user2 = self.bot.get_user(self, id=rinfo['id'])
                        reason = rinfo['reason']
                        proof = rinfo['proof']
                        reporter = rinfo['reporter']
                        desc = str(x.description).replace('Report', 'Approved')
                        em = discord.Embed(description=desc, color=discord.Color.green())
                        em.add_field(name=x._fields[0]['name'], value=x._fields[0]['value'])
                        em.set_thumbnail(url=x._thumbnail['url'])
                        em.set_footer(text=f'Ban approved by {user}', icon_url=user.avatar_url)
                        em.set_author(name='Ban approved', icon_url='http://media2.intoday.in/indiatoday/'
                                                                    'images/stories/thumb-image_031015040724.jpg')
                        user1 = await self.bot.get_user_info(rinfo['id'])
                        await Banlist.logch.send(f"`{str(user1)}` | {user1.mention}'s report has been APPROVED by **{user}**")
                        await Banlist.approve(self, user2, reason, proof, reporter)
                        await jch.send(embed=em)
                        await Banlist.reject(self, messageid=message_id)
                        await msg.delete()
            elif emoji.id == nay.id:
                user = await self.bot.get_user_info(user_id)
                guild = self.bot.get_guild(Banlist.ds_server)
                rdesc = ''
                if Banlist.banlist_judge in [ro.id for ro in [x for x in guild.members if x.id == user.id][0].roles]:
                    c = self.bot.get_channel(channel_id)
                    msg = await c.get_message(message_id)
                    reasonmsg = await c.send('1⃣ Proof is not Sufficient\n2⃣ Reason does not match proof provided.')
                    while True:
                        responses = ['1', '2']
                        def ncheck(n):
                            return n.channel == reasonmsg.channel and n.author == user
                        try:
                            reason = await self.bot.wait_for('message', timeout=300.0, check=ncheck)
                        except asyncio.TimeoutError:
                            await reasonmsg.delete()
                            break
                        if reason.content not in responses:
                            err = await c.send("You have entered an incorrect response. Please try again!")
                            await asyncio.sleep(5)
                            await err.delete()
                            await reason.delete()
                            await reasonmsg.delete()
                            await msg.remove_reaction(nay, user)
                        elif reason.content in responses:
                            if reason.content == '1':
                                rdesc += f'\n\n**__Denial Reason__**: Proof is not Sufficient'
                                await reasonmsg.delete()
                                await reason.delete()
                                jch = self.bot.get_channel(Banlist.judgement)
                                for x in msg.embeds:
                                    desc = str(x.description).replace('Report', 'Denied').replace('🔨', '🆓')
                                    desc += rdesc
                                    em = discord.Embed(description=desc, color=discord.Color.red())
                                    em.add_field(name=x._fields[0]['name'], value=x._fields[0]['value'])
                                    em.set_thumbnail(url=x._thumbnail['url'])
                                    em.set_footer(text=f'Ban denied by {user}', icon_url=user.avatar_url)
                                    em.set_author(name='Ban Denied',
                                                  icon_url='https://i.ytimg.com/vi/0qm-cOe0kwk/hqdefault.jpg')
                                    info = await Banlist.callreport(self, messageid=message_id)
                                    user1 = await self.bot.get_user_info(int(info['id']))
                                    ch = self.bot.get_channel(Banlist.logch)
                                    await ch.send(f"`{str(user1)}` | {user1.mention}'s report has been DENIED by **{user}**")
                                    await jch.send(embed=em)
                                    await Banlist.reject(self, messageid=message_id)
                                    await msg.delete()
                            if reason.content == '2':
                                rdesc += f'\n\n**__Denial Reason__**: Reason does not match proof provided'
                                await reasonmsg.delete()
                                await reason.delete()
                                jch = self.bot.get_channel(Banlist.judgement)
                                msg = await c.get_message(message_id)
                                for x in msg.embeds:
                                    desc = str(x.description).replace('Report', 'Denied').replace('🔨', '🆓')
                                    desc += rdesc
                                    em = discord.Embed(description=desc, color=discord.Color.red())
                                    em.add_field(name=x._fields[0]['name'], value=x._fields[0]['value'])
                                    em.set_thumbnail(url=x._thumbnail['url'])
                                    em.set_footer(text=f'Ban denied by {user}', icon_url=user.avatar_url)
                                    em.set_author(name='Ban Denied',
                                                  icon_url='https://i.ytimg.com/vi/0qm-cOe0kwk/hqdefault.jpg')
                                    info = await Banlist.callreport(self, messageid=message_id)
                                    user1 = await self.bot.get_user_info(int(info['id']))
                                    ch = self.bot.get_channel(Banlist.logch)
                                    await ch.send(f"`{str(user1)}` | {user1.mention}'s report has been DENIED by **{user}**")
                                    await jch.send(embed=em)
                                    await Banlist.reject(self, messageid=message_id)
                                    await msg.delete()
                        break
                        
# TODO, Make sure Check allows only Sapphire and Kanin to run this command
    @checks.is_owner()
    @commands.command()
    async def revoke(self, ctx, id: int, *, reason):
        try:
            user = await self.bot.get_user_info(id)
            ch = self.bot.get_channel(Banlist.logch)
            await Banlist.revoke(self, user=user.id)
            await ch.send(f"`{str(user)}` | {user.mention}'s global ban was revoked by developer **{ctx.author}** "
                          f"with reason: {reason}")
            await ctx.send("That user has been removed from the banlist!")
        except discord.errors.NotFound:
            ctx.send("Sorry that does not appear to be a valid UserID")



def setup(bot):
    n = Banlists(bot)
    bot.add_cog(n)
