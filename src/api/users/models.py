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
    Email = Column(String)
    password = Column(String)
    isVerfiedUser = Column(Boolean,default=False)
    Role=Column(String,default="HOSTER",nullable=False)
    verficationCode=Column(String,default=None)
    verficationCodeExpire=Column(DateTime,default=None)

