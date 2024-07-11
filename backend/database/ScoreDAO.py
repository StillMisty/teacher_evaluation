

from database.table import BaseService, Teachers_score
from schemas.teacher import TeacherEvaluate


class ScoreDAO():
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
    
    async def delete_score(id: int) -> bool:
        """删除教师评分"""
        score = BaseService.session.query(Teachers_score).filter(Teachers_score.id == id).first()
        if score is None:
            return False
        BaseService.session.delete(score)
        BaseService.session.commit()
        return True
    
    async def query_score_by_id(id: int) -> Teachers_score:
        """根据id获取教师评分"""
        score = BaseService.session.query(Teachers_score).filter(Teachers_score.id == id).first()
        return score
    
    
    async def update_score(id:int, score: TeacherEvaluate) -> bool:
        """更新教师评分"""
        score = BaseService.session.query(Teachers_score).filter(Teachers_score.id == id).first()
        if score is None:
            return False
        score.teaching_attitude = score.teaching_attitude
        score.teaching_level = score.teaching_level
        score.score_end = score.score_end
        score.teacher_morality = score.teacher_morality
        score.attendance_attitude = score.attendance_attitude
        BaseService.session.commit()
        return True
