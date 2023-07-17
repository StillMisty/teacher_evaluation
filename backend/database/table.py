
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from config import settings

class BaseService(object):
    engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
    Session = sessionmaker(bind = engine)
    session = Session()

Base=declarative_base()

class teachers(Base):
    __tablename__='teahcers'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    views = Column(Integer, default=0)
    is_delete = Column(Integer, default=0)
    # 教学态度
    teaching_attitude = Column(Integer, default=0)
    teaching_attitude_people = Column(Integer, default=0)
    # 教学水平
    teaching_level = Column(Integer, default=0)    
    teaching_level_people = Column(Integer, default=0)
    # 期末捞人
    score_end = Column(Integer, default=0)
    score_end_people = Column(Integer, default=0)
    # 教师人品
    teacher_morality = Column(Integer, default=0)
    teacher_morality_people = Column(Integer, default=0)
    # 考勤宽松
    attendance_attitude = Column(Integer, default=0)
    attendance_attitude_people = Column(Integer, default=0)
    
    
    
class comments(Base):
    __tablename__='comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200))
    create_time = Column(DateTime, default=datetime.now())
    teacher_id = Column(Integer, ForeignKey('teahcers.id'))
    is_delete = Column(Integer, default=0)
    
def create_table():
    Base.metadata.create_all(BaseService.engine)