from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(settings.db.url)
SessionLocal = sessionmaker(bind=engine)