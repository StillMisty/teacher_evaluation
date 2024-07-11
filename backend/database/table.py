from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from config import settings


class BaseService(object):
    engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
    Session = sessionmaker(bind=engine)
    session = Session()


Base = declarative_base()


class Teachers_score(Base):
    __tablename__ = "teachers_score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("teahcers.id"))
    time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    # 教学态度
    teaching_attitude = Column(Integer, default=0)
    # 教学水平
    teaching_level = Column(Integer, default=0)
    # 期末捞人
    score_end = Column(Integer, default=0)
    # 教师人品
    teacher_morality = Column(Integer, default=0)
    # 考勤宽松
    attendance_attitude = Column(Integer, default=0)


class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(300))
    create_time = Column(DateTime, default=datetime.now())
    teacher_id = Column(Integer, ForeignKey("teahcers.id"))
    is_delete = Column(Boolean, default=False)


class Teachers(Base):
    __tablename__ = "teahcers"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), default="")
    email = Column(String(50), default="")
    phone = Column(String(20), default="")
    photo = Column(String(100), default="")
    academicDegree = Column(String(20), default="")
    academicTitle = Column(String(20), default="")
    deptName = Column(Text, default="")
    officeAddr = Column(String(50), default="")
    researchFields = Column(Text, default="")
    subject = Column(String(20), default="")
    views = Column(Integer, default=0)
    columnInfo = Column(JSON)

    teaching_attitude = Column(Integer, default=0)
    teaching_level = Column(Integer, default=0)
    score_end = Column(Integer, default=0)
    teacher_morality = Column(Integer, default=0)
    attendance_attitude = Column(Integer, default=0)

    teachers_score = relationship("Teachers_score", backref="teahcers")
    comments = relationship("Comments", backref="teahcers")


def create_table():
    """创建表"""
    Base.metadata.create_all(BaseService.engine)
