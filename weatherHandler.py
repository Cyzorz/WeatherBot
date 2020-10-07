#Obsolete file, refer to next commit.
import json
import requests
import config as cfg
from dateutil import parser
import forecast as main


def searchWeatherInfo(x): 
     requests.post(cfg.WEBHOOK_URL, data=json.dumps({
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
                    }
                ],
                "footer": {"text":f"Last Updated: {current['observation_time']} ({location['name']})"}
            }
        ]
     }), headers={"Content-Type": "application/json"})
params = {
    'access_key': 'f94750a0bd28417e135bb2c85b4ae93e',
    'query': 'San Francisco'
}
r = requests.get("http://api.weatherstack.com/current", params)
response = r.json()
current = response['current']
request = response['request']
location = response['location']