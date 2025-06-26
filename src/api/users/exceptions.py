from fastapi import HTTPException


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