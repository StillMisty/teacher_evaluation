interface Teacher {
  id: number
  name: string
  email: string
  phone: string
  photo: string
  academicDegree: string
  academicTitle: string
  deptName: string
  views: number
}

interface TeacherPer {
  id: number
  name: string
}

interface ColumnInfo {
  name: string
  content: string
}

interface TeacherInfo extends Teacher {
  officeAddr: string
  researchFields: string
  subject: string
  columnInfo: ColumnInfo[]
}

export type { Teacher, TeacherInfo, TeacherPer }
