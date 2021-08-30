import requests as re
from datetime import datetime
import csv

class weather():
    def __init__(self):
        self.obs_time = None
        self.temp = None
        self.feels_like = None
        self.condition = None
        self.wind_speed = None
        self.wind_dir = None

    def out_for_csv(self):
        return [self.obs_time, self.temp, self.feels_like, self.condition, self.wind_speed, self.wind_dir]

def save_log(weathers, exit_file):
    with open(exit_file, 'a', newline="") as file:
        writer = csv.writer(file)
        new_row = weathers.out_for_csv()
        writer.writerow(new_row)


url = 'https://api.weather.yandex.ru/v2/forecast?'
api_key = 'd07a6867-2093-4993-8581-f528b41d8ca7'
headers = {'X-Yandex-API-Key':api_key}
params = {'lat':'55.841', 'lon':'37.596', 'lang':'en_US', 'limit':'1', 'hours':'false', 'extra':'true'}
res = re.get(url,headers=headers, params=params)
data = res.json()
weather_now = weather()
weather_now.temp = data['fact']['temp']
weather_now.feels_like = data['fact']['feels_like']
weather_now.condition = data['fact']['condition']
weather_now.wind_speed = data['fact']['wind_speed']
weather_now.wind_dir = data['fact']['wind_dir']
obs_time_unix = data['now']
weather_now.obs_time = datetime.utcfromtimestamp(obs_time_unix).strftime('%Y-%m-%d %H:%M')
exit_file = 'yandex_temp_logs.csv'
save_log(weather_now, exit_file)