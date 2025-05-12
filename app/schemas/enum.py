from enum import Enum        
        
class LoginValidationResult(Enum):
    OK = "ok"
    USER_NOT_FOUND = "user_not_found"
    INVALID_PASSWORD = "invalid_password"
    
class RefreshValidationResult(Enum):
    VALID = "valid"
    EXPIRED = "expired"
    INVALID = "invalid"
    NOT_FOUND = "not_found"