from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from typing import Annotated
from fastapi import Depends
from decouple import config

DB_USER = config("DB_USERNAME") 
DB_PASS = config("DB_PASSWORD")
DB_NAME = config("DB_NAME")
DB_PORT = config("DB_PORT")

DATABASE_URL=f"postgresql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependencie = Annotated[Session,Depends(get_db)]