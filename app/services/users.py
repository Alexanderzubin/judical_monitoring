from typing import Self

from app.database.models import User
from app.database.repositories.user import UserRepository
from app.database.session import Session
from app.services.exceptions import UserNotFoundError


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self._user_repository = user_repository

    @classmethod
    def get_service(cls, session: Session) -> Self:
        return cls(
            user_repository=UserRepository(session),
        )

    def create_user(
        self, tg_id: int, first_name: str, last_name: str, username: str, chat_id: int
    ) -> User:
        return self._user_repository.create(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            chat_id=chat_id,
        )

    def get_user_by_telegram_id(self, tg_id) -> User | None:
        return self._user_repository.get_by_tg_id(tg_id)

    def find_user_by_telegram_id(self, tg_id) -> User:
        user = self._user_repository.get_by_tg_id(tg_id)
        if not user:
            raise UserNotFoundError()

        return user
