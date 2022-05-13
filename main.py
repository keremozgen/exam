#http://api.weatherstack.com/current ?access_key = a32c4922965b24cd68c1e04baeb0acc0    & query = Istanbul
#optional parameters:  units = m & language = en & callback = MY_CALLBACK

#Make a flask application and query current weather from weatherstack.com for Istanbul
#If it rains in Istanbul and Oslo, show an umbrealla icon
#If it is sunny, show a sun icon and the degree of the temperature
#If it is cold (less than 15 celcius), show a house icon
#If it is hot (more than 25 celcius), show a walking icon

import requests
import json
from flask import Flask, render_template


app = Flask(__name__)

#In the main page, show the current weather
@app.route('/')
def index():
    r = requests.get('http://api.weatherstack.com/current?access_key=a32c4922965b24cd68c1e04baeb0acc0&query=Istanbul')
    data = json.loads(r.text)
    #{'request': {'type': 'City', 'query': 'Istanbul, Turkey', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'Istanbul', 'country': 'Turkey', 'region': 'Istanbul', 'lat': '41.019', 'lon': '28.965', 'timezone_id': 'Europe/Istanbul', 'localtime': '2022-05-13 20:27', 'localtime_epoch': 1652473620, 'utc_offset': '3.0'}, 'current': {'observation_time': '05:27 PM', 'temperature': 22, 'weather_code': 113, 'weather_icons': ['https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'], 'weather_descriptions': ['Clear'], 'wind_speed': 4, 'wind_degree': 110, 'wind_dir': 'ESE', 'pressure': 1015, 'precip': 0, 'humidity': 38, 'cloudcover': 0, 'feelslike': 24, 'uv_index': 5, 'visibility': 10, 'is_day': 'no'}}
    #if it rains in Istanbul weather_descriptions': ['Rain'] show an umbrella
    istanbul_str = ''
    oslo_str = ''
    oslo_request = requests.get('http://api.weatherstack.com/current?access_key=a32c4922965b24cd68c1e04baeb0acc0&query=Oslo')
    oslo_data = json.loads(oslo_request.text)
    #If string contains 'Rain' show umbrella
    if 'Rain' in oslo_data['current']['weather_descriptions']:
        oslo_str += '<br> Oslo ☔'
    elif 'Sunny' in oslo_data['current']['weather_descriptions'][0]:
        oslo_str += '<br> Oslo ☀️'
    else:
        oslo_str += '<br> Oslo '
    oslo_str += str(oslo_data['current']['temperature']) + '°C' + str(oslo_data['current']['temperature'] < 15 and ' 🏠' or ' 🚶')

    if 'Rain' in data['current']['weather_descriptions'][0]:
        return 'Istanbul ☔' + oslo_str
    elif 'Sunny' in data['current']['weather_descriptions'][0]:
        istanbul_str = 'Istanbul ☀️'
    else:
        istanbul_str = 'Istanbul '
    istanbul_str += str(data['current']['temperature']) + '°C' + str(data['current']['temperature'] < 15 and ' 🏠' or ' 🚶')
    return istanbul_str + oslo_str

if __name__ == '__main__':
    #Print requests version
    print(requests.__version__)
    #Print json version
    print(json.__version__)
    app.run()
  