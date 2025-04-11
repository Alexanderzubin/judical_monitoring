from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base


class Case(Base):
    __tablename__ = 'case'
    

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификтор карточки дела')
    number = Column(String(255), comment='номер дела')
    unique_identifier = Column(String(255), unique=True, nullable=False, comment='уникальный идентификатор дела')
    judge_id = Column(Integer, ForeignKey('judge.id', ondelete='RESTRICT'), nullable=False, index=True, comment='идентификатор судьи')
    name_of_the_court = Column(String(255), comment='наименование суда')
    date_of_receipt = Column(String(255), comment='дата размещения')


    
