from typing import List
from database.table import BaseService, Teachers, Comments
from schemas.teacher import TeacherBase, TeacherListPer
from schemas.comment import Comment
from config import settings

TEACHER_DIR = settings.TEACHER_DIR


def query_name(name: str) -> List[Teachers | None]:
    """根据name获取教师信息"""
    teacher = BaseService.session.query(Teachers).filter(Teachers.name == name).first()
    return teacher


def query_Info(id: int) -> TeacherBase | None:
    """根据id获取教师信息"""
    teacher = BaseService.session.query(Teachers).filter(Teachers.id == id).first()
    return teacher


def query_allcomment(id: int) -> List[Comment] | None:
    """根据id获取教师全部评论"""
    
    comments = (
        BaseService.session.query(Comments)
        .filter(Comments.teacher_id == id)
        .filter(Comments.is_delete == 0)
        .all()
    )
    if comments == []:
        return None
    else:
        return [
            Comment(id=comment.id, content=comment.content, create_time=comment.create_time)
            for comment in comments
        ]


def query_teacher_evaluate(id: int) -> dict | None:
    """根据id获取教师评价"""
    teacher = BaseService.session.query(Teachers).filter(Teachers.id == id).first()
    if teacher is None:
        return None
    
    return {
        "教学态度": teacher.teaching_attitude,
        "教学水平": teacher.teaching_level,
        "期末捞人": teacher.score_end,
        "教师人品": teacher.teacher_morality,
        "考勤宽松": teacher.attendance_attitude,
    }


def query_teacher_list(teacher_query: str) -> List[TeacherListPer] | None:
    """获取教师列表"""
    teacher_list = (
        BaseService.session.query(Teachers)
        .filter(Teachers.name.like(f"%{teacher_query}%"))
        .order_by(Teachers.views.desc())
        .limit(8)
        .all()
    )
    if teacher_list == []:
        return None
    else:
        return [
            TeacherListPer(id=teacher.id, name=teacher.name) for teacher in teacher_list
        ]


def query_hot_teacher_list() -> list[TeacherListPer]:
    """获取热门教师列表"""
    teacher_list = (
        BaseService.session.query(Teachers)
        .order_by(Teachers.views.desc())
        .limit(4)
        .all()
    )
    return [
        TeacherListPer(id=teacher.id, name=teacher.name) for teacher in teacher_list
    ]
