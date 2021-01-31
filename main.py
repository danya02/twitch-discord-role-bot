import discord
from discord.ext import commands
import os
import dotenv
import requests

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TWITCH_CLIENT = os.getenv('TWITCH_CLIENT')
TWITCH_SECRET = os.getenv('TWITCH_SECRET')

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(DISCORD_TOKEN)

