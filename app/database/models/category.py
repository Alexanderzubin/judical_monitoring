from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификтор категории дела')
    name = Column(String(1024), unique=True, comment='наименование категории дела')
    


    
