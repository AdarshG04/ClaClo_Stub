from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Feedback(BaseModel):
    student_id: str
    teacher_id: str
    grade: str
    comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)