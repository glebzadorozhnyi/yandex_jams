import requests
from bs4 import BeautifulSoup
url = 'https://yandex.ru/'
soup = BeautifulSoup(requests.get(url).text, 'lxml')
jam = soup.find('div', attrs={'class' : 'traffic__rate-text'}).text
print(jam)