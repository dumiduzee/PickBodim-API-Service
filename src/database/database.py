from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from typing import Annotated
from fastapi import Depends

DATABASE_URL=f"postgresql://username:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependencie = Annotated[Session,Depends(get_db)]