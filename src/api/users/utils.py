import uuid
from decouple import config
import requests
from passlib.hash import pbkdf2_sha256
import json
from .exceptions import UserRegisterException
from datetime import datetime, timedelta, timezone
import jwt
from .exceptions import CredentialsException
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError

def GenVerifyCode():
    """Genarate verification code for the user"""
    code = str(uuid.uuid4())
    return code.split("-")[0]


def HashPassword(PLAIN_PASSWORD):
    """Use for hash the password"""
    return pbkdf2_sha256.hash(PLAIN_PASSWORD)

def decodeHashedPassword(PLAIN_PASSWORD,HASH_PASSWORD)->bool:
    """_summary_

    Args:
        PLAIN_PASSWORD (_type_): _description_
        HASH_PASSWORD (_type_): _description_

    Returns:
        bool: _description_
    """
    return pbkdf2_sha256.verify(PLAIN_PASSWORD,HASH_PASSWORD)


#Create jwt token for user and thir role
def create_jwt_token(data:dict,expires_in:timedelta | None = None):
    TOKEN = config("ACCESS_TOKEN_SECRET")
    to_encode = data.copy()
    if expires_in:
        expires = datetime.now(timezone.utc) + expires_in
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp":expires})
    encode_jwt = jwt.encode(to_encode,TOKEN,config("ALGORITHM"))
    return encode_jwt

#Decode jwt token
def decode_token(token):
    try:
        payload = jwt.decode(token,config("ACCESS_TOKEN_SECRET"),algorithms=config("ALGORITHM"))
        user_id = payload.get("sub")
        if user_id is None:
            raise CredentialsException()
        return user_id
    except ExpiredSignatureError:
        raise CredentialsException()
    except InvalidTokenError:
        raise CredentialsException()
    
    




def SendVerificationCode(verification_code,CLIENT_NUMBER,CLIENT_NAME):
    """Send verification code through phone number"""
    try:
        res = requests.post(
            "https://app.text.lk/api/v3/sms/send",
            headers={
                'Authorization': f'Bearer {config("TEXT_LK_API_KEY")}',
            },
            params={
                "recipient":"94"+ CLIENT_NUMBER[0:],
                "sender_id":config("TEXT_LK_SENDER_ID"),
                "type":"plain",
                "message":f"Hello {CLIENT_NAME}, Your PickBodim verification code is {verification_code}. Please enter it within the next 5 minutes to continue.",
            }
        )
        result = res.json()
        if result["status"] == "success":
            return True
        print(result)
        return False
    
    except Exception as e:
        print(e)
        raise UserRegisterException()
    
#Send emails

def AccountConfirmOtpSend(to_email: str, subject: str, otp_code: str,CLIENT_NAME):
    url = "https://api.brevo.com/v3/smtp/email"
    payload = json.dumps(
        {
            "sender": {"name": "PickBodim", "email": config("SENDER_EMAIL_BRAVO")},
            "to": [{"email": f"{to_email}"}],
            "subject": subject,
            "textContent": f"Hello {CLIENT_NAME}, Your PickBodim verification code is {otp_code}. Please enter it within the next 5 minutes to continue.",
            
        }
    )
    headers = {
        "accept": "application/json",
        "api-key": config("BRAVO_API_KEY"),
        "content-type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    if res["messageId"]:
        return True
    else:
        return False
