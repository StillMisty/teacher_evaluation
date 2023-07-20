
from fastapi import APIRouter,  Query, Request
from database.query import *
from database.updata import updata_teacher_score
from database.insert import insert_comment
from schemas.response import success, fail
from schemas.teacher import TeacherEvaluate
from schemas.comment import CommentBase, Comment
from config import settings
from utils import *

router = APIRouter(prefix="/api/teacher", tags=["教师"])

TEACHER_DIR = settings.TEACHER_DIR

@router.get("/get_teacher_brief")
async def get_teacher_brief(teacher_id: int = Query(...)):
    """
    从id获取教师的基本信息
    """
    data = query_baseInfo(teacher_id)
    
    if data == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        return success(data=data)

@router.get("/get_teacher_info")
async def get_teacher_info(teacher_id: int = Query(...)):
    """
    从id获取教师信息
    """
    data = query_Info(teacher_id)
    if data == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        return success(data=data)
    
@router.get("/get_teacher_name")
async def get_teacher_name(name: str = Query(..., max_length=10, min_length=2)):
    """
    从名字获取教师信息
    """
    teacher = query_name(name)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = query_Info(teacher.id)
        return success(data)

@router.get("/id_teacher_comment")
async def get_teacher_comment(
    teacher_id: int = Query(...), 
    page: int = Query(1, gt=0), 
    page_size: int = Query(10, gt=0)
):
    """
    从id获取教师评论
    """
    teacher = query_id(teacher_id)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    
    comments_total = query_commentNum(teacher_id)
    comments = query_comment(teacher_id, page, page_size)
    data = {
        "id": teacher_id,
        "comments": comments,
        "comments_total": comments_total
    }
    return success(data=data)

@router.get("/id_teacher_allcomment")
async def get_teacher_allcomment(
    teacher_id: int = Query(...), 
):
    """
    从id获取教师所有评论
    """
    teacher = query_id(teacher_id)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    
    comments_total = query_commentNum(teacher_id)
    comments = query_allcomment(teacher_id)
    data = {
        "id": teacher_id,
        "comments": comments,
        "comments_total": comments_total
    }
    return success(data=data)
    
@router.get("/name_teacher_comment")
async def get_teacher_comment(
    teacher_name: str = Query(...), 
    page: int = Query(1, gt=0), 
    page_size: int = Query(10, gt=0)
):
    """
    从名字获取教师评论
    """
    teacher = query_name(teacher_name)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    
    comments_total = query_commentNum(teacher.id)
    comments = query_comment(teacher.id, page, page_size)
    data = {
        "id": teacher.id,
        "comments": comments,
        "comments_total" : comments_total
    }
    return data

@router.get("/name_teacher_allcomment")
async def get_teacher_allcomment(
    teacher_name: str = Query(...), 
):
    """
    从名字获取教师所有评论
    """
    teacher = query_name(teacher_name)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    comments_total = query_commentNum(teacher.id)
    comments = query_allcomment(teacher.id)
    data = {
        "id": teacher.id,
        "comments": comments,
        "comments_total": comments_total
    }
    return data
    
@router.get("/id_teacher_career")
async def id_teacher_career(
    teacher_id: int = Query(...),
):
    """
    从id获取教师经历
    """
    
    career = query_teacher_career(teacher_id)
    if career == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = {
            "id": teacher_id,
            "career" : career,
        }
        return success(data=data)
    
@router.get("/name_teacher_career")
async def name_teacher_career(
    teacher_name: str = Query(...),
):
    """
    从名字获取教师经历
    """
    teacher = query_name(teacher_name)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    
    career= query_teacher_career(teacher.id)
    if career == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = {
            "id": teacher.id,
            "career" : career,
        }
        return success(data=data)
    
@router.get("/id_teacher_evaluate")
async def id_teacher_evaluate(
    teacher_id: int = Query(...),
):
    '''从id获取教师评分'''
    evaluate  = query_teacher_evaluate(teacher_id)
    if evaluate == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = {
            "id": teacher_id,
            "score" : evaluate,
        }
        return success(data=data)
    
@router.get("/name_teacher_evaluate")
async def name_teacher_evaluate(
    teacher_name: str = Query(...),
):
    '''从名字获取教师评分'''
    teacher = query_name(teacher_name)
    if teacher == None:
        fail(msg="没有找到该教师",code=404)
        
    evaluate  = query_teacher_evaluate(teacher.id)
    if evaluate == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = {
            "id": teacher.id,
            "score" : evaluate,
        }
        return success(data=data)
    
@router.post("/post_teacher_score")
async def post_teacher_score(
    request: Request,
    *,
    teacher_scores: TeacherEvaluate
):
    '''提交教师评分'''
    if ip_review(request.client.host) == False:
        return fail(msg="您的IP不在允许范围内",code=403)
    
    teacher = query_id(teacher_scores.id)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    
    updata_teacher_score(teacher_scores)
    
    return success(msg="提交成功")

@router.post("/post_teacher_comment")
async def post_teacher_comment(
    request: Request,
    *,
    teacher_comment: CommentBase
):
    '''提交教师评论'''
    
    if ip_review(request.client.host) == False:
        return fail(msg="您的IP不在允许范围内",code=403)
    
    teacher = query_id(teacher_comment.id)
    if teacher == None:
        return fail(msg="没有找到该教师",code=404)
    
    await insert_comment(teacher_comment)
    
    return success(msg="提交成功")

@router.get("/get_teacher_list")
async def get_teacher_list(
    teacher_query: str = Query(max_length=10, min_length=1),
):
    '''获取教师列表'''
    teachers_list = query_teacher_list(teacher_query)
    
    if teachers == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = teachers_list
        return success(data=data)
    
@router.get("/get_hot_teacher_list")
async def get_hot_teacher_list():
    '''获取热门教师列表'''
    teachers_list = query_hot_teacher_list()
    
    if teachers == None:
        return fail(msg="没有找到该教师",code=404)
    else:
        data = teachers_list
        return success(data=data)