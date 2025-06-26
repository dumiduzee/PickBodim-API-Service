from fastapi import FastAPI
from database.database import Base,engine
from api.users.routes import router as UserRouter
from api.hostel.routes import router as HostelRouter
from database.database import Base
from api.users.models import UserModel


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

#Use routes
app.include_router(prefix="/api/v1/user",router=UserRouter)
app.include_router(prefix="/api/v1/hostel",router=HostelRouter)



Base.metadata.create_all(bind=engine)


