import os
import asyncio
import logging
import json

from dotenv import load_dotenv
from nextcord.ext.commands import Bot
from nextcord.ext import commands
from nextcord import (
    AllowedMentions,
    Intents,
    Status,
    Activity,
    MemberCacheFlags
)

load_dotenv()

logger = logging.basicConfig(
    format='[%(asctime)s] %(process)d-%(levelname)s : %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S', 
    filename='zoey-errors.log', 
    level=logging.WARNING
)

intents = Intents.none()
intents.guilds = True
intents.invites = True
intents.members = True
intents.voice_states = True
intents.guild_messages = True
intents.guild_reactions = True

bot = commands.Bot(
    status=Status.idle, 
    activity=Activity(name=f'over the table.', type=3),
    allowed_mentions=AllowedMentions(everyone=False, users=True, roles=False),
    member_cache_flags=MemberCacheFlags(voice=False, joined=False),
    command_prefix="-", 
    case_insensitive=True,
    chunk_guilds_at_startup=False,
    strip_after_prefix=True,
    help_command=None,
    max_messages=2500,
    intents=intents,
    heartbeat_timeout=20.0
)

with open ('config.json') as f: 
    config_json = json.load(f)
    bot.blacklisted_words = config_json['blacklisted_words']
    bot.moderation_log_channel_id = config_json['moderation_log_channel_id']
    bot.message_log_channel_id = config_json['message_log_channel_id']
    bot.ban_message_raw = config_json['ban_message']
    bot.kick_message_raw = config_json['kick_message']

@bot.command()
async def ping(ctx, ):
    ping = round(bot.latency / 1000,1)
    await ctx.reply(f"🐍 Pong! `{ping}ms`",delete_after=12)
    try:
        await ctx.delete(delay=12)
    except:
        pass
    
@bot.command()
@commands.has_any_role(940357593912705066)
async def reload(ctx, module: str):
    try:
        bot.reload_extension(f"cogs.{module}")
        await ctx.send(f"`🔁` | Reloaded **cogs.{module}**")
    except Exception as error: 
        await ctx.reply(f"`⚠️` | Could not reload `cogs.{module}`\n```{error}```")

@bot.command()
@commands.has_any_role(940357593912705066)
async def unload(ctx, module: str):
    try:
        bot.unload_extension(f"cogs.{module}")
        await ctx.send(f"`📤` | Unloaded **cogs.{module}**")
    except Exception as error: 
        await ctx.reply(f"`⚠️` | Could not unload `cogs.{module}`\n```{error}```")

@bot.command()
@commands.has_any_role(940357593912705066)
async def load(ctx, module: str):
    try:
        bot.load_extension(f"cogs.{module}")
        await ctx.send(f"`📥` | Loaded **cogs.{module}**")
    except Exception as error: 
        await ctx.reply(f"`⚠️` | Could not load `cogs.{module}`\n```{error}```")
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.add_reaction("⏰")
        return await ctx.reply(f"`⏰` | You're on cooldown. | Try again in **{int(error.retry_after)}s**.", delete_after=error.retry_after if error.retry_after <= 60 else None)
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.reply(f"`🧦` | You're lacking the following permission `{list(error.missing_perms)[0]}`.")
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.reply("`🚨` | You're missing a required argument!")
    elif isinstance(error, commands.TooManyArguments):
        return await ctx.reply("`🚨` | You've given me too many arguments!")
    elif isinstance(error, commands.BadArgument):
        return await ctx.reply("`🚨` | I'm not sure what one of your arguments is!")
    elif not isinstance(error, commands.CommandNotFound):
        return logging.warning(error)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
    elif os.path.isfile(filename):
        logging.warning(f"Unable to load {filename[:-3]}")

bot.run(os.getenv('TOKEN'))
