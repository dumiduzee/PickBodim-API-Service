from sqlalchemy import Column,String,Integer,Text,Boolean,DateTime
from datetime import date
from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserModel(Base):
    __tablename__ = "users"
    userId=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,unique=True,index=True)
    firstName = Column(String)
    lastName = Column(String)
    Address = Column(Text)
    phoneNumber = Column(String)
    Email = Column(String,unique=True)
    password = Column(String)
    isVerfiedUser = Column(Boolean,default=False,nullable=False)
    Role=Column(String,default="HOSTER",nullable=False)
    verficationCode=Column(String,default=None)
    verficationCodeExpire=Column(DateTime,default=None)
    def __repr__(self):
        return f"UserModel(userId={self.userId}, firstName={self.firstName}, lastName={self.lastName}, Email={self.Email})"
