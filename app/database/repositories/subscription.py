from sqlalchemy.orm import Session
from app.database.models.subscription import Subscription
from typing import Callable, TypeAlias, List
from sqlalchemy.exc import SQLAlchemyError
import logging

SessionFactory: TypeAlias = Callable[[], Session]

class SubscriptionRepository:

    def __init__(self, session: SessionFactory, logger: logging.Logger):
       self.session = session()
       self.logger = logger

    def __del__(self):
        self.session.close()

    def create(
            self,
            user_id: int,
            case_id: int
    ) -> Subscription | None:
        
        try:
            subscription = Subscription(user_id=user_id, case_id=case_id)
            self.session.add(subscription)
            self.session.commit()
            return subscription
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating subscription: {exc}')
    
    def get_by_id(
            self,
            subscription_id: int
        ) -> Subscription | None:
        
        try:
            return self.session.query(Subscription).filter(Subscription.id == subscription_id).first()
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get by id subscription: {exc}')
    
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
    
    def get_user_subscriptions(
            self,
            user_id: int
    ) -> List[Subscription] | None:
        
        try:
            return self.session.query(Subscription)\
                .filter(Subscription.user_id == user_id)\
                .all()
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get user subscriptions: {exc}')
    
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
