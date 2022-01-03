from datetime import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from os import remove, getenv
from dotenv import load_dotenv
import tweepy
import wget

load_dotenv()
CONSUMER_KEY = getenv('CONSUMER_KEY')
CONSUMER_SECRET = getenv('CONSUMER_SECRET')
ACCESS_KEY = getenv('ACCESS_KEY')
ACCESS_SECRET = getenv('ACCESS_SECRET')

#get formatted date values
date = datetime.now()
hour = date.hour
month = date.strftime('%m')
day = date.strftime('%d')
year = date.strftime('%Y')
def scrape_and_post_tweet():
    #determine how to format the hours for the URL, either '0800' or '1200'
    if(hour < 9):
        fhour = '0' + str(hour-1) + '00'
    else:
        fhour = str(hour-1) + '00'
    partialURL = 'https://cameras-cam.cdn.weatherbug.net/LSVRR/'

    #get formatted image URL then download it
    imgurl = partialURL + year + '/' + month + '/' + day + \
            '/' + month + day + year + fhour + '_l.jpg'
    img = wget.download(imgurl)
    print('img downloaded')
    #get weather data using selenium
    driver = Firefox(executable_path=('./drivers/geckodriver'))
    weatherURL = 'https://forecast.weather.gov/MapClick.php?lon=-115.433333333&lat=36.1333333333#.YdJ1xJuIYlp'
    driver.get(weatherURL)
    temperature = driver.find_element(By.CLASS_NAME, 'myforecast-current-lrg')
    status = 'The current temperature in Red Rock is ' + temperature.text + '. Photo courtesy of WeatherBug.com'

    # API v1.1 required to upload media to get mediaIDs & post tweet
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)


    #get media id and post tweet
    media = api.media_upload(img)
    res = api.update_status(status=status, media_ids=[media.media_id])
    print('tweet posted')
    remove(img)
    driver.close()
