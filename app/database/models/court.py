from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import relationship

from app.database.base import Base


class Court(Base):
	__tablename__ = 'court'

	id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификтор судов')
	name = Column(String(255), unique=True, nullable=False, comment='Наименования суда')

	cases = relationship('Case', back_populates='court')
