
from database.table import BaseService, teachers
from schemas.teacher import TeacherEvaluate

def updata_teacher_score(evaluate: TeacherEvaluate):
    '''更新教师评分'''
    teacher = BaseService.session.query(teachers).filter(teachers.id==evaluate.id).first()
    if teacher == None:
        return None
    teacher.teaching_attitude += evaluate.teaching_attitude
    teacher.teaching_attitude_people += 1
    teacher.teaching_level += evaluate.teaching_level
    teacher.teaching_level_people += 1
    teacher.score_end += evaluate.score_end
    teacher.score_end_people += 1
    teacher.teacher_morality += evaluate.teacher_morality
    teacher.teacher_morality_people += 1
    teacher.attendance_attitude += evaluate.attendance_attitude
    teacher.attendance_attitude_people += 1
    
    BaseService.session.commit()