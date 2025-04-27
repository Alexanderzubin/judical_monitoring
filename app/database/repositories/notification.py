from sqlalchemy.orm import Session
from app.database.models import User, CaseEvent, Notification
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.database.repositories.exceptions import NotificationError

class NotificationRepository():

    def __init__(self, session: Session, logger: logging.Logger):
        self.session = session
        self.logger = logger

    def create(self, user: User, event: CaseEvent
        ) -> Notification:
        
        try:
            new_notification = Notification(
                user=user,
                event=event
            )

            self.session.add(new_notification)
            self.session.commit()
            return new_notification
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating notification: {exc}')
            raise NotificationError('Ошибка при создании уведомления')
