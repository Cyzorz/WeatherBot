# File dependencies
import config as cfg
import colorHandler as color
# Command Dependencies
import discord
from discord.ext import commands
# Data Dependencies
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
        await message.channel.send(embed = discord.Embed(title="Error ❌", description = "Please enter a location!", color = 0xd63f3f))
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
    data = {
        "embeds": [
            {
                "title": "Weather",
                "description": f"Forecast for {request['query']}",
                "color": 808080,
                "fields": [
                    {
                        "name": "Celsius (°C)",
                        "value": f"{current['temperature']}° C",
                    },
                    {
                        "name": "Farenheit (°F)",
                        "value": f"{round((current['temperature'] * 9/5) + 32)}° F"
                    },
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
                ],
                "footer": {"text":f"Last Updated: {current['observation_time']} ({location['name']})"}
            }
        ]
    }

# Actual embed text from JSON data
    embed = discord.Embed(title = data['embeds'][0]['title'], description = data['embeds'][0]['description'], color = data['embeds'][0]['color'])
    embed.set_thumbnail(url = f"{current['weather_icons'][0]}")
    embed.add_field(name = data['embeds'][0]['fields'][0]['name'], value = data['embeds'][0]['fields'][0]['value'], inline = True)
    embed.add_field(name = data['embeds'][0]['fields'][1]['name'], value = data['embeds'][0]['fields'][1]['value'], inline= True)
    embed.add_field(name = data['embeds'][0]['fields'][2]['name'], value = data['embeds'][0]['fields'][2]['value'], inline= False)
    embed.add_field(name = data['embeds'][0]['fields'][3]['name'], value = data['embeds'][0]['fields'][3]['value'], inline = True)
    embed.add_field(name = data['embeds'][0]['fields'][4]['name'], value = data['embeds'][0]['fields'][4]['value'], inline = False)
    embed.set_footer(text = data['embeds'][0]['footer']['text'])
    await message.channel.send(embed=embed)

# Run bot
client.run(cfg.BOT_TOKEN)