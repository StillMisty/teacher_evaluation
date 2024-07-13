from fastapi import APIRouter, Body, Depends, File, Query, UploadFile
import psutil
import platform
from auth.security import get_current_active_user, get_password_hash
from database.DAO.CommentDAO import CommentDAO
from database.DAO.ScoreDAO import ScoreDAO
from database.DAO.AdminDAO import AdminDAO
from database.DAO.TeacherDAO import TeacherDAO
from schemas.comment import Admin_comment, CommentBase
from schemas.response import success, fail
from schemas.teacher import TeacherEvaluate, TeacherInfo
from config import settings

router = APIRouter(
    prefix="/api/admin",
    tags=["管理员"],
    dependencies=[Depends(get_current_active_user)],
)

HEADIMGS_DIR = settings.HEADIMGS_DIR

@router.post("/register")
async def register(username: str, password: str):
    password = get_password_hash(password)
    AdminDAO.insert(username, password)
    return {"msg": "注册成功"}


@router.get("/system/info", summary="系统信息")
async def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return success(
        data={
            "system": f"{platform.system()} {platform.release()} {platform.version()}",
            "machine": f"{platform.machine()} {platform.processor()}",
            "cpu": f"{psutil.cpu_count()}核 {psutil.cpu_freq().max}MHz",
            "cpu_percent": cpu_percent,
            "memory_total": round(memory.total / (1024**3), 2),
            "memory_available": round(memory.available / (1024**3), 2),
            "disk_total": round(disk.total / (1024**3), 2),
            "disk_used": round(disk.used / (1024**3), 2),
        }
    )


@router.get("/teacher/search", summary="教师搜索")
async def search_teacher(name: str):
    teacher = await TeacherDAO.query_name_like(name)
    if not teacher:
        return fail(msg="教师不存在")
    return success(data=teacher)


@router.get("/teacher", summary="教师详细分页列表")
async def get_teacher(page: int = Query(..., ge=1), size: int = Query(..., ge=1)):
    teacher_list = await TeacherDAO.get_teacher_by_page(page, size)
    total = await TeacherDAO.get_teacher_total()
    return success(data={"teacher_list": teacher_list, "total": total})


@router.get("/teacher/{id}", summary="教师详细信息")
async def get_teacher_info(id: int):
    teacher = await TeacherDAO.query_info(id)
    if teacher is None:
        return fail(msg="教师不存在")
    return success(data=teacher)


@router.put("/teacher", summary="更新教师信息")
async def update_teacher(teacher: TeacherInfo):
    TeacherDAO.update(teacher)
    return success(msg="更新成功")

@router.post("/teacher/photo", summary="修改教师头像")
async def update_teacher_photo(id: int, file: UploadFile = File(...)):
    if not await TeacherDAO.query_info(id):
        return fail(msg="教师不存在", code=404)
    
    content = await file.read()
    print(f"{HEADIMGS_DIR}\{id}.png")
    with open( f"{HEADIMGS_DIR}\{id}.png", "wb") as f:
        f.write(content)

    return success(msg="更新成功")

@router.get("/teacher/evaluate/all", summary="所有的教师评分")
async def get_all_teacher_evaluate():
    print("get_all_teacher_evaluate")
    score = await ScoreDAO.query_all()
    if not score:
        return fail(msg="评分为空")
    return success(data=score)


@router.get("/teacher/evaluate/{id}", summary="教师评分")
async def get_teacher_evaluate(id: int):
    evaluate = await ScoreDAO.query_by_id(id)
    if evaluate is None:
        return fail(msg="教师不存在")
    return success(data=evaluate)


@router.post("/teacher/evaluate", summary="添加教师评分")
async def add_teacher_evaluate(teacherEvaluate: TeacherEvaluate):
    if not await ScoreDAO.insert(teacherEvaluate):
        return fail(msg="教师不存在", code=404)
    return success(msg="添加成功")


@router.put("/teacher/evaluate/{id}", summary="更新教师评价")
async def update_teacher_evaluate(id: int, teacherEvaluate: TeacherEvaluate):
    if not await ScoreDAO.update(id, teacherEvaluate):
        return fail(msg="评价不存在", code=404)
    return success(msg="更新成功")


@router.delete("/teacher/evaluate/{id}", summary="删除教师评分")
async def delete_teacher_evaluate(id: int):
    await ScoreDAO.delete(id)
    return success(msg="删除成功")


@router.get("/teacher/comment/all", summary="所有的教师评论")
async def get_teacher_comment():
    comment = await CommentDAO.query_all()
    if not comment:
        return fail(msg="评论为空")
    return success(data=comment)


@router.post("/teacher/comment", summary="添加教师评论")
async def add_teacher_comment(comment: CommentBase):
    if not await CommentDAO.insert(comment):
        return fail(msg="教师不存在", code=404)
    return success(msg="添加成功")


@router.put("/teacher/comment/{id}", summary="更新教师评论")
async def update_teacher_comment(id: int, comment: Admin_comment):
    await CommentDAO.update(id, comment)
    return success(msg="更新成功")


@router.delete("/teacher/comment/{id}", summary="删除教师评论")
async def delete_teacher_comment(id: int):
    await CommentDAO.delete(id)
    return success(msg="删除成功")


@router.get("/teacher/comment/{id}", summary="教师评论")
async def get_teacher_comment_by_id(id: int):
    comment = await CommentDAO.query_by_id(id)
    if not comment:
        return fail(msg="评论不存在")
    return success(data=comment)
