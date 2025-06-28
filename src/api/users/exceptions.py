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