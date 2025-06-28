from pydantic import BaseModel,Field,field_validator
from fastapi import status
from .exceptions import InvalidEmailException,InvalidNumberException
from typing import Any

class SuccussResponse(BaseModel):
    status:str=Field(default="succuss")
    message:str
    data:Any




class UserRegisterSchema(BaseModel):
    firstName:str=Field(min_length=3)
    lastName:str=Field(min_length=3)
    Address:str=Field(min_length=3)
    phoneNumber:str=Field(min_length=3,max_length=10)
    Email:str=Field(min_length=3)
    password:str=Field(min_length=3)
    Role:str=Field(default="HOSTER")

    @field_validator("Email",mode="after")
    def EmailValidator(value:str,cls):
        """Use for validate email address"""
        if value.endswith(".com"):
            return value
        raise InvalidEmailException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong email address",
            solution="Check your email address again.It must be a valid email address"
            )
    @field_validator("phoneNumber",mode="after")
    def PhoneNumberValidator(value:str,cls):
        if value.startswith("07"):
            return value
        raise InvalidNumberException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number format",
            solution="Please check your phone number it must be starts with 07 and it must have 10 digits"
        )
    