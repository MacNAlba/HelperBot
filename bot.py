import os
import requests
from discord.ext import commands
import ExamReminder
import Quoter
import discord
from dotenv import load_dotenv
import json

bot = commands.Bot(command_prefix="!")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
youtube = os.getenv('YOUTUBE_API')
guild = os.getenv('DISCORD_GUILD')
steamAPI = os.getenv('STEAM_API')
# bot = discord.Client()
weatherAPI = os.getenv('WEATHER_API')
weatherURL = os.getenv('WEATHER_URL')


@bot.event  # Bot connected
async def on_ready():
    print(f'{bot.user.name} has connected to the server!')


@bot.event  # Message Listener
async def on_message(message):
    if message.author == bot.user:
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
    await bot.process_commands(message)


@bot.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = weatherURL + city_name + "&appid=" + weatherAPI
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel

    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celcius = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]

            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}", color=ctx.guild.me.top_role.color,
                                  timestamp=ctx.message.created_at, )
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celcius}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        await channel.send(embed=embed)
    else:
        await channel.send("City not found.")


@bot.command()
async def test(ctx):
    response = "Successful test"
    await ctx.send(response)


@bot.event  # Error handler
async def on_error(event, *args, **kwargs):
    with open('errors.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


bot.run(token)
