#file dependencies
import weatherHandler as forecast
import config as cfg
import colorHandler as color
#Command Dependencies
import discord
from discord.ext import commands
#Data Dependencies
import json
import requests
#Image dependencies
from skimage import io, img_as_float
import urllib.request
import io as sysio


#command prefix for weather
client = commands.Bot(command_prefix="c!")

#presence, console message 
async def on_ready(self):
    await self.wait_until_ready()
    print(self.user.name + " is ready, ID: " + str(self.user.id))
    count = len(client.users)
    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{count} users | n!help"))

#weather command, handler(s) not attatched (refer to next commit)
@client.command()
async def weather(message, *args):
#URL json data to load on embed
    params = {
        'access_key': 'f94750a0bd28417e135bb2c85b4ae93e',
        'query': " ".join(args)
    }
#Embed data from JSON data URL
    r = requests.get("http://api.weatherstack.com/current", params)
    response = r.json()
    current = response['current']
    request = response['request']
    location = response['location']
    data = {
        "content": "WeatherBot",
        "embeds": [
            {
                "title": "Weather",
                "description": f"Weather for {request['query']}",
                "thumbnail": {"url": current['weather_icons']},
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
                    }
                ],
                "footer": {"text":f"Last Updated: {current['observation_time']} ({location['name']})"}
            }
        ]
    }

#Actual embed text from JSON data
    embed = discord.Embed(title = data['embeds'][0]['title'], description = data['embeds'][0]['description'], color = data['embeds'][0]['color'])
    embed.set_thumbnail(url = f"{current['weather_icons'][0]}")
    embed.add_field(name = data['embeds'][0]['fields'][0]['name'], value = data['embeds'][0]['fields'][0]['value'])
    embed.add_field(name = data['embeds'][0]['fields'][1]['name'], value = data['embeds'][0]['fields'][1]['value'], inline=False)
    embed.add_field(name = data['embeds'][0]['fields'][2]['name'], value = data['embeds'][0]['fields'][2]['value'], inline=False)
    embed.set_footer(text = data['embeds'][0]['footer']['text'])
    await message.channel.send(embed=embed)

#run bot
client.run(cfg.BOT_TOKEN)