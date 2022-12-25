import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Saver:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self._props_setter()

    def _props_setter(self):
        self.service = Service(
            '/chromedriver')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--headless')
        self.options.binary_location = '/usr/bin/google-chrome'

    def save_page(self) -> None:
        with webdriver.Chrome(options=self.options,
                              service=self.service) as driver:
            try:
                driver.get(self.url)
                driver.get_cookies()
                time.sleep(3)
                driver.execute_script('window.scrollTo(15,4666);')
                time.sleep(5)
                html = driver.page_source
                with open(f'saved_pages/{self.filename}', 'w', encoding='utf-8') as file:
                    file.write(html)
                print(f'page {self.filename} saved successfully!')
            except Exception as e:
                print(e)


def all_smartphones_pages_saver() -> None:
    url = 'https://www.ozon.ru/category/smartfony-15502/'

    # для сбора информации о первых 100 смартфонах спарсим 3 страницы, т.к. на одной стр 36 моделей
    num_pages = 3
    for i in range(1, num_pages + 1):
        filename = f'page_{i}.html'
        if i == 1:
            first_url = f'{url}?sorting=rating'
            Saver(first_url, filename).save_page()
        else:
            next_url = f'{url}?page={i}&?sorting=rating'
            Saver(next_url, filename).save_page()


def each_smartphone_pages_saver() -> None:
    with open(f'saved_pages/all_phones_links.csv', 'r') as file:
        sm_list = file.read().split('\n')[1:-1]
        for index, value in enumerate(sm_list):
            url = f'https://www.ozon.ru{value}'
            filename = f'saved_phones/{index}.html'
            Saver(url=url, filename=filename).save_page()
            time.sleep(random.randrange(4, 10))
