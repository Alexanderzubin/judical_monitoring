from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.database.base import Base
from app.database.models.court import Court
from sqlalchemy.orm import relationship


class Case(Base):
    """Модель судебного дела"""
    __tablename__ = 'case'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификтор карточки дела')
    number = Column(String(255), comment='номер дела')
    unique_identifier = Column(String(255), unique=True, nullable=False, comment='уникальный идентификатор дела')
    judge_id = Column(Integer, ForeignKey('judge.id', ondelete='RESTRICT'), nullable=False, index=True, comment='идентификатор судьи')
    name_of_the_court = Column(String(255), comment='наименование суда')
    date_of_receipt = Column(Date, comment='дата размещения')
    url = Column(String, unique=True, nullable=False, comment='URL дела')
    court_id = Column(Integer, ForeignKey('court.id', ondelete='RESTRICT', ), nullable=False, index=True,
					  comment='идентификатор суда')


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
