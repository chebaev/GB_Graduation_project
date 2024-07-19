from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.settings.settings import settings
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

engine = create_engine(
    url=settings.DATABASE_URL_MYSQL_asyncmy,
    echo=False
)


session_factory = sessionmaker(engine)