from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Judge(Base):
    __tablename__ = 'judge'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификтор судьи')
    name = Column(String(255), unique=True, nullable=False, comment='ФИО судьи')
