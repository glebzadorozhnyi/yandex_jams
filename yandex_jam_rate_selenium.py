from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
import datetime
import csv

class jam:
    def __init__(self, rating):
        self.rating = rating
        now = datetime.datetime.utcnow()
        self.time = now.strftime("%d-%m-%Y %H:%M")
    def out_for_csv(self):
        return [self.time, self.rating]


def get_city_jam(city):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,)
    driver.get('https://yandex.ru/tune/geo')
    geolock = driver.find_element_by_id(id_='city__front-input')
    geolock.clear()
    geolock.send_keys(city)
    time.sleep(1)
    geolock.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    geolock.send_keys(Keys.RETURN)
    time.sleep(1)
    save_button = driver.find_element_by_class_name('button.button.form__save.button_theme_action.button_size_m.i-bem.button_js_inited')
    save_button.click()
    time.sleep(2)
    driver.get('https://yandex.ru/')
    time.sleep(2)
    jams = driver.find_element_by_class_name('traffic__rate-text').text
    driver.close()
    return jams

def save_log(cur_jam, exit_file):
    with open(exit_file, 'a',newline="") as file:
        writer = csv.writer(file)
        new_row = cur_jam.out_for_csv()
        writer.writerow(new_row)

current_jam = jam(get_city_jam('Москва'))
save_log(current_jam, 'ya_jams.csv')



