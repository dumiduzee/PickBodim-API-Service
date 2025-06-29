from fastapi import APIRouter,status
from .schemas import UserRegisterSchema,SuccussResponse
from database.database import db_dependencie
from .services import RegisterUserService,OtpVerificationService,RequestNewOtpService
from .exceptions import UserRegisterException,OtpResolutionFailException


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
    print(RequestNewOtpService(user_id,db))