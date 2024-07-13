import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings
from slowapi import Limiter
from slowapi.util import get_remote_address

class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)

    # 调试模式
    APP_DEBUG: bool = False

    # 是否使用IP验证
    SEGMENTATION: bool = False
    # 财专ip端，用列表方便扩展
    SEGMENTATION_IP: list[str] = ["210.35.192.0-210.35.207.255"]

    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    TEMPLATE_DIR: str = os.path.join(STATIC_DIR, "template")
    TEACHER_DIR: str = os.path.join(STATIC_DIR, "teacher")
    HEADIMGS_DIR: str = os.path.join(STATIC_DIR, "headimgs")

    # 跨域请求
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # 数据库配置
    DATABASE_URL: str = "mysql://root:root@localhost:3306/teacher_evaluation?charset=utf8mb4"
    DATABASE_ECHO: bool = False
    
    # JWT配置
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 百度AI配置
    ACCESS_TOKEN: str | None = None # 到百度AI平台申请


settings = Config()
limiter = Limiter(key_func=get_remote_address)
