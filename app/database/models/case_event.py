from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class CaseEvent(Base):
    """Модель события"""

    __tablename__ = 'case_event'

    id = Column(Integer, autoincrement=True, primary_key=True, comment='идентификатор события')
    name = Column(String(255), nullable=False, comment='наименование события')
    date = Column(Date, nullable=False, comment='дата события')
    time = Column(Time, nullable=False, comment='время события')
    result = Column(String(255), comment='результат события')
    the_basic_for_the_selected_result = Column(
        String(255), comment='Основание для выбранного результата события'
    )
    date_of_placement = Column(Date, nullable=False, comment='дата размещения события')
    case_id = Column(
        Integer,
        ForeignKey('case.id', ondelete='CASCADE'),
        nullable=False,
        comment='идентификатор карточки дела',
    )

    # relationship
    case = relationship('Case', back_populates='events')
    notifications = relationship('Notification', back_populates='event')
    users = relationship('User', secondary='notification', back_populates='events', viewonly=True)

    @property
    def occurred_at(self) -> datetime:
        return datetime.combine(self.date, self.time)

    @property
    def days_since_event(self) -> int:
        return (datetime.now() - self.occurred_at).days

