import uuid
from decouple import config
import requests
from passlib.hash import pbkdf2_sha256
from .exceptions import UserRegisterException

def GenVerifyCode():
    """Genarate verification code for the user"""
    code = str(uuid.uuid4())
    return code.split("-")[0]


def HashPassword(PLAIN_PASSWORD):
    """Use for hash the password"""
    return pbkdf2_sha256.hash(PLAIN_PASSWORD)



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
    

