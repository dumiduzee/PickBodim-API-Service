from sqlalchemy.orm import Session
from .models import UserModel
from .exceptions import UserAlreadyExistsException,InternalServerException


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
        print(e)
        raise InternalServerException()