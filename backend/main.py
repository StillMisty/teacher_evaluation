from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import settings, limiter
from routers import teacherHTML
from routers import adminHTML
from api import teacher
from database.table import create_table
from database.insert import insert_all_teacher
from database.updata import updata_teacher_score
import os

os.chdir(os.path.dirname(__file__))


create_table()
insert_all_teacher()



app = FastAPI(debug=settings.APP_DEBUG)

# 限流策略

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 路由
app.include_router(teacherHTML.router)
app.include_router(adminHTML.router)
# api
app.include_router(teacher.router)

updata_teacher_score()

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# 静态资源目录
app.mount("/", StaticFiles(directory=settings.STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="127.0.0.1", port=80, reload=True)
