from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator

class StatusEnum(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class TodoItem(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the to-do item")
    description: Optional[str] = Field(None, max_length=500, description="Description of the to-do item")
    due_date: Optional[datetime] = Field(None, description="Due date for the to-do item")
    status: StatusEnum = Field(default=StatusEnum.PENDING, description="Current status of the to-do item")

    @validator('due_date', pre=True, always=True)
    def validate_due_date(cls, value):
        if value and value < datetime.now():
            raise ValueError('Due date cannot be in the past')
        return value