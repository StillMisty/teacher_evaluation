import ujson as json
from database.table import BaseService, Teachers, Comments, Teachers_score
from schemas.comment import CommentBase
from config import settings
from schemas.teacher import TeacherEvaluate
from utils import content_review, get_academicTitle
from pathlib import Path

TEACHER_DIR = Path(settings.TEACHER_DIR)


def insert_all_teacher():
    """插入所有老师的信息"""
    for file in TEACHER_DIR.iterdir():
        with open(file, "r", encoding="utf-8") as f:
            teacher_info = json.loads(f.read())
        id = teacher_info["teacherInfo"].get("uid")

        if BaseService.session.query(Teachers).filter(Teachers.id == id).first():
            continue
        columnInfo = []
        for column in teacher_info.get("columnInfo"):
            if column.get("content") is not None:
                columnInfo.append(
                    {"name": column.get("name"), "content": column.get("content")}
                )
        new_teacher = Teachers(
            id=id,
            name=teacher_info["teacherInfo"].get("realname"),
            email=teacher_info["teacherInfo"].get("email"),
            phone=teacher_info["teacherInfo"].get("phone"),
            photo=str(id) + ".png",
            academicDegree=teacher_info["teacherInfo"].get("academicDegree"),
            academicTitle=get_academicTitle(
                teacher_info["teacherInfo"].get("academicTitle")
            ),
            deptName=teacher_info["teacherInfo"].get("deptName"),
            officeAddr=teacher_info["teacherInfo"].get("officeAddr"),
            researchFields=teacher_info["teacherInfo"].get("researchFields"),
            subject=teacher_info["teacherInfo"].get("subject"),
            views=teacher_info["teacherInfo"].get("viewNum"),
            columnInfo=columnInfo,
        )
        BaseService.session.add(new_teacher)
    BaseService.session.commit()


async def insert_comment(comment: CommentBase) -> bool:
    """插入评论"""
    result = await content_review(comment.content)
    if result is False:
        return False

    new_comment = Comments(content=comment.content, teacher_id=comment.id)
    try:
        BaseService.session.add(new_comment)
        BaseService.session.commit()
    except Exception:
        return False
    return True


async def insert_score(score: TeacherEvaluate) -> bool:
    """插入教师评分"""
    new_score = Teachers_score(
        teacher_id=score.teacher_id,
        teaching_attitude=score.teaching_attitude,
        teaching_level=score.teaching_level,
        score_end=score.score_end,
        teacher_morality=score.teacher_morality,
        attendance_attitude=score.attendance_attitude,
    )
    try:
        BaseService.session.add(new_score)
        BaseService.session.commit()
    except Exception:
        return False
    return True
