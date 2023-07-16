from typing import List
import copy
import ujson as json

from database.table import BaseService, teachers, comments
from schemas.teacher import TeacherInfo, TeacherBase
from schemas.comment import CommentBase
from config import settings
from utils import *

STATIC_DIR = settings.STATIC_DIR

def insert_all_teacher():
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
            
def insert_comment(comment: CommentBase):
    new_comment = comments(
        content=comment.content,
        teacher_id=comment.id
    )
    BaseService.session.add(new_comment)
    BaseService.session.commit()
    