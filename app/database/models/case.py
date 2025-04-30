from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.database.base import Base
from sqlalchemy.orm import relationship


class Case(Base):
    """Модель судебного дела"""
    __tablename__ = 'case'
    str_columns = ('number', 'court_id')

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, unique=True, comment='идентификтор карточки дела')
    number = Column(String(255), nullable=False, comment='номер дела')
    unique_identifier = Column(String(255), unique=True, nullable=False, comment='уникальный идентификатор дела')
    judge_id = Column(Integer, ForeignKey('judge.id', ondelete='RESTRICT'), nullable=False, index=True, comment='идентификатор судьи')
    date_of_receipt = Column(Date, nullable=False, comment='дата размещения')
    url = Column(String, unique=True, nullable=False, index=True, comment='URL дела')
    court_id = Column(Integer, ForeignKey('court.id', ondelete='RESTRICT', ), nullable=False, index=True,
					  comment='идентификатор суда')

	# relationship
    judge = relationship('Judge', back_populates='cases')
    categories = relationship(
		'Category',
		secondary='case_category',
		back_populates='cases'
	)
    court = relationship('Court', back_populates='cases')
    events = relationship('CaseEvent', back_populates='case')


