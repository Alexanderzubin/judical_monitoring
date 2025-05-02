from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    str_columns: tuple[str] = ('id',)

    def as_dict(self) -> dict:
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }

    def __repr__(self):
        columns = []
        for col in self.__table__.columns.keys():
            if col in self.str_columns:
                columns.append(f'{col}={getattr(self, col)}')
        
        return f"<{self.__class__.__name__} {', '.join(columns)}>"
    