from pydantic import BaseModel, conint

class Admin_score(BaseModel):
    id: int
    teacher_id: conint(strict=True, ge=0)
    teaching_attitude: conint(strict=True, ge=0, le=5) #教学态度
    teaching_level: conint(strict=True, ge=0, le=5) #教学水平
    score_end: conint(strict=True, ge=0, le=5) #期末捞人
    teacher_morality: conint(strict=True, ge=0, le=5) #教师人品
    attendance_attitude: conint(strict=True, ge=0, le=5) #考勤宽松
    

