from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pathlib
from config import settings

router = APIRouter(prefix="/admin", tags=["管理员页面"])

STATIC_DIR = pathlib.Path(settings.STATIC_DIR)


@router.get("/", response_class=HTMLResponse)
async def index():
    """管理员页面"""
    html = open(STATIC_DIR / "admin.html", "r", encoding="utf-8").read()
    return HTMLResponse(content=html, status_code=200)

@router.get("/login", response_class=HTMLResponse)
async def login():
    """管理员登录页面"""
    html = open(STATIC_DIR / "login.html", "r", encoding="utf-8").read()
    return HTMLResponse(content=html, status_code=200)