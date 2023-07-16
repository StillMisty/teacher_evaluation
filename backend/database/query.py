
from typing import List
import copy
import ujson as json

from database.table import BaseService, teachers, comments
from schemas.teacher import TeacherInfo, TeacherBase, TeacherCareer, TeacherListPer
from schemas.comment import Comment
from config import settings
from utils import *

TEACHER_DIR = settings.TEACHER_DIR

def query_name(name: str) -> List[teachers|None]:
    teacher = BaseService.session.query(teachers).filter(teachers.name==name).first()
    if teacher == None:
        return None
    else:
        return copy.deepcopy(teacher)

def query_id(id: int) -> teachers|None:
    if id < 0:
        return None
    teacher = BaseService.session.query(teachers).filter(teachers.id==id).first()
    if teacher == None:
        return None
    else:
        return copy.deepcopy(teacher)
    
def query_views(id: int) -> int:
    teacher = BaseService.session.query(teachers).filter(teachers.id==id).first()
    if teacher == None:
        return None
    teacher.views += 1
    return copy.deepcopy(teacher.views)


def query_baseInfo(id: int) -> TeacherBase|None:
    """根据id获取教师基本信息"""
    teacher = query_id(id)
    if teacher == None:
        return None
    
    with open(TEACHER_DIR + f"/{teacher.id}.json", "r", encoding="utf-8") as f:
        teacher_info = json.loads(f.read())
        teacher_info = teacher_info["teacherInfo"]
        teacher = TeacherBase(
            id = teacher_info['uid'],
            name = teacher_info['realname'],
            email = teacher_info.get("email",""),
            phone = teacher_info.get("phone",""),
            academicDegree = teacher_info.get("academicDegree",""),
            academicTitle = get_academicTitle(teacher_info.get("academicTitle")),
            groupname=teacher_info.get("deptName",""),
            views=query_views(id),
            photo = f'headimgs/{teacher_info["uid"]}.png'
        ) 
    return teacher

def query_Info(id: int):
    """根据id获取教师信息"""
    teacher = query_id(id)
    if teacher == None:
        return None
    
    with open(TEACHER_DIR + f"/{teacher.id}.json", "r", encoding="utf-8") as f:
        teacher_info = json.loads(f.read())
        teacher_info = teacher_info["teacherInfo"]
        teacher = TeacherInfo(
            id = teacher_info['uid'],
            name = teacher_info['realname'],
            email = teacher_info.get("email",""),
            phone = teacher_info.get("phone",""),
            academicDegree = teacher_info.get("academicDegree",""),
            academicTitle = get_academicTitle(teacher_info.get("academicTitle")),
            groupname = teacher_info.get("deptName",""),
            views = query_views(id),
            officeAddr = teacher_info.get("officeAddr",""),
            researchFields = teacher_info.get("researchFields",""),
            subject = teacher_info.get("subject",""),
            photo = f'headimgs/{teacher_info["uid"]}.png'
        ) 
    return teacher

def query_commentNum(id: int) -> int:
    """获取该教师评论总数"""
    total = BaseService.session.query(comments).filter(comments.teacher_id==id).count()
    return total

def query_comment(id: int, page: int, page_size: int) -> List[Comment]|None:
    """根据id获取教师评论"""
    data = query_id(id)
    if data == None:
        return None
    comment_list = BaseService.session.query(comments).filter(comments.teacher_id==id).offset((page-1)*page_size).limit(page_size).all()
    return copy.deepcopy(comment_list)

def query_allcomment(id: int) -> List[Comment]|None:
    """根据id获取教师全部评论"""
    teacher = query_id(id)
    if teacher == None:
        return None
    comment_list = BaseService.session.query(comments).filter(comments.teacher_id==id, comments.is_delete==0).all()
    return copy.deepcopy(comment_list)



def query_teacher_career(id: int) -> List[TeacherCareer]|None:
    '''根据id获取教师职业生涯'''
    teacher = query_id(id)
    if teacher == None:
        return None
    
    with open(TEACHER_DIR + f"/{teacher.id}.json", "r", encoding="utf-8") as f:
        teacher_info = json.loads(f.read())
        teacher_info = teacher_info.get('columnInfo',[])
        if teacher_info == []:
            return None
        return [TeacherCareer(name=info['name'],content=info['content']) for info in teacher_info if info.get('content') != None]
        
        
def query_teacher_evaluate(id: int) -> dict|None:
    '''根据id获取教师评价'''
    teacher = query_id(id)
    if teacher == None:
        return None
    
    score_teaching_attitude = teacher.teaching_attitude / teacher.teaching_attitude_people if teacher.teaching_attitude_people != 0 else 0
    score_teaching_level = teacher.teaching_level / teacher.teaching_level_people if teacher.teaching_level_people != 0 else 0
    score_score_end = teacher.score_end / teacher.score_end_people if teacher.score_end_people != 0 else 0
    score_teacher_morality = teacher.teacher_morality / teacher.teacher_morality_people if teacher.teacher_morality_people != 0 else 0
    score_attendance_attitude = teacher.attendance_attitude / teacher.attendance_attitude_people if teacher.attendance_attitude_people != 0 else 0
    round(score_teaching_attitude, 1)
    return {
        "教学态度": round(score_teaching_attitude, 1),
        "教学水平": round(score_teaching_level, 1),
        "期末捞人": round(score_score_end, 1),
        "教师人品": round(score_teacher_morality, 1),
        "考勤宽松": round(score_attendance_attitude, 1)
    }
    
def query_teacher_list(teacher_query: str) ->List[TeacherListPer]|None:
    '''获取教师列表'''
    teacher_list = BaseService.session.query(teachers).filter(teachers.name.like(f"%{teacher_query}%")).order_by(teachers.views.desc()).limit(8).all()
    if teacher_list == []:
        return None
    else: 
        return [TeacherListPer(id=teacher.id,name=teacher.name) for teacher in teacher_list]

