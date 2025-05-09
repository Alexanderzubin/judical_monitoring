from typing import Self

from app.database.models import Notification, User, CaseEvent
from app.database.repositories.notification import NotificationRepository
from app.database.session import Session


class NotificationService:
    def __init__(
        self,
        notification_repository: NotificationRepository,
    ):
        self._notification_repository = notification_repository

    @classmethod
    def get_service(cls, session: Session) -> Self:
        return cls(
            notification_repository=NotificationRepository(session),
        )

    def get_or_create_notification(
        self,
        user: User,
        event: CaseEvent,
    ) -> tuple[Notification, bool]:
        return self._notification_repository.get_or_create(user, event)

