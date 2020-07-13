import discord
from discord.ext.commands import AutoShardedBot as DiscordBot
from datetime import datetime


async def check(bot: DiscordBot, guild: discord.Guild):
    con = await bot.pool.acquire()
    _data = await con.fetch("SELECT * FROM guildsettings_privatevc WHERE guild_id=$1", guild.id)
    if not _data:
        await con.execute("INSERT INTO guildsettings_privatevc (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild.id)
        bot.log.info(f"Added {guild.name} to the (guildsettings_privatevc) database")


async def settings(bot: DiscordBot, guild: discord.Guild):
    con = await bot.pool.acquire()
    await check(bot, guild)
    return await con.fetchrow("SELECT * FROM guildsettings_privatevc WHERE guild_id=$1", guild.id)


async def set_settings(bot: DiscordBot, guild: discord.Guild,
                       category: discord.CategoryChannel, voice: discord.VoiceChannel, text: discord.TextChannel):
    con = await bot.pool.acquire()
    await check(bot, guild)
    await con.execute(
        "UPDATE guildsettings_privatevc SET category_id=$1, default_vc_id=$2, default_tc_id=$3 WHERE guild_id=$4",
        category.id,
        voice.id,
        text.id,
        guild.id
    )


async def reset_settings(bot: DiscordBot, guild: discord.Guild):
    con = await bot.pool.acquire()
    await con.execute(
        "UPDATE guildsettings_privatevc SET category_id=null, default_vc_id=null, default_tc_id=null WHERE guild_id=$1",
        guild.id
    )


async def add_data(bot: DiscordBot,
                   user: discord.Member, guild: discord.Guild, tc: discord.TextChannel, vc: discord.VoiceChannel):
    con = await bot.pool.acquire()
    await con.execute(
        "INSERT INTO data_privatevc (user_id, guild_id, textchannel_id, voicechannel_id, time_created) VALUES"
        " ($1, $2, $3, $4, $5)"
        " ON CONFLICT DO NOTHING",
        user.id,
        guild.id,
        tc.id,
        vc.id,
        datetime.utcnow()
    )


async def fetch_data(bot: DiscordBot, user: discord.Member):
    con = await bot.pool.acquire()
    return await con.fetchrow(
        "SELECT * FROM data_privatevc WHERE user_id=$1 AND time_removed IS NULL",
        user.id
    )


async def update_data(bot: DiscordBot, user: discord.Member):
    con = await bot.pool.acquire()
    await con.execute(
        "UPDATE data_privatevc SET time_removed=$1 WHERE user_id=$2 AND time_removed IS NULL",
        datetime.utcnow(),
        user.id,
    )
