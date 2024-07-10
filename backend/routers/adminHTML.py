from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pathlib
from config import settings

router = APIRouter()

STATIC_DIR = pathlib.Path(settings.STATIC_DIR)


@router.get("/admin", response_class=HTMLResponse)
async def index():
    """管理员页面"""
    html = open(STATIC_DIR / "admin.html", "r", encoding="utf-8").read()
    return HTMLResponse(content=html, status_code=200)