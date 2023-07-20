
try:
    import ujson as json
except:
    import json

from database.table import BaseService, teachers, comments
from schemas.comment import CommentBase
from config import settings
from utils import *

STATIC_DIR = settings.STATIC_DIR

def insert_all_teacher():
    '''插入所有老师的信息'''
    with open(STATIC_DIR + "/total_info.json", "r", encoding="utf-8") as f:
        total_info = json.loads(f.read())
        for teacher in total_info:
            id = teacher.get("uid")
            if id == None:
                continue
            if BaseService.session.query(teachers).where(id == teachers.id).first() != None:
                continue
            name = teacher.get("realname")
            views = teacher.get("viewNum")
            new_teacher = teachers(id=id, name=name, views=views)
            BaseService.session.add(new_teacher)
            BaseService.session.commit()
            
async def insert_comment(comment: CommentBase) -> bool:
    '''插入评论'''
    result = await content_review(comment.content)
    if result == False:
        return False
    
    new_comment = comments(
        content=comment.content,
        teacher_id=comment.id
    )
    BaseService.session.add(new_comment)
    BaseService.session.commit()
    return True
    