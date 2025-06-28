from .utils import GenVerifyCode,SendVerificationCode,HashPassword
from .repository import IsExists,InsertRegisterRecord,FindUserByUserIdRespo,VerifyUserUpdate
from datetime import timedelta,datetime
from .exceptions import UserNotFoundException,UserAlreadyVerifiedException,InvalidOtpCode,OtpCodeExpiredException



def RegisterUserService(db,user):
    #Check user email exists or not
    is_Notexsist = IsExists(db,user["Email"])
    if is_Notexsist:
        #Genarate verification code and attach it to user record
        user["verficationCode"] = GenVerifyCode()
        #Hash the password
        user["password"] = HashPassword(user["password"])
        #Genarate expire date and add it to record
        user["verficationCodeExpire"] = datetime.now() + timedelta(minutes=30)
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
    
    

    