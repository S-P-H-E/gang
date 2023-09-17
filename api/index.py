from flask import Flask
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv(".env.local")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()  # Enable default intents
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='hello')
async def hello(ctx):
    # Respond with "hello" when the "!hello" command is invoked
    await ctx.send('hello')

@app.route('/')
def home():
    return f'Logged in as {bot.user.name}'

@app.route('/about')
def about():
    return 'I AM A BOT'