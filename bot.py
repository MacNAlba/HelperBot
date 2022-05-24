import asyncio
import os
import asyncio
from asyncio import tasks

import ExamReminder
import Quoter
import discord
from dotenv import load_dotenv
import schedule
import time

# Main bot code
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
youtube = os.getenv('YOUTUBE_API')
guild = os.getenv('DISCORD_GUILD')
steamAPI = os.getenv('STEAM_API')
client = discord.Client()


@client.event  # Bot connected
async def on_ready():
    print(f'{client.user.name} has connected to the server!')


@client.event  # Message Listener
async def on_message(message):

    if message.author == client.user:
        return
    if "99" in message.content:
        response = Quoter.Brooklyn()
        await message.channel.send(response)
    elif "sunny" in message.content:
        response = Quoter.AlwaysSunnyQuote()
        await message.channel.send(response)
    elif "random" in message.content:
        response = Quoter.RandQuote()
        await message.channel.send(response)
    elif "graded unit" in message.content:
        response = ExamReminder.GUreminder()
        await message.channel.send(response)
    elif "ethical hacking project" in message.content:
        response = ExamReminder.EHPReminder()
        await message.channel.send(response)
    elif "ethical hacking theory" in message.content:
        response = ExamReminder.EHreminder()
        await message.channel.send(response)
    elif "muos" in message.content:
        response = ExamReminder.MUOSReminder()
        await message.channel.send(response)
    elif "report!" in message.content:
        response = ExamReminder.reportreminder()
        await message.channel.send(response)

@client.event # Error handler
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(token)
