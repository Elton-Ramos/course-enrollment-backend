from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EnrollmentBase(BaseModel):
    user_id: UUID
    course_id: UUID
    


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Response(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[EnrollmentRead | List[EnrollmentRead]] = None