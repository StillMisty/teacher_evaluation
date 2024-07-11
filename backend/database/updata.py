from database.table import BaseService, Teachers, Teachers_score
from schemas.teacher import TeacherEvaluate
from datetime import datetime


def updata_teacher_score():
    """基于时间序列更新教师评分"""
    # 获取所有教师的id
    teachers_id = BaseService.session.query(Teachers_score.teacher_id).distinct().all()
    # 获取教师的评分，基于时间加权，最近的评分权重最大
    for teacher_id in teachers_id:
        teacher_id = teacher_id[0]
        scores = BaseService.session.query(Teachers_score).filter(Teachers_score.teacher_id == teacher_id).all()
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
        teacher = BaseService.session.query(Teachers).filter(Teachers.id == teacher_id).first()
        teacher.teaching_attitude = teaching_attitude
        teacher.teaching_level = teaching_level
        teacher.score_end = score_end
        teacher.teacher_morality = teacher_morality
        teacher.attendance_attitude = attendance_attitude
    BaseService.session.commit()
        
        
