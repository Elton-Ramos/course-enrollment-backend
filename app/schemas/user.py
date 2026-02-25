from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str = "student"
    is_active: bool = False


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class UserActivate(BaseModel):
    is_active: bool


class Response(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[UserRead | List[UserRead]] = None