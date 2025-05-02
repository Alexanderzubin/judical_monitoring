import traceback
import requests
from bs4 import BeautifulSoup
from requests import RequestException
import logging

url = 'https://krasnodar-prikubansky--krd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=case&case_id=257838257&case_uid=5c28649b-9910-4493-aede-8e95b89b7061&delo_id=1540005&new='

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36 "

}


class CasePageParse:
    def __init__(self, url: str,
                 logger: logging.Logger,
                 cookies: dict[str, str] | None = None,
                 proxies: dict[str, str] | None = None,
                 headers: dict[str, str] | None = None):
        self.url = url
        self.cookies = cookies
        self.proxies = proxies
        self.logger = logger

        if headers is None or headers == {}:
            self.headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) "
                              "Chrome/58.0.3029.110 Safari/537.36 "

            }
        else:
            self.headers = headers

    def get_case_data(self):
        case_data = {
            'number': None,
            'unique_identifier': None,
            'judge': None,
            'date_of_receipt': None,
            'url': self.url,
            'court': None,
            'categories': None,
        }

        response = self.get_case_page()

        if response:
            soup = self.convert_response_to_bs4(response)
            case_data['number'] = self.get_case_number(soup)
            case_data.update(self.get_case_table(soup))

        return case_data

    def get_case_page(self) -> requests.Response | None:

        try:
            response = requests.get(self.url, headers=self.headers, cookies=self.cookies, proxies=self.proxies)

            if response.status_code == 200:
                return response
            else:
                self.logger.warning(f'{response.text}')

        except RequestException as exc:
            self.logger.error(f'При получении страницы возникла ошибка: {exc}')

    def convert_response_to_bs4(self, response: requests.Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_case_number(self, soup):

        case_number = soup.select_one('div.casenumber')
        case_number_txt = case_number.text
        return case_number_txt.split()[2]

    def get_case_table(self, soup: BeautifulSoup) -> dict | None:

        try:
            table = (soup.find('table', {'id': 'tablcont'}) or
                     soup.find('table', {'class': 'table'}) or
                     soup.find('table'))

            if not table:
                self.logger.warning("Таблица не найдена на странице")
                return None

            table_data = []

            all_rows = table.select_one('tr')  # Находим все строки в таблице

            for row in all_rows:  # Пропускаем строку, если это заголовок (содержит th)
                if row.find('th') or 'ДЕЛО' == row.text.strip():
                    continue

                current_row = {}  # Создаем пустой словарь для текущей строки

                cells = row.find_all('td')  # Находим все ячейки в строке

                # Добавляем данные в словарь
                current_row['unique_identifier'] = cells[1].text.strip() if len(cells) > 0 else ''
                current_row['judge'] = cells[7].text.strip() if len(cells) > 1 else ''
                current_row['date_of_receipt'] = cells[3].text.strip() if len(cells) > 2 else ''
                current_row['court'] = cells[9].text.strip() if len(cells) > 2 else ''
                current_row['categories'] = cells[5].text.strip() if len(cells) > 2 else ''

            return current_row

        except Exception as exc:
            self.logger.error(f"Ошибка при парсинге таблицы с карточкой дела: {exc}")
            self.logger.error(traceback.format_exc(limit=3))
            return None

    def get_event_data(self, ):
        event_data = {
            'name': None,
            'date': None,
            'time': None,
            'result': None,
            'the_basic_for_the_selected_result': None,
            'date_of_placement': None,
        }

        response = self.get_case_page()

        if response:
            soup = self.convert_response_to_bs4(response)
            event_data.update(self.get_event_table(soup))

        return event_data

    def get_event_table(self, soup: BeautifulSoup) -> dict | None:

        try:

            div = soup.find('div', id='cont2')
            table = div.find('table', id='tablcont')

            if not table:
                self.logger.warning("Таблица не найдена на странице")
                return None

            all_rows = table.select_one('tr')  # Находим все строки в таблице

            for row in table:  # Пропускаем строку, если это заголовок (содержит th)
                if row.find('th') or 'ДВИЖЕНИЕ ДЕЛА' == row.text.strip():
                    continue

                current_row = {}  # Создаем пустой словарь для текущей строки

                cells = row.find_all('td')  # Находим все ячейки в строке

                # Добавляем данные в словарь
                current_row['name'] = cells[0].text.strip() if len(cells) > 0 else ''
                current_row['date'] = cells[1].text.strip() if len(cells) > 1 else ''
                current_row['time'] = cells[2].text.strip() if len(cells) > 2 else ''
                current_row['result'] = cells[4].text.strip() if len(cells) > 2 else ''
                current_row['the_basic_for_the_selected_result'] = cells[5].text.strip() if len(cells) > 2 else ''
                current_row['date_of_placement'] = cells[7].text.strip() if len(cells) > 2 else ''

            return current_row

        except Exception as exc:
            self.logger.error(f"Ошибка при парсинге таблицы с событиями дела: {exc}")
            self.logger.error(traceback.format_exc(limit=3))
            return None
