from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    title: str
    course_code: str
    capacity: int
    is_active: bool


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    course_code: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


class CourseRead(CourseBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class Response(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[CourseRead | List[CourseRead]] = None