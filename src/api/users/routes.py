from fastapi import APIRouter,status
from .schemas import UserRegisterSchema,SuccussResponse
from database.database import db_dependencie
from .services import RegisterUserService
from .exceptions import UserRegisterException
#Define router
router = APIRouter(tags=["User services"])

@router.post("/register",description="Use for register user",status_code=status.HTTP_201_CREATED)
def RegisterUser(user:UserRegisterSchema,db:db_dependencie):
    """Register user from thir provided details"""
    user = RegisterUserService(db,user.model_dump())
    if not user:
        raise UserRegisterException()
    print(":type of id",type(str(user.userId)))
    user_id = user.userId
    return SuccussResponse(
        message="User registration succusfull!!",
        data={"id":user_id}
    )
    