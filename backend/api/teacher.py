from fastapi import APIRouter, Query, Request
from database.DAO.TeacherDAO import TeacherDAO
from database.DAO.ScoreDAO import ScoreDAO
from database.DAO.CommentDAO import CommentDAO
from schemas.response import success, fail
from schemas.teacher import TeacherEvaluate
from schemas.comment import CommentBase
from config import settings, limiter
from utils import ip_review

router = APIRouter(prefix="/api/teacher", tags=["教师"])

TEACHER_DIR = settings.TEACHER_DIR


@router.get("/get_teacher_info")
async def get_teacher_info(teacher_id: int = Query(...)):
    """
    从id获取教师信息
    """
    teahcer = await TeacherDAO.query_info(teacher_id)
    if teahcer:
        return success(teahcer)
    else:
        return fail(msg="没有找到该教师", code=404)


@router.get("/get_teacher_name")
async def get_teacher_name(name: str = Query(..., max_length=10, min_length=2)):
    """
    从名字获取教师信息
    """
    teacher = await TeacherDAO.query_name(name)
    if teacher:
        return success(teacher)
    else:
        return fail(msg="没有找到该教师", code=404)


@router.get("/id_teacher_allcomment")
async def get_teacher_allcomment(
    teacher_id: int = Query(...),
):
    """
    从id获取教师所有评论
    """
    comments = await TeacherDAO.query_allcomment(teacher_id)
    data = {"id": teacher_id, "comments": comments}
    return success(data=data)


@router.get("/id_teacher_evaluate")
async def id_teacher_evaluate(
    teacher_id: int = Query(...),
):
    """从id获取教师评分"""
    evaluate = await TeacherDAO.query_evaluate(teacher_id)
    if evaluate is None:
        return fail(msg="没有找到该教师", code=404)
    else:
        data = {
            "id": teacher_id,
            "score": evaluate,
        }
        return success(data=data)


@router.get("/get_teacher_list")
async def get_teacher_list(
    teacher_query: str = Query(max_length=10, min_length=1),
):
    """获取教师列表"""
    teachers_list = await TeacherDAO.query_teacher_list(teacher_query)

    if teachers_list is None:
        return fail(msg="没有找到该教师", code=404)
    else:
        data = teachers_list
        return success(data=data)


@router.get("/get_hot_teacher_list")
async def get_hot_teacher_list():
    """获取热门教师列表"""
    teachers_list = await TeacherDAO.query_hot_teacher_list()
    return success(data=teachers_list)


@router.post("/post_teacher_score")
@limiter.limit("3/minute")
async def post_teacher_score(request: Request, *, teacher_scores: TeacherEvaluate):
    """提交教师评分"""
    if ip_review(request.client.host) is False:
        return fail(msg="您的IP不在允许范围内", code=403)

    if await ScoreDAO.insert(teacher_scores):
        return success(msg="提交成功")
    else:
        return fail(msg="没有找到该教师", code=404)


@router.post("/post_teacher_comment")
@limiter.limit("3/minute")
async def post_teacher_comment(request: Request, *, teacher_comment: CommentBase):
    """提交教师评论"""

    if ip_review(request.client.host) is False:
        return fail(msg="您的IP不在允许范围内", code=403)

    if await CommentDAO.insert(teacher_comment):
        return success(msg="提交成功")
    else:
        return fail(msg="没有找到该教师", code=404)
