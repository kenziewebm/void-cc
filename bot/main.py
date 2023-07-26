#!/usr/bin/env python3
import os
import json
import discord
import requests
from signal import SIGTERM
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = '.', intents=intents)

global TOKEN
global CHANNEL_IDS

with open("../config.json", "r") as config_file:
	config_data = json.load(config_file)
	TOKEN = config_data.get('bot', {}).get('token')
	CHANNEL_IDS = config_data.get('bot', {}).get('channels', [])

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
	await ctx.send(response.content.decode())

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

client.run(TOKEN)
