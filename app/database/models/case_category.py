from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


from app.database.base import Base


class CaseCategory(Base):
    """Промежуточная модель для связи многие ко многим между Case и Category"""
    __tablename__ = 'case_category'
    __table_args__= (
        UniqueConstraint('category_id','case_id', name='uq_casecategory_case_category'),
    )
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='суррогатный ключ')
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'), nullable=False, comment='категория дела')
    case_id = Column(Integer, ForeignKey('case.id', ondelete='CASCADE'), nullable=False, comment='идентификтор карточки дела')

