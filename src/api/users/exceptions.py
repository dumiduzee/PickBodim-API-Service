from fastapi import HTTPException,status


class UserExceptions(HTTPException):
    """base class for user base exceptions"""
    pass

class InvalidEmailException(UserExceptions):
    """wrong email validator exception"""
    def __init__(self, status_code, detail = None, solution = None):
        super().__init__(status_code, detail)
        self.solution = solution

class InvalidNumberException(UserExceptions):
    """wrong phone number validator exception"""
    def __init__(self, status_code, detail = None, solution = None):
        super().__init__(status_code, detail)
        self.solution = solution

class UserAlreadyExistsException(UserExceptions):
    """raise when user email already exists in database"""
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "User already exists with email", solution = "User another email to signup"):
        super().__init__(status_code, detail)
        self.solution = solution

class InternalServerException(UserExceptions):
    """raise when interl server error occured"""
    def __init__(self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Internal server error", solution = "Try again later"):
        super().__init__(status_code, detail)
        self.solution = solution

class UserRegisterException(UserExceptions):
    """raise when interl server error occured"""
    def __init__(self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Registration failed", solution = "Try again later"):
        super().__init__(status_code, detail)
        self.solution = solution


class OtpResolutionFailException(UserExceptions):
    """raise when interl server error occured"""
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Not a valid otp code", solution = "Recheck your otp code resolution"):
        super().__init__(status_code, detail)
        self.solution = solution

class UserNotFoundException(UserExceptions):
    """raise when user cannot find"""
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "User cannot find!!", solution = "Double check user id"):
        super().__init__(status_code, detail)
        self.solution = solution

class UserAlreadyVerifiedException(UserExceptions):
    """raise when user already verified"""
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "User already verified!!", solution = "Please login instead of re verify"):
        super().__init__(status_code, detail)
        self.solution = solution

class InvalidOtpCode(UserExceptions):
    """raise when invalid otp"""
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Invalid OTP code!!", solution = "Recheck your verification code or resend it"):
        super().__init__(status_code, detail)
        self.solution = solution

class OtpCodeExpiredException(UserExceptions):
    """when raise opt code expires"""
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Otp code expired!!", solution = "Genarate new verification code to continue"):
        super().__init__(status_code, detail)
        self.solution = solution

class OtpCodeStillValidException(UserExceptions):
    """When raise otp code still valid """
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Otp code Still valid!!", solution = "No need to genarate new otp. use existing one"):
        super().__init__(status_code, detail)
        self.solution = solution

class PasswordWrongException(UserExceptions):
    """_summary_

    Args:
        UserExceptions (_type_): _description_
    """
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Password is wrong for this email", solution = "Recheck your password"):
        super().__init__(status_code, detail)
        self.solution = solution

class SignInFailedException(UserExceptions):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Signin failed!", solution = "retry after sometime"):
        super().__init__(status_code, detail)
        self.solution = solution


class CredentialsException(UserExceptions):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, detail = "Unauthorized access", solution = "Logout and login again"):
        super().__init__(status_code, detail)
        self.solution = solution