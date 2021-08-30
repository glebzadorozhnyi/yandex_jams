import requests
from bs4 import BeautifulSoup
import datetime
import csv
import time
import re

class route:
    def __init__(self, travel_time, current_time, route_type=None, km=None, travel_time_without_traffic=None):
        self.travel_time = travel_time
        self.km = km
        self.travel_time_without_traffic = travel_time_without_traffic
        self.current_time = current_time.strftime("%d-%m-%Y %H:%M")
        self.route_type = route_type

    def __str__(self):
        string = 'log time: {}, route {}, time with traffic: {}, time without traffic: {},  route length: {}'.format(self.current_time, self.route_type, self.travel_time, self.travel_time_without_traffic, self.km)
        return string
    def out_for_csv(self):
        return [self.current_time, self.route_type, self.travel_time, self.travel_time_without_traffic, self.km]

def get_routes_by_url(url, route_type, sort_by_km=False):
    now = datetime.datetime.utcnow()
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    routes_time = soup.find_all('div', attrs={'class' : 'auto-route-snippet-view__route-title-primary'})
    routes_km = soup.find_all('div', attrs={'class' : 'auto-route-snippet-view__route-subtitle'})
    all_routes = list()
    for i, element in enumerate(routes_time):
        km_and_minute = routes_km[i].text.split(sep=', Без пробок: ')
        km = km_to_digits(km_and_minute[0])
        minute = convert_to_time(km_and_minute[1])
        all_routes.append(route(convert_to_time(element.text), now, route_type=route_type, km=km, travel_time_without_traffic=minute))
    if sort_by_km:
        all_routes.sort(key=lambda route : route.km)
    return all_routes

def save_log(route, exit_file):
    with open(exit_file, 'a',newline="") as file:
        writer = csv.writer(file)
        for element in route:
            new_row = element.out_for_csv()
            writer.writerow(new_row)

def km_to_digits(km):
    pattern = '\d+'
    return re.search(pattern,km).group() + ' km'

def convert_to_time(time):
    pattern = '\d+'
    time = re.findall(pattern,time)
    if len(time) == 1:
        return time[0] + ' m'
    return time[0] + ' h ' + time[1] + ' m'


#print('Маршрут от Работы до Дома')
url = 'https://yandex.ru/maps/-/CCU46WBNOB'
exit_file = 'yandex_maps_logs.csv'
work_to_home = get_routes_by_url(url, 'from work')
save_log(work_to_home, exit_file)
time.sleep(5)
#print('Маршрут из Дома на Работу')
url = 'https://yandex.ru/maps/-/CCU4fEABgD'
work_to_home = get_routes_by_url(url, 'to work')
save_log(work_to_home, exit_file)
print('success')


