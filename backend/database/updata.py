from database.table import BaseService, Teachers
from schemas.teacher import TeacherEvaluate


def updata_teacher_score(evaluate: TeacherEvaluate):
    """更新教师评分"""
    # TODO: 优化
