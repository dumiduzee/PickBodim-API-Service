from .utils import GenVerifyCode,SendVerificationCode,HashPassword,AccountConfirmOtpSend,decodeHashedPassword,create_jwt_token,decode_token
from .repository import IsExists,InsertRegisterRecord,FindUserByUserIdRespo,VerifyUserUpdate,UpdateOtp,FindUserByEmailRepo
from datetime import timedelta,datetime
from .exceptions import PasswordWrongException,UserNotFoundException,UserAlreadyVerifiedException,InvalidOtpCode,OtpCodeExpiredException,OtpCodeStillValidException,CredentialsException
from decouple import config
from fastapi.security  import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from database.database import db_dependencie
from .configs import CustomOAuth2PasswordBearer

OTP_EXPIRES_IN = config("OTP_EXPIRES_IN")


def RegisterUserService(db,user):
    #Check user email exists or not
    is_Notexsist = IsExists(db,user["Email"])
    if is_Notexsist:
        #Genarate verification code and attach it to user record
        user["verficationCode"] = GenVerifyCode()
        #Hash the password
        user["password"] = HashPassword(user["password"])
        #Genarate expire date and add it to record
        user["verficationCodeExpire"] = datetime.now() + timedelta(minutes=int(OTP_EXPIRES_IN))
        #Insert user into database and get verfication code
        insertedUser = InsertRegisterRecord(db,user=user)
        #Send verification code to user
        if AccountConfirmOtpSend(user["Email"],"Account Verification",insertedUser.verficationCode,insertedUser.firstName):
            return insertedUser
        return None
        

def OtpVerificationService(OTP,USER_ID,DB):
    """Check user exists or not by user id"""
    exists_user = FindUserByUserIdRespo(USER_ID,DB=DB)
    if not exists_user:
        raise UserNotFoundException()
    #check user already verified or not
    if exists_user.isVerfiedUser:
        raise UserAlreadyVerifiedException()
    #check verification code
    if OTP != exists_user.verficationCode:
        raise InvalidOtpCode()
    #Check verification code expire time
    if datetime.now() > exists_user.verficationCodeExpire:
        raise OtpCodeExpiredException()
    #update user as verified
    return VerifyUserUpdate(exists_user,DB)


#Request enw otp code
def RequestNewOtpService(user_id,db):
    #Check user validity
    exists_user = FindUserByUserIdRespo(user_id,db)
    if not exists_user:
        raise UserNotFoundException()
    if exists_user.isVerfiedUser:
        raise UserAlreadyVerifiedException()
    #check otp still valid
    if exists_user.verficationCodeExpire > datetime.now():
        raise OtpCodeStillValidException()
    #Genarate new otp code
    new_otp = GenVerifyCode()
    expire_time = datetime.now() + timedelta(minutes=int(OTP_EXPIRES_IN))
    otp =  UpdateOtp(exists_user,new_otp,expire_time,db)
    if AccountConfirmOtpSend(exists_user.Email,"Account Verification",exists_user.verficationCode,exists_user.firstName):
        return True
    else:
        return False
    
#Use for user signin and genarate token
def SignInService(user_data:OAuth2PasswordRequestForm,db:Session):
    #Check user exists and is he verified
    user = FindUserByEmailRepo(user_data.username,db)
    if not user:
        raise UserNotFoundException(
            detail="User cannot find!",
            solution="please check your email address"
        )
    #Compare passwords
    if not decodeHashedPassword(user_data.password,user.password):
        raise PasswordWrongException()
    # 3genarate jwt token
    access_token_expires = timedelta(minutes=int(config("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token = create_jwt_token(data={"sub":str(user.userId),"role":user.Role},expires_in=access_token_expires)
    return token
    

oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="/api/v1/user/login")
def get_current_user_service(token:Annotated[str,Depends(oauth2_scheme)],db:db_dependencie):
    user_id = decode_token(token=token)
    if not user_id:
        raise CredentialsException()
    #find user from with that id
    user = FindUserByUserIdRespo(user_id,db)
    if user is None:
        raise CredentialsException()
    return user


    

    
    
    

    