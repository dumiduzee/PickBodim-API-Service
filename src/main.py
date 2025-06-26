from fastapi import FastAPI
from .database.database import Base,engine

app = FastAPI(
    title="PickBodim-API-Service",
    description="Core api for managing hostels services arround universities",
    version="1.0",
    contact={
        "name":"ZeusDev",
        "url":"https://google.com",
        "email":"xxxxxxx@gmail.com"
    }
)


Base.metadata.create_all(bind=engine)


