from .utils import GenVerifyCode,SendVerificationCode,HashPassword
from .repository import IsExists,InsertRegisterRecord,FindUserByUserIdRespo,VerifyUserUpdate,UpdateOtp
from datetime import timedelta,datetime
from .exceptions import UserNotFoundException,UserAlreadyVerifiedException,InvalidOtpCode,OtpCodeExpiredException,OtpCodeStillValidException
from decouple import config

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
        if SendVerificationCode(verification_code=insertedUser.verficationCode,CLIENT_NUMBER=insertedUser.phoneNumber,CLIENT_NAME=insertedUser.firstName):
            return insertedUser
        else:
            return False
        

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
    if SendVerificationCode(otp,exists_user.phoneNumber,exists_user.firstName):
        return True
    else:
        return False

    
    
    

    