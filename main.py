import discord
import openai
from discord.ext import commands

intents = discord.Intents.default()  # Enable default intents
intents.typing = False  # You can adjust intents based on your bot's functionality

# Set up the Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Configure OpenAI
openai.api_key = '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'

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

bot.run('MTE0NTA3NzI1NzE1Nzc1MDgwNA.GWpp-q.C0sHgnM0JQOnSFEdmVzX__MtzgZuD4Btf8-tIw')

#DISCORD: MTE0NTA3NzI1NzE1Nzc1MDgwNA.GWpp-q.C0sHgnM0JQOnSFEdmVzX__MtzgZuD4Btf8-tIw
#OPENAI: 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