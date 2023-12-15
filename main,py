from discord.ext import commands
import discord

import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="t.", intents=intents)

token = os.environ.get('DISCORD_API_TOKEN', None)
if token is None:
    raise Exception("Discord-Client-Token is required")
client.run(token)