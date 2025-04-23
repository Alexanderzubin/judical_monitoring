from sqlalchemy.orm import Session
from app.database.models.notification import Notification
from typing import Callable, TypeAlias
import logging
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


SessionFactory: TypeAlias = Callable[[], Session]


class NotificationRepository():

    def __init__(self, session: SessionFactory, logger: logging.Logger):
        self.session = session()
        self.logger = logger

    def __del__(self):
        self.session.close()

    def create(self, user_id: int, event_id: int,
        sent_at: datetime) -> Notification | None:
        
        try:
            new_notification = Notification(
                user_id=user_id,
                event_id=event_id,
                sent_at=sent_at
            )

            self.session.add(new_notification)
            self.session.commit()
            return new_notification
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating notification: {exc}')
