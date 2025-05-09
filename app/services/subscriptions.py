import logging
from typing import Self

from app.database.models import User, Case, Subscription
from app.database.repositories.subscription import SubscriptionRepository
from app.database.session import Session
from app.services.exceptions import SubscriptionNotFoundError

logger = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
    ):
        self._subscription_repository = subscription_repository

    @classmethod
    def get_service(cls, session: Session) -> Self:
        return cls(
            subscription_repository=SubscriptionRepository(session),
        )

    def get_user_subscriptions(
        self,
        user: User,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Subscription]:
        return self._subscription_repository.get_user_subscriptions(
            user_id=user.id,
            limit=limit,
            offset=offset,
        )

    def get_user_subscriptions_count(self, user: User) -> int:
        return self._subscription_repository.get_user_subscriptions_count(user.id)

    def find_subscription_by_id(self, subscription_id: int) -> Subscription:
        subscription = self._subscription_repository.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError()

        return subscription

    def is_user_subscribed_to_case(
        self,
        user: User,
        case: Case,
    ) -> bool:
        subscription = self._subscription_repository.get_by_user_and_case(
            user_id=user.id,
            case_id=case.id,
        )

        if subscription:
            return True

        return False

    def subscribe_user(
        self,
        user: User,
        case: Case,
    ) -> Subscription:
        return self._subscription_repository.create(user.id, case.id)

    def unsubscribe_user(
        self,
        user: User,
        case: Case,
    ) -> None:
        self._subscription_repository.delete_user_case_subscription(
            user_id=user.id,
            case_id=case.id,
        )

        logger.info(f'User {user.id} unsubscribed from case {case.id}')

    def get_case_subscribers(self, case: Case) -> list[User]:
        return self._subscription_repository.get_case_subscribers(case=case)
