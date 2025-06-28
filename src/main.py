from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database.database import Base,engine
from api.users.routes import router as UserRouter
from api.hostel.routes import router as HostelRouter
from database.database import Base
from api.users.models import UserModel
from api.users.exceptions import UserExceptions




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


#custom exception handler
@app.exception_handler(UserExceptions)
async def exception_handler(request,exe:UserExceptions):
    return JSONResponse(
        status_code=exe.status_code,
        content={
            "error_code":exe.status_code,
            "message":exe.detail,
            "solution":exe.solution
        }
    )



Base.metadata.create_all(bind=engine)


