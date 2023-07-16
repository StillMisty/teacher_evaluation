from fastapi import APIRouter, Cookie, File, UploadFile
from schemas.response import success, fail
from database.crud import *

router = APIRouter(prefix="/super", tags=["超级管理员"])


    
    