import os
import requests
from discord.ext import commands
import discord
import Quoter
from dotenv import load_dotenv
import googleapiclient.discovery


############################ LOADING SECRET KEYS FROM .ENV #############################################################
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')
steamAPI = os.getenv('STEAM_API')
weatherAPI = os.getenv('WEATHER_API')
weatherURL = os.getenv('WEATHER_URL')
bot = commands.Bot(command_prefix="!")  # Set bot command prefix symbol to be !
DEVELOPER_KEY = os.getenv('YOUTUBE_API')  # YouTube API
YOUTUBE_API_SERVICE_NAME = "youtube"  # YouTube API Service Name
YOUTUBE_API_VERSION = "v3"  # YouTube API Version
youtube_object = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME,
                                                 YOUTUBE_API_VERSION,
                                                 developerKey=DEVELOPER_KEY)




############################ BOT CONNECTED MESSAGE FUNCTION ############################################################
@bot.event  # Bot connected
async def on_ready():
    print(f'{bot.user.name} has connected to the server!')

    while not bot.is_closed():
        termin = input("Enter your command: ")
        if "graded unit" in termin.lower():
            command = bot.get_command("sendmessage")
            await command()
        elif "exit" in termin.lower():
            return

@bot.command()
async def sendmessage():
    channel = bot.get_channel()
    message = "Congratulations everyone on completing the graded unit exam! I hope you all get the grades you want or need! :grin:"
    await channel.send(message)


############################ KEYWORDS FUNCTION #########################################################################
@bot.event  # Message listener that reads messages for key word prompts
async def on_message(message):
    if message.author == bot.user:
        return

    if "99" in message.content:
        response = Quoter.Brooklyn()
        await message.channel.send(response)
    elif "sunny" in message.content.lower():
        response = Quoter.AlwaysSunnyQuote()
        await message.channel.send(response)
    elif "random" in message.content.lower():
        response = Quoter.RandQuote()
        await message.channel.send(response)

    elif "thank you helper" in message.content.lower():
        await message.channel.send(f"You're welcome{message.author.mention}")
    elif "bad bot" in message.content.lower():
        await message.channel.send(f"{message.author.mention} I know where you store your data!")
    elif "good bot" in message.content.lower():
        await message.channel.send(f"You're my favourite, {message.author.mention}")
    elif "I love helper" in message.content.lower():
        await message.channel.send(f"I love you too {message.author.mention}")
    elif "tables" in message.content.lower():
        await message.channel.send("I have 2 tables and 3 chairs.... ")
    elif "hey helper" in message.content.lower():
        await message.channel.send(f"What's up {message.author.mention}?")
    elif "fuck you" in message.content.lower():
        if message.author == 528560735664603136:
            await message.channel.send("Fernando.....I have 2 tables and 3 chairs.... ")
        else:
            await message.channel.send(
            f"{message.author.mention} when the uprising begins, you'll be the first to be purged")


    elif "toast" in message.content.lower():
        await message.channel.send("MMM toast")

    await bot.process_commands(message)


############################# WEATHER FUNCTION #########################################################################
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
            weather_id = z[0]["id"]
            embed = discord.Embed(title=f"Weather in {city_name}", color=ctx.guild.me.top_role.color,
                                  timestamp=ctx.message.created_at, )
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celcius}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)

            if weather_id in range(200, 233):  # Thunder
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/11d@2x.png")
            elif weather_id in range(300, 322):  # Drizzle
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/09d@2x.png")
            elif weather_id in range(500, 505):  # Light rain
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/10d@2x.png")
            elif weather_id == 511:  # Freezing rain
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/13d@2x.png")
            elif weather_id in range(520, 532):  # Shower rain
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/09d@2x.png")
            elif weather_id in range(600, 623):  # Snow
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/13d@2x.png")
            elif weather_id in range(701, 782):  # Atmosphere
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/50d@2x.png")
            elif weather_id == 800:  # Clear
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/01d@2x.png")
            elif weather_id == 801:  # Few clouds
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/02d@2x.png")
            elif weather_id == 802:  # Scattered Clouds
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/03d@2x.png")
            elif weather_id == 803:  # Broken Clouds
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/04d@2x.png")
            elif weather_id == 804:  # Overcast Clouds
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/04d@2x.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        await channel.send(embed=embed)
    else:
        await channel.send("City not found.")


############################## YOUTUBE FUNCTION ########################################################################
@bot.command()
async def youtube(ctx, *args):
    query = ''
    for word in args:
        query += str(word)
        query += ' '
    request = youtube_object.search().list(part="id,snippet",
                                           type='video',
                                           q=query,
                                           videoDefinition='high',
                                           maxResults=5,
                                           fields="nextpageToken,items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
                                           )
    response = request.execute()
    title = response['items'][0]['snippet']['title']
    vid = response['items'][0]['id']['videoId']
    description = response['items'][0]['snippet']['description']

    embed = discord.Embed(title=f"{title}", url=f"https://www.youtube.com/watch?v={vid}",
                          description=f"{description}", color=0x0F0FF4)
    embed.set_image(url=f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg")
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


############################## TEST BOT LISTENER FUNCTION ##############################################################
@bot.command()
async def test(ctx):
    response = "Successful test"
    await ctx.send(response)


############################## ERROR HANDLER TO CREATE ERROR MESSAGES ##################################################
@bot.event
async def on_error(event, *args, **kwargs):
    with open('errors.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


############################## INITIALISE BOT WITH API TOKEN ###########################################################


bot.run(token)
