from http.server import BaseHTTPRequestHandler
import os
import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(".env.local")

# Retrieve API keys from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()  # Enable default intents
intents.typing = False  # You can adjust intents based on your bot's functionality

# Set up the Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        question = message.content
        try:
            response = generate_openai_response(question)
            await message.author.send(response)
        except Exception as e:
            await message.author.send(f"An error occurred: {str(e)}")
    elif isinstance(message.channel, discord.TextChannel):
        if message.content.startswith('!ask'):
            question = message.content[5:]  # Remove the !ask part
            try:
                response = generate_openai_response(question)
                code_response = f'``` {response} ```'
                await message.channel.send(code_response)
            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")

    await bot.process_commands(message)

def generate_openai_response(question):
    prompt = f"Question: {question}\nAnswer:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the OpenAI engine you prefer
            prompt=prompt,
            max_tokens=50  # Adjust the response length as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"

bot.run(DISCORD_TOKEN)
