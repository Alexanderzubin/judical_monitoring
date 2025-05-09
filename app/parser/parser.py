from datetime import datetime, time

import requests
from bs4 import BeautifulSoup
from requests import RequestException
import logging

from app.parser.exceptions import CasePageResponseError, CasePageParsingError
from app.parser.types import ParsedCaseData, ParsedCaseTableData, ParsedCaseEventData

DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.36 '
)

logger = logging.getLogger(__name__)


class CasePageParser:
    """
    Класс парсера карточки дела на сайте суда.
    """

    def __init__(
        self,
        url: str,
        cookies: dict[str, str] | None = None,
        proxies: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 20,
    ) -> None:
        self.url = url
        self.cookies = cookies
        self.proxies = proxies
        self.headers = headers or {'User-Agent': DEFAULT_USER_AGENT}
        self.timeout = timeout

    def get_case_data(self) -> ParsedCaseData:
        """
        Парсинг карточки дела на сайте суда.
        """
        response = self._get_case_page()

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            case_number = self._get_case_number(soup)
            case_table_data = self._get_case_table_data(soup)

            return ParsedCaseData(number=case_number, **case_table_data)

        except Exception as exc:
            logger.exception('Ошибка парсинга данных', exc_info=exc)
            raise CasePageParsingError()

    def get_case_events(
        self,
    ) -> list[ParsedCaseEventData]:
        """
        Парсинг движения дела на сайте суда.
        """
        response = self._get_case_page()

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._get_case_events_data(soup)

    def _get_case_page(self) -> requests.Response:
        """
        Отправка запроса на получение HTML-страницы карточки дела.
        """
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                cookies=self.cookies,
                proxies=self.proxies,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response
        except RequestException as exc:
            logger.exception('Ошибка при получении страницы', exc_info=exc)
            raise CasePageResponseError()

    def _get_case_number(self, soup: BeautifulSoup) -> str:
        """
        Парсинг номера дела.
        """
        case_number = soup.select_one('div.casenumber')
        case_number_txt = case_number.text
        return str(case_number_txt.split()[2]).strip()

    def _get_case_table_data(self, soup: BeautifulSoup) -> ParsedCaseTableData:
        """
        Парсинг данных вкладки "ДЕЛО".
        """
        try:
            div = soup.find('div', id='cont1')
            table = div.find('table', id='tablcont')

            if not table:
                logger.error('Таблица не найдена на странице')
                raise CasePageParsingError()

            case_details = {
                'Дата поступления': None,
                'Категория дела': None,
                'Номер здания, название обособленного подразделения': None,
                'Признак рассмотрения дела': None,
                'Судья': None,
                'Уникальный идентификатор дела': None,
            }

            # Обход строк таблицы и формирование словаря
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    case_details[key] = value

            date_of_receipt = case_details.get('Дата поступления')
            if date_of_receipt:
                case_details['Дата поступления'] = datetime.strptime(date_of_receipt, '%d.%m.%Y')

            categories = case_details.get('Категория дела')
            if categories:
                case_details['Категория дела'] = map(str.strip, categories.split('→'))

            return ParsedCaseTableData(
                unique_identifier=case_details['Уникальный идентификатор дела'],
                judge=case_details['Судья'],
                date_of_receipt=case_details['Дата поступления'],
                court=case_details['Номер здания, название обособленного подразделения'],
                categories=case_details['Категория дела'] or [],
            )

        except Exception as exc:
            logger.exception('Ошибка при парсинге таблицы с карточкой дела', exc_info=exc)
            raise CasePageParsingError()

    def _get_case_events_data(
        self,
        soup: BeautifulSoup,
    ) -> list[ParsedCaseEventData]:
        """
        Парсинг вкладки 'ДВИЖЕНИЕ ДЕЛА'.
        """
        try:
            div = soup.find('div', id='cont2')
            table = div.find('table', id='tablcont')

            if not table:
                logger.error("Таблица 'Движение дела' не найдена")
                raise CasePageParsingError()

            rows = table.find_all('tr')[2:]  # Пропускаем заголовки

            events: list[ParsedCaseEventData] = []

            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 8:
                    raise CasePageParsingError(
                        'Некорректное количество столбцов во вкладке "ДВИЖЕНИЕ ДЕЛА"'
                    )

                raw_event_date = cells[1].get_text(strip=True)
                raw_hour, raw_minute = cells[2].get_text(strip=True).split(':')
                raw_placement_date = cells[7].get_text(strip=True)

                event = ParsedCaseEventData(
                    event_name=cells[0].get_text(strip=True),
                    date=datetime.strptime(raw_event_date, '%d.%m.%Y').date(),
                    time=time(hour=int(raw_hour), minute=int(raw_minute)),
                    location=cells[3].get_text(strip=True) or None,
                    result=cells[4].get_text(strip=True) or None,
                    reason=cells[5].get_text(strip=True) or None,
                    note=cells[6].get_text(strip=True) or None,
                    placement_date=datetime.strptime(raw_placement_date, '%d.%m.%Y'),
                )
                events.append(event)

            return events

        except Exception as exc:
            logger.exception('Ошибка при парсинге таблицы движения дела', exc_info=exc)
            raise CasePageParsingError()
