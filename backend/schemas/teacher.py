from pydantic import BaseModel, conint

class TeacherBase(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    photo: str
    academicDegree: str
    academicTitle: str
    groupname: str
    views: int

    
class TeacherInfo(TeacherBase):
    officeAddr: str
    researchFields: str
    subject: str
    
class TeacherCareer(BaseModel):
    name: str
    content: str

class TeacherEvaluate(BaseModel):
    id: conint(strict=True, ge=0)
    teaching_attitude: conint(strict=True, ge=0, le=5) #教学态度
    teaching_level: conint(strict=True, ge=0, le=5) #教学水平
    score_end: conint(strict=True, ge=0, le=5) #期末捞人
    teacher_morality: conint(strict=True, ge=0, le=5) #教师人品
    attendance_attitude: conint(strict=True, ge=0, le=5) #考勤宽松
    
class TeacherListPer(BaseModel):
    id: int
    name: str