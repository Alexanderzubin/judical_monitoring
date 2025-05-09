class UserServiceError(Exception):
    """Базовый класс для исключений сервиса пользователей."""


class UserNotFoundError(UserServiceError):
    """Пользователь не найден."""

    def __init__(self):
        super().__init__('Пользователь не найден')


class CaseServiceError(Exception):
    """Базовый класс для исключений сервиса дел."""


class CaseNotFoundError(CaseServiceError):
    """Дело не найдено."""

    def __init__(self):
        super().__init__('Дело не найдено')


class CasePageParsingError(CaseServiceError):
    """Ошибка парсинга карточки дела."""

    def __init__(self):
        super().__init__('Ошибка парсинга карточки дела')


class SubscriptionServiceError(Exception):
    """Базовый класс для исключений сервиса подписок."""


class SubscriptionNotFoundError(SubscriptionServiceError):
    """Подписка не найдена."""

    def __init__(self):
        super().__init__('Подписка не найдена')


class CaseEventServiceError(Exception):
    """Базовый класс для исключений сервиса событий по делам."""


class CaseEventNotFoundError(CaseServiceError):
    """Событие по делу не найдено."""

    def __init__(self):
        super().__init__('Событие по делу не найдено')
