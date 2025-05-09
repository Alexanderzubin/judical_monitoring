import logging
from typing import Dict
from app.database.repositories.user import UserRepository
from app.database.repositories.case import CaseRepository
from app.database.repositories.case_event import CaseEventRepository
from app.database.repositories.subscription import SubscriptionRepository
from app.database.repositories.notification import NotificationRepository
from app.database.session import Session
from app.parser.parser import CasePageParser

logger = logging.getLogger(__name__)


def create_notification_for_event(session: Session, user_id: int, event_id: int) -> Dict:
    try:
        user_repo = UserRepository(session)
        event_repo = CaseEventRepository(session)
        notif_repo = NotificationRepository(session)

        user = user_repo.get_by_tg_id(user_id)
        if not user:
            raise ValueError('Пользователь не найден')

        event = event_repo.get_by_id(event_id)
        if not event:
            raise ValueError('Событие не найдено')

        notification = notif_repo.create(user=user, event=event)

        return {
            'status': 'success',
            'notification_id': notification.id,
            'event_id': event_id,
            'user_id': user_id,
        }

    except Exception as exc:
        logger.error(f'Ошибка при создании уведомления: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при создании уведомления: {str(exc)}',
            'user_id': user_id,
            'event_id': event_id,
        }
