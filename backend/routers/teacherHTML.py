from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pathlib
from config import settings

router = APIRouter()

STATIC_DIR = pathlib.Path(settings.STATIC_DIR)


@router.get("/", response_class=HTMLResponse)
async def index():
    """首页"""
    html = open(STATIC_DIR / "index.html", "r", encoding="utf-8").read()
    return HTMLResponse(content=html, status_code=200)
