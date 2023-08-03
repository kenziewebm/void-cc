#!/usr/bin/env python3
import os
import json
import random
import discord
import requests
from signal import SIGTERM
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = ';', intents=intents)

global TOKEN
global CHANNEL_IDS
global FUNNY_CHANNEL

with open("../config.json", "r") as config_file:
        config_data = json.load(config_file)
        TOKEN = config_data.get('bot', {}).get('token')
        CHANNEL_IDS = config_data.get('bot', {}).get('channels', [])
        FUNNY_CHANNEL = config_data.get('bot', {}).get('funny_channel')

@client.event
async def on_ready():
        print("ready")

@client.event
async def on_message(message):
        # Ignore messages sent by the bot itself to avoid potential loops
        if message.author == client.user:
                return

        # Check if the message was sent in the #general channel and has an attachment
        if message.channel.id in CHANNEL_IDS and message.attachments:
                # Check if any attachment has a .py extension
                for attachment in message.attachments:
                        if attachment.filename.endswith('.py'):
                                # Delete the message with the .py attachment
                                await message.delete()
                                # Send the warning message to the author
                                await message.channel.send(f"HEY!!! THIS IS {message.channel.name} !!! DON\'T LEAK SHIT!!!")

        # Let the bot process commands as well
        await client.process_commands(message)

@client.command(brief = "Pings the bot",
                description = "Pings the bot and shows ping in ms")
async def ping(ctx):
        await ctx.send(f"pong! {round(client.latency * 1000)}ms")

@client.command(brief = "add account to database",
                description = "adds account to database")
async def add(ctx, user, login, cookies, authl, authp):
        params = {
                'user': user,
                'pass': login,
                'cookies': cookies,
        }

        response = requests.get('http://localhost:7272/addAccount', params=params, auth=(authl, authp))
        await ctx.message.delete()
        await ctx.send(response.content.decode())

@client.command(brief = "get accounts from database",
                description = "gets accounts from database")
async def get(ctx, user, login):
        response = requests.get('http://localhost:7272/getAccounts', auth=(user, login))
        await ctx.message.delete()
        # the fact that i have to download the file is retarded
        with open('/tmp/BD-accs.txt', 'wb') as f:
                f.write(response.content)
        accounts_file = discord.File("/tmp/BD-accs.txt", filename="accounts.txt")
        await ctx.send(file=accounts_file)
        os.remove('/tmp/BD-accs.txt')

@client.command(brief = "restart the bot",
                description = "restarts the bot")
async def restartbot(ctx):
        if int(ctx.message.author.id) == 424254493287251968:
                await ctx.send("Goodbye, world!")
                exit(0)
        else:
                await ctx.send("lol no")

@client.command(brief = "restart server",
                description = "restarts the server")
async def restartserver(ctx):
        if int(ctx.message.author.id) == 424254493287251968:
                pid = requests.get("http://localhost:7272/getPid")
                os.kill(int(pid.content.decode()), SIGTERM)
                await ctx.send("restarted server")
        else:
                await ctx.send("lol no")

@client.command(brief = 'i cant use emojis in here but pretend i put a trollface',
                description = 'trolle')
async def yiff(ctx, *, tags=str(None)): # retarded
        if ctx.message.channel.id != FUNNY_CHANNEL:
                await ctx.send("https://media.discordapp.net/attachments/814794831645114378/834328552761196574/SmartSelect_20210409-183226.jpg")
        else:
                headers = {
                        'User-Agent': 'the robot we kissed (by breadtard)',
                }

                params = {
                    'tags': 'rating:e ' + tags,
                    'limit': '10',
                }

                response = requests.get('https://e621.net/posts.json', params=params, headers=headers)
                data = response.json()
                posts = data['posts']

                # Extract all post URLs from the response
                post_urls = []
                for post in posts:
                         if 'file' in post and 'url' in post['file']:
                                post_url = post['file']['url']
                                post_urls.append(post_url)

                 # Use random.choice to pick a random post URL
                if post_urls:
                        random_post_url = random.choice(post_urls)
                        await ctx.send(random_post_url)
		else:
			await ctx.send("I bring the most unfortunate news. No results found.")

@client.command(brief = "Gets file from server",
		description = "Download file from the server.")
async def download(ctx, user, login, filepath):
	await ctx.message.delete()
	params = {
		'file': filepath,
	}

	response = requests.get('http://localhost:7272/downloadRes', params=params, auth=(user, login))
	with open('/tmp/BD-get.txt', 'wb') as f:
		f.write(response.content)
	resfile = discord.File("/tmp/BD-get.txt", filename=filepath)
	await ctx.send(file=resfile)
	os.remove('/tmp/BD-get.txt')

@client.command(brief = "Upload file to server",
		description = "Uploads a file to the server.")
async def upload(ctx, user, login):
	await ctx.message.delete()
	if len(ctx.message.attachments) == 0:
		await ctx.send("Attach a file bruh")
		return
	attachment = ctx.message.attachments[0]
	with open(attachment.filename, 'wb') as file:
		await attachment.save(file)

	files = {
		'file': open(attachment.filename, 'rb'),
	}

	response = requests.get('http://localhost:7272/uploadRes', files=files, auth=(user, login)) # i love using GET to upload files
	os.remove(attachment.filename)
	if response.status_code == 200:
		await ctx.send("done")
	else:
		await ctx.send(response.text)

@client.command(brief = "Runs git pull",
		description = "Runs git pull")
async def update(ctx):
	if int(ctx.message.author.id) == 424254493287251968:
		os.system("git pull")
		await ctx.send("done")
	else:
		await ctx.send("lolno")

client.run(TOKEN)
