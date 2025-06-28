from .utils import GenVerifyCode,SendVerificationCode,HashPassword
from .repository import IsExists,InsertRegisterRecord
from datetime import timedelta,datetime



def RegisterUserService(db,user):
    #Check user email exists or not
    is_Notexsist = IsExists(db,user["Email"])
    if is_Notexsist:
        #Genarate verification code and attach it to user record
        user["verficationCode"] = GenVerifyCode()
        #Hash the password
        user["password"] = HashPassword(user["password"])
        #Genarate expire date and add it to record
        user["verficationCodeExpire"] = datetime.now() + timedelta(minutes=10)
        #Insert user into database and get verfication code
        insertedUser = InsertRegisterRecord(db,user=user)
        #Send verification code to user
        if SendVerificationCode(verification_code=insertedUser.verficationCode,CLIENT_NUMBER=insertedUser.phoneNumber,CLIENT_NAME=insertedUser.firstName):
            return insertedUser
        else:
            return False
        

    