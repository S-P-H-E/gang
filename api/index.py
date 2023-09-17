import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Load environment variables from .env.local
load_dotenv(".env.local")

# Retrieve API keys from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HTTP_SERVER_PORT = int(os.getenv("HTTP_SERVER_PORT"))

intents = discord.Intents.default()  # Enable default intents
intents.typing = False  # You can adjust intents based on your bot's functionality

# Set up the Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='hello')
async def hello(ctx):
    # Respond with "hello" when the "!hello" command is invoked
    await ctx.send('hello')

class HTTPServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))

def start_http_server():
    server = HTTPServer(('0.0.0.0', HTTP_SERVER_PORT), HTTPServerHandler)
    server.serve_forever()

# Start the HTTP server in a separate thread
http_server_thread = threading.Thread(target=start_http_server)
http_server_thread.daemon = True  # This will allow the thread to exit when the main program exits
http_server_thread.start()

bot.run(DISCORD_TOKEN)