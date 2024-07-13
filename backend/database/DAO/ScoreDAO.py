from database.table import BaseService, Teachers, Teachers_score
from schemas.teacher import TeacherEvaluate


class ScoreDAO:
    @staticmethod
    async def insert(score: TeacherEvaluate):
        """插入教师评分"""
        if (
            BaseService.session.query(Teachers)
            .filter(Teachers.id == score.teacher_id)
            .first()
            is None
        ):
            return False

        new_score = Teachers_score(
            teacher_id=score.teacher_id,
            teaching_attitude=score.teaching_attitude,
            teaching_level=score.teaching_level,
            score_end=score.score_end,
            teacher_morality=score.teacher_morality,
            attendance_attitude=score.attendance_attitude,
        )
        BaseService.session.add(new_score)
        BaseService.session.commit()
        return True

    @staticmethod
    async def delete(id: int):
        """删除教师评分"""
        score = (
            BaseService.session.query(Teachers_score)
            .filter(Teachers_score.id == id)
            .first()
        )
        if score is None:
            return False
        BaseService.session.delete(score)
        BaseService.session.commit()
        return True

    @staticmethod
    async def query_all():
        """获取所有教师评分"""
        scores = BaseService.session.query(Teachers_score).all()
        return [
            {
                "id": score.id,
                "teacher_id": score.teacher_id,
                "teaching_attitude": score.teaching_attitude,
                "teaching_level": score.teaching_level,
                "score_end": score.score_end,
                "teacher_morality": score.teacher_morality,
                "attendance_attitude": score.attendance_attitude,
            }
            for score in scores
        ]

    @staticmethod
    async def query_by_id(id: int):
        """根据id获取教师评分"""
        score = (
            BaseService.session.query(Teachers_score)
            .filter(Teachers_score.id == id)
            .first()
        )
        return score

    @staticmethod
    async def update(id: int, score: TeacherEvaluate):
        """更新教师评分"""
        old_score = (
            BaseService.session.query(Teachers_score)
            .filter(Teachers_score.id == id)
            .first()
        )
        if old_score is None:
            return False
        old_score.teaching_attitude = score.teaching_attitude
        old_score.teaching_level = score.teaching_level
        old_score.score_end = score.score_end
        old_score.teacher_morality = score.teacher_morality
        old_score.attendance_attitude = score.attendance_attitude
        BaseService.session.commit()
        return True
