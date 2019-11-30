import discord
from discord.ext import commands
import datetime
import requests
import random
import math
import time
from discord.ext.commands import errors, converter
from random import choice, randint
from random import choice, randint as rnd
import aiohttp
import asyncio
import json
import os
import config

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '&'

    @commands.command(aliases=['cmds', 'commands', 'Help'])
    async def help(self, ctx):
        embed = discord.Embed(colour=0x9c0101, description='Hello, I am **Santa**! Here is a list of commands that you are able to use.\n\n'\
        f'`{self.prefix}countdown` - **View the countdown until Christmas**\n'\
        f'`{self.prefix}heartbeats` - **View how many days until Christmas**\n'\
        f'`{self.prefix}status` - **View boost status for this server.**\n'\
        f'`{self.prefix}user <@user>` - **Check boost stats for a user**\n'\
        f'`{self.prefix}boostmessage [message]` - **Set boost message** - Admin Only\n'
        )
        #embed.set_image(url="https://i.ibb.co/chxrYtn/restaurantbanner.png")
        embed.set_footer(text="Arguments are inside [] and <>. [] is optional and <> is required. Do not include [] or <> in the command.")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Help(bot))
