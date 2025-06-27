from fastapi import APIRouter
from .schemas import UserRegisterSchema
from database.database import db_dependencie
#Define router
router = APIRouter(tags=["User services"])

@router.post("/register",description="Use for register user")
def RegisterUser(user:UserRegisterSchema,db:db_dependencie):
    """Register user from thir provided details"""
    print(user,db)