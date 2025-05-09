from sqlalchemy.orm import Session
from app.database.models import User, CaseEvent, Notification
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.database.repositories.exceptions import NotificationError

logger = logging.getLogger(__name__)

class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, user: User, event: CaseEvent) -> Notification | None:
        try:
            return (
                self.session.query(Notification)
                .filter(Notification.user_id == user.id, Notification.event_id == event.id)
                .first()
            )
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error('Database error while getting notification', exc_info=exc)
            raise NotificationError('Ошибка при поиске уведомления')

    def create(self, user: User, event: CaseEvent) -> Notification:
        try:
            new_notification = Notification(user=user, event=event)

            self.session.add(new_notification)
            self.session.commit()
            return new_notification

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error('Database error while creating notification', exc_info=exc)
            raise NotificationError('Ошибка при создании уведомления')

    def get_or_create(self, user: User, event: CaseEvent) -> tuple[Notification, bool]:
        notification = self.get(user, event)
        created = notification is None

        if not notification:
            notification = self.create(user, event)
            created = True

        return notification, created
