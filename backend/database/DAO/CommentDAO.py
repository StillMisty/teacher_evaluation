from database.table import BaseService, Comments
from schemas.comment import CommentBase
from utils import content_review


class CommentDAO:
    async def insert(self, comment: CommentBase) -> bool:
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

    async def delete(self, id: int) -> bool:
        """删除评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        if comment is None:
            return False
        comment.is_delete = True
        BaseService.session.commit()
        return True

    async def query_all(self) -> list:
        """获取全部评论"""
        comments = BaseService.session.query(Comments).all()
        return comments

    async def query_by_id(self, id: int) -> Comments:
        """根据id获取评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        return comment

    async def query_by_teacher_id(self, teacher_id: int) -> list:
        """根据教师id获取评论"""
        comments = (
            BaseService.session.query(Comments)
            .filter(Comments.teacher_id == teacher_id)
            .all()
        )
        return comments

    async def query_by_content(self, content: str) -> list:
        """根据内容获取评论"""
        comments = (
            BaseService.session.query(Comments)
            .filter(Comments.content.like(f"%{content}%"))
            .all()
        )
        return comments

    async def update(self, id: int, comment: CommentBase) -> bool:
        """更新评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        if comment is None:
            return False
        comment.content = comment.content
        BaseService.session.commit()
        return True


commentDAO = CommentDAO()
