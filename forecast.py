# File dependencies
import config as cfg
import colorHandler as color
# Command Dependencies
import discord
from discord.ext import commands
# data Dependencies
import json
import requests
# Image dependencies
from skimage import io, img_as_float
import urllib.request
import io as sysio


# Command Prefix
client = commands.Bot(command_prefix="c!")

# Initialization
@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"The Forecast!"))

# Weather command
@client.command()
async def weather(message, *args):
    # Check for errors
    if len(args) < 1:
        await message.channel.send(embed = discord.Embed(title="❌ Error", description = "Please enter a location!", color = 0xd63f3f))
        return True
    # Get API request key and query
    params = {
        'access_key': 'f94750a0bd28417e135bb2c85b4ae93e',
        'query': " ".join(args)
    }
    r = requests.get("http://api.weatherstack.com/current", params)
    response = r.json()
    current = response['current']
    request = response['request']
    location = response['location']
#Get Info via Handler
    embeds = {
        "title": "Weather",
        "description": f"Forecast for {request['query']}",
        "color": color.getAverageColor(current['weather_icons'][0]),
        "footer": f"Last Updated: {current['observation_time']} ({location['name']})",
        "thumbnail": f"{current['weather_icons'][0]}",
        "pageOne": {
                "fields": [
                    {
                        "name": "Celsius (°C)",
                        "value": f"{current['temperature']}° C",
                    },
                    {
                        "name": "Farenheit (°F)",
                        "value": f"{round((current['temperature'] * 9/5) + 32)}° F"
                    },
                ]
            },
        "pageTwo": {
                "fields": [
                    {
                        "name": "Humidity",
                        "value": f"{current['humidity']}"
                    },
                    {
                        "name": "Observation Time",
                        "value": f"{current['observation_time']}"
                    },
                    {
                        "name": "Weather Description",
                        "value": f"{current['weather_descriptions'][0]}"
                    }
                ]
        }
    }

# Actual embed text from JSON page1
    pageOne = discord.Embed(title=embeds["title"], color=embeds["color"], description=embeds["description"])
    for fields in embeds["pageOne"]["fields"]:
        pageOne.add_field(name=fields["name"], value=fields["value"], inline=False)
    pageOne.set_thumbnail(url=embeds["thumbnail"])
    pageOne.set_footer(text=embeds["footer"])

    pageTwo = discord.Embed(title=embeds["title"], color=embeds["color"], description=embeds["description"])
    for fields in embeds["pageTwo"]["fields"]:
        pageTwo.add_field(name=fields["name"], value=fields["value"], inline=False)
    pageTwo.set_thumbnail(url=embeds["thumbnail"])
    pageTwo.set_footer(text=embeds["footer"])

    embed_response = await message.channel.send(embed=pageOne)
    await embed_response.add_reaction('◀')
    await embed_response.add_reaction('▶')

    pages = [pageOne, pageTwo]

    def check(reaction, user):
        return user == message.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '▶':
            if i == 0:
                i += 1
                await embed_response.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await embed_response.edit(embed = pages[i])
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await embed_response.remove_reaction(reaction, user)
        except:
            break

    await embed_response.clear_reactions()

# Run bot
client.run(cfg.BOT_TOKEN)