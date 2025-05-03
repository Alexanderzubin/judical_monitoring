from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base


class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__= (
        UniqueConstraint('user_id','case_id', name='uq_subscription_user_case'),
    )
    
    id = Column(Integer, autoincrement=True, primary_key=True, comment='идентификтор подписки')
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, comment='идентификтор пользователя')
    case_id = Column(Integer, ForeignKey('case.id', ondelete='CASCADE'), nullable=False, comment='идентификтор карточки дела')

    cases = relationship('Case', back_populates='subscription')
