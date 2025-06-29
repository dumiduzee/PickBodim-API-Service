from fastapi import APIRouter,status,Depends
from .schemas import UserRegisterSchema,SuccussResponse,Token,User
from database.database import db_dependencie
from .services import RegisterUserService,OtpVerificationService,RequestNewOtpService,SignInService,get_current_user_service
from .exceptions import UserRegisterException,OtpResolutionFailException,InternalServerException,SignInFailedException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


#Define router
router = APIRouter(tags=["User services"])

#Register new user
@router.post("/register",description="Use for register user",status_code=status.HTTP_201_CREATED)
def RegisterUser(user:UserRegisterSchema,db:db_dependencie):
    """Register user from thir provided details"""
    user = RegisterUserService(db,user.model_dump())
    if not user:
        raise UserRegisterException()
    user_id = user.userId

    return SuccussResponse(
        message="User registration succusfull!!",
        data={"id":user_id}
    )

#New user verify otp
@router.post("/confirm-otp/{user_id}",description="Use for confirm the phone number",status_code=status.HTTP_200_OK)
def ConfirmOtp(otp:str,user_id:str,db:db_dependencie):
   """Use confirm the password otp"""
   if len(user_id) < 3 or len(otp) < 3:
       raise OtpResolutionFailException()
   if OtpVerificationService(otp,user_id,db):
       return SuccussResponse(
           message="User account verified!!",
           data={}
       )


#Request new otp
@router.get("/reqest-otp/{user_id}",description="Use for request new otp",status_code=status.HTTP_200_OK)
def RequestNewOtp(user_id:str,db:db_dependencie):
    if RequestNewOtpService(user_id,db):
        return SuccussResponse(
            message="New otp sent!",
            data={}
        )
    raise InternalServerException()


#Sign in useer
@router.post("/login",description="Login handle",response_model=Token)
def UserLogin(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependencie):
    token =SignInService(form_data,db)
    if not token:
        raise SignInFailedException()
    return Token(
        access_token=token,
        token_type="bearer"
    )


@router.get("/me")
def userget(current_user:Annotated[User,Depends(get_current_user_service)]):
    print(current_user)