from datetime import datetime
import requests
from os import remove, getenv, path
from dotenv import load_dotenv
import tweepy
import wget

load_dotenv()
CONSUMER_KEY = getenv('CONSUMER_KEY')
CONSUMER_SECRET = getenv('CONSUMER_SECRET')
ACCESS_KEY = getenv('ACCESS_KEY')
ACCESS_SECRET = getenv('ACCESS_SECRET')
WEATHER_API = getenv('WEATHER_API')

#get formatted date values
date = datetime.now()
hour = date.hour
month = date.strftime('%m')
day = date.strftime('%d')
year = date.strftime('%Y')
city = 'calico+basin'

#determine how to format the hours for the URL, either '0800' or '1200'
if(hour < 9):
    fhour = '0' + str(hour-1) + '00'
else:
    fhour = str(hour-1) + '15'
partialURL = 'https://cameras-cam.cdn.weatherbug.net/LSVRR/'

#get formatted image URL then download it
imgurl = partialURL + year + '/' + month + '/' + day + \
        '/' + month + day + year + fhour + '_l.jpg'
img = wget.download(imgurl)
print('img downloaded')

#get weather data using openweatherAPI
response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + WEATHER_API)
kelvin = (response.json()['main']['temp'])
fahrenheit = str(round((kelvin - 273.15) * (9/5) + 32)) 
status = 'The current temperature in Red Rock is ' + fahrenheit + '°F. Photo courtesy of WeatherBug.com'

# API v1.1 required to upload media to get mediaIDs & post tweet
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#get media id and post tweet
media = api.media_upload(img)
res = api.update_status(status=status, media_ids=[media.media_id])
print('tweet posted')

remove(img)
