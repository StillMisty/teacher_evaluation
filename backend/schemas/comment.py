from pydantic import BaseModel, conint, constr
from datetime import datetime
    
class CommentBase(BaseModel):
    id: conint(strict=True, ge=0)
    content: constr(strip_whitespace=True,max_length=300)

    
    
class Comment(CommentBase):
    create_time: datetime