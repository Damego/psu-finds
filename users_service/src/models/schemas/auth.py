from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = Field(default=None)
    token_type: str = "Bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class ChangeEmailPayload(BaseModel):
    token: str


class ChangePasswordPayload(BaseModel):
    password: str
    token: str
