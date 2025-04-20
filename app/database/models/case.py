from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.database.models.court import Court


class Case(Base):
	"""Модель судебного дела"""
	__tablename__ = 'case'

	id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификатор карточки дела')
	number = Column(String(255), nullable=False, comment='номер дела')
	unique_identifier = Column(String(255), unique=True, nullable=False, comment='уникальный идентификатор дела')
	judge_id = Column(Integer, ForeignKey('judge.id', ondelete='RESTRICT'), nullable=False, index=True,
					  comment='идентификатор судьи')
	court_id = Column(Integer, ForeignKey('court.id', ondelete='RESTRICT', ), nullable=False, index=True,
					  comment='идентификатор суда')
	date_of_receipt = Column(Date, comment='дата размещения')

	# relationship
	judge = relationship('Judge', back_populates='cases')
	case_categories = relationship('CaseCategory', back_populates='case')
	categories = relationship(
		'Category',
		secondary='case_category',
		back_populates='cases'
	)
	court = relationship('Court', back_populates='cases')
	events = relationship('CaseEvent', back_populates='case')
