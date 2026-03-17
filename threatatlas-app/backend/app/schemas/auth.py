from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Decoded token data schema."""
    user_id: int | None = None


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str
