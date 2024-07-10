import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings


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
    PHOTO_DIR: str = os.path.join(STATIC_DIR, "photo")

    # 跨域请求
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # 数据库配置
    DATABASE_URL: str = "mysql://root:root@localhost:3306/teacher_evaluation?charset=utf8mb4"
    DATABASE_ECHO: bool = False

    # 百度AI配置
    ACCESS_TOKEN: str | None = None # 到百度AI平台申请


settings = Config()
