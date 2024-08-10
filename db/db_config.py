import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, DeclarativeMeta

load_dotenv()

DB_LOGIN = os.getenv("DATABASE_LOGIN")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_URL = f"postgresql+psycopg2://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_ENGINE = create_engine(DB_URL)

Base: DeclarativeMeta = declarative_base()


def create_session():
    return sessionmaker(bind=DB_ENGINE, expire_on_commit=False)()
