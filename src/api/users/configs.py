from fastapi.security import OAuth2PasswordBearer
from fastapi import Request,status
from starlette.status import HTTP_401_UNAUTHORIZED
from .exceptions import CredentialsException

class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise CredentialsException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access",
                solution="Please login before access protected rouets"
            )
        return authorization.split(" ")[1]