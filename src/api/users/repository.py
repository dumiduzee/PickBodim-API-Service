from sqlalchemy.orm import Session
from .models import UserModel
from .exceptions import UserAlreadyExistsException,InternalServerException
import uuid


#Check user exsistance function
def IsExists(db:Session,email):
    try:
        user = db.query(UserModel).filter(UserModel.Email == email).first()
        if user:
            raise UserAlreadyExistsException()
        return True
    except UserAlreadyExistsException as e:
        raise e
    except Exception as e:
         print(e)
         raise InternalServerException()
    
def InsertRegisterRecord(db:Session,user):
    try:
        user_record = UserModel(**user)
        db.add(user_record)
        commit = db.commit()
        db.refresh(user_record)
        return user_record
    except Exception as e:
        db.rollback()
        print(e)
        raise InternalServerException()

#Find useer by thir user id 
def FindUserByUserIdRespo(USERID,DB:Session):
    user = DB.query(UserModel).filter(UserModel.userId == uuid.UUID(USERID)).first()
    if user:
        return user
    return None

#Update user veriied state to VERFIED
def VerifyUserUpdate(USER,DB:Session):
    user = DB.query(UserModel).filter(UserModel.userId == USER.userId).update({"isVerfiedUser":True},synchronize_session=False)
    DB.commit()
    if user:
        return True
    else:
        return False
    

#for request request new otp
def UpdateOtp(user,otp,expire,db:Session):
    print(user.userId)
    user = db.query(UserModel).filter(UserModel.userId == user.userId).update({"verficationCode":otp,"verficationCodeExpire":expire})
    db.commit()
    return otp