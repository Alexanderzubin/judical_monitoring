from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Notification(Base):
	"""Модель уведомлений"""
	__tablename__ = 'notification'
    
	__table_args__ = (UniqueConstraint('user_id', 'event_id', name='uq_user_event'),)
	id = Column(Integer, autoincrement=True, primary_key=True, comment='идентификтор уведомления')
	user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, comment='идентификтор пользователя')
	event_id = Column(Integer, ForeignKey('case_event.id', ondelete='CASCADE'), nullable=False, comment='идентификтор события')
	sent_at = Column(DateTime, server_default=func.now(), comment='дата отправки уведомления пользователю')

	# relationship
	user = relationship('User', back_populates='notifications')
	event = relationship('CaseEvent', back_populates='notifications')