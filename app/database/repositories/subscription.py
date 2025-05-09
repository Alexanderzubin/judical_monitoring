from sqlalchemy.orm import Session

from app.database.models import User, Case
from app.database.models.subscription import Subscription
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import SubscriptionError


logger = logging.getLogger(__name__)


class SubscriptionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, case_id: int) -> Subscription:
        try:
            subscription = Subscription(user_id=user_id, case_id=case_id)
            self.session.add(subscription)
            self.session.commit()
            return subscription

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while creating subscription: {exc}')
            raise SubscriptionError('Ошибка при создании подписки')

    def get_by_id(self, subscription_id: int) -> Subscription | None:
        try:
            return (
                self.session.query(Subscription).filter(Subscription.id == subscription_id).first()
            )
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get by id subscription: {exc}')
            raise SubscriptionError('Ошибка получения подписки по id')

    def get_by_user_and_case(self, user_id: int, case_id: int) -> Subscription:
        try:
            return (
                self.session.query(Subscription)
                .filter(Subscription.user_id == user_id, Subscription.case_id == case_id)
                .first()
            )

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get by user and case subscription: {exc}')
            raise SubscriptionError('Ошибка получения подписки по id пользователя и дела')

    def get_user_subscriptions_count(self, user_id: int) -> int:
        try:
            query = self.session.query(Subscription).filter(Subscription.user_id == user_id)

            return query.count()

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get user subscriptions count: {exc}')
            raise SubscriptionError('Ошибка получения количества подписок пользователя')

    def get_user_subscriptions(
        self,
        user_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Subscription]:
        try:
            query = self.session.query(Subscription).filter(Subscription.user_id == user_id)

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(limit * offset)

            return query.all()

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get user subscriptions: {exc}')
            raise SubscriptionError('Ошибка получения подписок пользователя')

    def count_user_subscriptions(self, user_id: int) -> int:
        try:
            return self.session.query(Subscription).filter(Subscription.user_id == user_id).count()

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while count user subscription: {exc}')
            raise SubscriptionError('Ошибка при получении количества подписок пользователя')

    def delete(self, subscription_id: int) -> None:
        try:
            subscription = (
                self.session.query(Subscription).filter(Subscription.id == subscription_id).first()
            )
            if subscription:
                self.session.delete(subscription)
                self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while deleting subscription: {exc}')
            raise SubscriptionError('Ошибка при удалении подписки')

    def delete_user_case_subscription(self, user_id: int, case_id: int) -> None:
        try:
            (
                self.session.query(Subscription)
                .filter(Subscription.user_id == user_id, Subscription.case_id == case_id)
                .delete()
            )
            self.session.commit()
        except SQLAlchemyError as exc:
            logger.error(f'Database error while creating subscription: {exc}')
            raise SubscriptionError('Ошибка при удалении подписки')

    def get_case_subscribers(self, case: Case) -> list[User]:
        try:
            stmt = (
                self.session.query(User).join(Subscription).where(Subscription.case_id == case.id)
            )
            return self.session.execute(stmt).scalars().all()

        except SQLAlchemyError as exc:
            logger.error('Database error while getting case subscribers', exc_info=exc)
            raise SubscriptionError('Ошибка при получении подписок по делу')
