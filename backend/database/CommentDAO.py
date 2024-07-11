

from database.table import BaseService, Comments
from schemas.comment import CommentBase
from utils import content_review


class CommentDAO():
    
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
    
    async def delete_comment(id: int) -> bool:
        """删除评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        if comment is None:
            return False
        comment.is_delete = True
        BaseService.session.commit()
        return True
    
    async def query_all_comment() -> list:
        """获取全部评论"""
        comments = BaseService.session.query(Comments).all()
        return comments
    
    async def query_comment_by_id(id: int) -> Comments:
        """根据id获取评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        return comment
    
    async def query_comment_by_teacher_id(teacher_id: int) -> list:
        """根据教师id获取评论"""
        comments = BaseService.session.query(Comments).filter(Comments.teacher_id == teacher_id).all()
        return comments
    
    async def query_comment_by_content(content: str) -> list:
        """根据内容获取评论"""
        comments = BaseService.session.query(Comments).filter(Comments.content.like(f"%{content}%")).all()
        return comments
    
    async def update_comment(id: int, comment: CommentBase) -> bool:
        """更新评论"""
        comment = BaseService.session.query(Comments).filter(Comments.id == id).first()
        if comment is None:
            return False
        comment.content = comment.content
        BaseService.session.commit()
        return True