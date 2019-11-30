import discord
from discord.ext import commands

import datetime
import schedule
import time
import subprocess
import traceback
from discord.ext.commands import errors, converter
import requests
import random
from random import choice as rnd
from random import choice, randint
import threading
import aiohttp
import asyncio
import sys
import json

import config


bot = commands.Bot(command_prefix="&")


async def status_task():
    users = len(set(bot.get_all_members()))
    while True:
        await bot.change_presence(activity=discord.Game(name=f'&help | {str(len(bot.guilds))} guilds', type=2))
        await asyncio.sleep(30)
        
async def ctd_task():
    while True:
        if datetime.now().time() == datetime.time.fromisoformat('19:00:00.000001'):
            futuredate = datetime.strptime('Dec 25 2019  0:00', '%b %d %Y %H:%M')
            nowdate = datetime.now()
            count = int((futuredate-nowdate).total_seconds())
            days = round(count/86400)
            posts = db.utility.find_one({"utility": "santaconf"})
            for x in posts['channel']:
                channel = bot.get_channel(int(x))
                embed = discord.Embed(colour=0x9c0101, description=f"There are currently **{days}** until Christmas!")
                if x in posts['images']:
                    embed.set_image(url=rnd(randomimg.imgs))
                else: 
                    pass
                await channel.send(embed=embed)
         else:
            pass
         asyncio.sleep(0.5)

@bot.event
async def on_ready():
    print('\x1b[1;34;40m' + 'Discord Version: ' + '\x1b[0m' + f'{discord.__version__}\n------')
    print('\x1b[1;36;40m' + '[UPDATE]: ' + '\x1b[0m' + f'Logged in as: {bot.user.name} ({str(bot.user.id)})')
    print("\x1b[1;33;40m" + "[AWAITING]: " + "\x1b[0m" + "Run 'r!load all'")
    bot.loop.create_task(status_task())
    bot.loop.create_task(ctd_task())

@bot.event
async def on_guild_join(guild):
    server = guild
    targets = [
            discord.utils.get(server.channels, name="bot"),
            discord.utils.get(server.channels, name="bots"),
            discord.utils.get(server.channels, name="bot-commands"),
            discord.utils.get(server.channels, name="bot-spam"),
            discord.utils.get(server.channels, name="bot-channel"),
            discord.utils.get(server.channels, name="testing"),
            discord.utils.get(server.channels, name="testing-1"),
            discord.utils.get(server.channels, name="general"),
            discord.utils.get(server.channels, name="shitposts"),
            guild.get_member(guild.owner.id)
            ]
    embed = discord.Embed(description="Thank you for adding me! Do `&help` to see a list of my commands. To set up daily countdown messages, do `&setcc`.")
    embed.set_footer(text="Santa created by lukee#0420 - Thank you for adding me!", icon_url=bot.user.avatar_url)
    for x in targets:
        try:
            await x.send(embed=embed)
        except:
            continue
        break


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await bot.process_commands(message)


if __name__ == '__main__':
    bot.remove_command("help")
    bot.load_extension("cogs.bot")
    bot.load_extension("cogs.help")
    bot.load_extension("cogs.main")


bot.run(config.token, bot=True, reconnect=True)
