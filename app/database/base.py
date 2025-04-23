from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    def as_dict(self) -> dict:
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }
