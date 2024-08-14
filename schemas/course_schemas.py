from typing import Optional
from pydantic import BaseModel as SCBaseModel


class CourseSchema(SCBaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    duration: int

    class Config:
        from_attributes = True