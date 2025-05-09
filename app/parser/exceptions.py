class CasePageParserError(Exception):
    """Базовый класс ошибки парсинга данных карточки дела."""


class CasePageResponseError(CasePageParserError):
    """Ошибка при отправке запроса на сайт суда."""


class CasePageParsingError(CasePageParserError):
    """Ошибка при парсинге данных карточки дела."""
