import atexit
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "qwerty123")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app_ad")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app_ad")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5431')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Ad(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    creation_datetime = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creation_datetime': self.creation_datetime.isoformat(),
            'owner': self.owner,
        }


Base.metadata.create_all(bind=engine)
