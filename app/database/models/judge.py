from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Judge(Base):
    """Модель судьи"""
    __tablename__ = 'judge'
    str_columns = ('name',)
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификатор судьи')
    name = Column(String(255), unique=True, nullable=False, comment='ФИО судьи')

    # relationship
    cases = relationship('Case', back_populates='judge')