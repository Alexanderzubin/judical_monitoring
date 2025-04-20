from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship

from app.database.base import Base


class Court(Base):
	"""Модель суда"""
	__tablename__ = 'court'

	id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификатор судов')
	name = Column(String(255), unique=True, nullable=False, comment='Наименование суда')

	# relationship
	cases = relationship('Case', back_populates='court')
