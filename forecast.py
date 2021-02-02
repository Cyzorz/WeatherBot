# File dependencies
import config as cfg
import colorHandler as color
# Command Dependencies
import discord
from discord.ext import commands
# Data Dependencies
import requests

# Command Prefix
client = commands.Bot(command_prefix=cfg.COMMAND_PREFIX)

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
    # Embed data, cannot be put into another file due to circular imports (specifically, using the command arguments in another file)
    embeds = {
        "title": "Weather",
        "description": f"Forecast for {request['query']}",
        "color": color.getAverageColor(current['weather_icons'][0]),
        "page_one_footer": f"Last Updated: {current['observation_time']}\n1/2",
        "page_two_footer": f"Last Updated: {current['observation_time']}\n2/2",
        "thumbnail": f"{current['weather_icons'][0]}",
        "page_one": {
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
        "page_two": {
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

    # Embed building for pages
    page_one = discord.Embed(title=embeds["title"], color=embeds["color"], description=embeds["description"])
    for fields in embeds["page_one"]["fields"]:
        page_one.add_field(name=fields["name"], value=fields["value"], inline=False)
    page_one.set_thumbnail(url=embeds["thumbnail"])
    page_one.set_footer(text=embeds["page_one_footer"])

    page_two = discord.Embed(title=embeds["title"], color=embeds["color"], description=embeds["description"])
    for fields in embeds["page_two"]["fields"]:
        page_two.add_field(name=fields["name"], value=fields["value"], inline=False)
    page_two.set_thumbnail(url=embeds["thumbnail"])
    page_two.set_footer(text=embeds["page_two_footer"])

    embed_response = await message.channel.send(embed=page_one)
    await embed_response.add_reaction('◀')
    await embed_response.add_reaction('▶')

    # Add pages to list
    pages = [page_one, page_two]

    def check(reaction, user):
        return user == message.author

    # Set initial page to 0 and reactions to none
    i = 0
    reaction = None

    # Loop to check if reactions have been used, i being the page number corresponding to the pages list above
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
            reaction, user = await client.wait_for('reaction_add', check = check)
            await embed_response.remove_reaction(reaction, user)
        except:
            break
    await embed_response.clear_reactions()

# Run bot
client.run(cfg.BOT_TOKEN)