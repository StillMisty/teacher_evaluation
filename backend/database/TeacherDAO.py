from datetime import datetime
from typing import List
from database.table import BaseService, Teachers, Comments, Teachers_score
from schemas.teacher import TeacherInfo, TeacherListPer
from schemas.comment import Comment
from config import settings
from utils import get_academicTitle
from pathlib import Path
import ujson as json

TEACHER_DIR = Path(settings.TEACHER_DIR)


class TeacherDAO:
    def insert_all_teacher():
        """插入所有老师的信息"""
        for file in TEACHER_DIR.iterdir():
            with open(file, "r", encoding="utf-8") as f:
                teacher_info = json.loads(f.read())
            id = teacher_info["teacherInfo"].get("uid")

            if (
                id <= 0
                or BaseService.session.query(Teachers).filter(Teachers.id == id).first()
            ):
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
        
    def updata_teacher_score():
        """基于时间序列更新教师评分"""
        # 获取所有教师的id
        teachers_id = BaseService.session.query(Teachers_score.teacher_id).distinct ().all()
        # 获取教师的评分，基于时间加权，最近的评分权重最大
        for teacher_id in teachers_id:
            teacher_id = teacher_id[0]
            scores = BaseService.session.query(Teachers_score).filter   (Teachers_score.teacher_id == teacher_id).all()
            teaching_attitude = 0
            teaching_level = 0
            score_end = 0
            teacher_morality = 0
            attendance_attitude = 0
            for score in scores:
                time = score.time
                now = datetime.now()
                # 时间差
                time_diff = now - time
                # 时间加权
                time_weight = 120 / (120 + time_diff.days)
                teaching_attitude += score.teaching_attitude * time_weight
                teaching_level += score.teaching_level * time_weight
                score_end += score.score_end * time_weight
                teacher_morality += score.teacher_morality * time_weight
                attendance_attitude += score.attendance_attitude * time_weight
            # 更新教师评分
            teacher = BaseService.session.query(Teachers).filter(Teachers.id ==     teacher_id).first()
            teacher.teaching_attitude = teaching_attitude
            teacher.teaching_level = teaching_level
            teacher.score_end = score_end
            teacher.teacher_morality = teacher_morality
            teacher.attendance_attitude = attendance_attitude
        BaseService.session.commit()

    def query_name(name: str) -> List[Teachers | None]:
        """根据name获取教师信息"""
        teacher = (
            BaseService.session.query(Teachers).filter(Teachers.name == name).first()
        )
        return teacher

    def query_Info(id: int) -> TeacherInfo | None:
        """根据id获取教师信息"""
        teacher = BaseService.session.query(Teachers).filter(Teachers.id == id).first()
        return teacher

    def query_allcomment(id: int) -> List[Comment] | None:
        """根据id获取教师全部评论"""
        comments = (
            BaseService.session.query(Comments)
            .filter(Comments.teacher_id == id)
            .filter(Comments.is_delete is False)
            .all()
        )
        if comments == []:
            return None
        else:
            return [
                Comment(
                    id=comment.id,
                    content=comment.content,
                    create_time=comment.create_time,
                )
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
                TeacherListPer(id=teacher.id, name=teacher.name)
                for teacher in teacher_list
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
