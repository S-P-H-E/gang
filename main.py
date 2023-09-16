import os
import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask, render_template_string

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

# Set up Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("Logged in as {{ bot_name }}", bot_name=bot.user.name)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        question = message.content
        response = generate_openai_response(question)
        await message.author.send(response)
    elif isinstance(message.channel, discord.TextChannel):
        if message.content.startswith('!ask'):
            question = message.content[5:]  # Remove the !ask part
            response = generate_openai_response(question)
            code_response = f'``` {response} ```'
            await message.channel.send(code_response)

    await bot.process_commands(message)

def generate_openai_response(question):
    prompt = f"Question: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the OpenAI engine you prefer
        prompt=prompt,
        max_tokens=50  # Adjust the response length as needed
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
