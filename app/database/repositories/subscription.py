from sqlalchemy.orm import Session
from app.database.models.subscription import Subscription
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import SubscriptionError

class SubscriptionRepository:

    def __init__(self, session: Session, logger: logging.Logger):
       self.session = session
       self.logger = logger

    def create(
            self,
            user_id: int,
            case_id: int
    ) -> Subscription:
        
        try:
            subscription = Subscription(user_id=user_id, case_id=case_id)
            self.session.add(subscription)
            self.session.commit()
            return subscription
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating subscription: {exc}')
            raise SubscriptionError('Ошибка при создании подписки')
    
    def get_by_id(
            self,
            subscription_id: int
        ) -> Subscription | None:
        
        try:
            return self.session.query(Subscription).filter(Subscription.id == subscription_id).first()
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get by id subscription: {exc}')
            raise SubscriptionError('Ошибка получения подписки по id')
    
    def get_by_user_and_case(
            self,
            user_id: int,
            case_id: int
    ) -> Subscription:
        
        try:
            return (
                self.session.query(Subscription)
                .filter(Subscription.user_id == user_id, Subscription.case_id == case_id)
                .first()
            )
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get by user and case subscription: {exc}')
            raise SubscriptionError('Ошибка получения подписки по id пользователя и дела')
    
    def get_user_subscriptions(
            self,
            user_id: int
    ) -> list[Subscription | None]:
        
        try:
            return self.session.query(Subscription)\
                .filter(Subscription.user_id == user_id)\
                .all()
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get user subscriptions: {exc}')
            raise SubscriptionError('Ошибка получения подписок пользователя')
    
    def count_user_subscriptions(
            self,
            user_id: int
    ) -> int:
        try:
            return self.session.query(Subscription)\
                .filter(Subscription.user_id == user_id)\
                .count()
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while count user subscription: {exc}')
            raise SubscriptionError('Ошибка при получении количества подписок пользователя')


    def delete(
            self,
            subscription_id: int
    ) -> None:
        try:
            subscription = self.session.query(Subscription).filter(Subscription.id == subscription_id).first()
            if subscription:
                self.session.delete(subscription)
                self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while deleting subscription: {exc}')
            raise SubscriptionError('Ошибка при удалении подписки')
