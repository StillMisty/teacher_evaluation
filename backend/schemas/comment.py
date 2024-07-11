from pydantic import BaseModel, conint, constr
from datetime import datetime


class CommentBase(BaseModel):
    id: conint(strict=True, ge=0)
    content: constr(strip_whitespace=True, max_length=300, min_length=5)


class Comment(CommentBase):
    create_time: datetime

class Admin_comment(BaseModel):
    id: int
    teacher_id: conint(strict=True, ge=0)
    content: constr(strip_whitespace=True, max_length=300, min_length=5)
    create_time: datetime
    is_delete: bool