from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey

from app.database.base import Base


class CaseEvent(Base):
    __tablename__ = 'case_event'
    
    id = Column(Integer, autoincrement=True, primary_key=True, comment='идентификтор события')
    name = Column(String(255), comment='наименование события')
    date = Column(Date, comment='дата события')
    time = Column(Time, comment='время события')
    result = Column(String(255), comment='результат события')
    the_basic_for_the_selected_result = Column(String(255), comment='Основание для выбранного результата события')
    date_of_placement = Column(Date, comment='дата размещения события')
    case_id = Column(Integer, ForeignKey('case.id', ondelete='CASCADE'), nullable=False, comment='идентификтор карточки дела')