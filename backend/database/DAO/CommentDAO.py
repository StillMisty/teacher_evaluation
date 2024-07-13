from database.table import BaseService, Comments, Teachers
from schemas.comment import Admin_comment, CommentBase
from utils import content_review


class CommentDAO:
    @staticmethod
    async def insert(comment: CommentBase) -> bool:
        """插入评论"""
        result = await content_review(comment.content)
        if result is False:
            return False
        
        if BaseService.session.query(Teachers).filter(Teachers.id == comment.id).first() is None:
            return False
        
        new_comment = Comments(content=comment.content, teacher_id=comment.id)
        BaseService.session.add(new_comment)
        BaseService.session.commit()
        return True

    @staticmethod
    async def delete(id: int) -> bool:
        """删除评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        if comment is None:
            return False
        comment.is_delete = True
        BaseService.session.commit()
        return True

    @staticmethod
    async def query_all() -> list:
        """获取全部评论"""
        comments = BaseService.session.query(Comments).all()
        return comments

    @staticmethod
    async def query_by_id(id: int) -> Comments:
        """根据id获取评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        return comment

    @staticmethod
    async def query_by_teacher_id(teacher_id: int) -> list:
        """根据教师id获取评论"""
        comments = (
            BaseService.session.query(Comments)
            .filter(Comments.teacher_id == teacher_id)
            .all()
        )
        return comments

    @staticmethod
    async def query_by_content(content: str) -> list:
        """根据内容获取评论"""
        comments = (
            BaseService.session.query(Comments)
            .filter(Comments.content.like(f"%{content}%"))
            .all()
        )
        return comments

    @staticmethod
    async def update(id: int, comment: Admin_comment) -> bool:
        """更新评论"""
        old_comment = (
            BaseService.session.query(Comments).filter(Comments.id == id).first()
        )
        if old_comment is None:
            return False
        old_comment.teacher_id = comment.teacher_id
        old_comment.content = comment.content
        old_comment.is_delete = comment.is_delete
        BaseService.session.commit()
        return True
