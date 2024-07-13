<template>
  <div class="flex flex-col h-full p-0">
    <div>
      <div>
        <el-button type="primary" @click="openAddDialog">添加评分</el-button>
        <el-dialog v-model="dialogFormVisible" title="添加评分" width="800">
          <el-form>
            <el-form-item label="教师ID">
              <el-input v-model="score.teacher_id" type="number"></el-input>
            </el-form-item>
            <el-form-item label="教学态度">
              <el-input-number v-model="score.teaching_attitude" :min="0" :max="5" />
            </el-form-item>
            <el-form-item label="教学水平">
              <el-input-number v-model="score.teaching_level" :min="0" :max="5" />
            </el-form-item>
            <el-form-item label="期末捞人">
              <el-input-number v-model="score.score_end" :min="0" :max="5" />
            </el-form-item>
            <el-form-item label="教师人品">
              <el-input-number v-model="score.teacher_morality" :min="0" :max="5" />
            </el-form-item>
            <el-form-item label="考勤态度">
              <el-input-number v-model="score.attendance_attitude" :min="0" :max="5" />
            </el-form-item>
          </el-form>
          <template v-slot:footer>
            <span class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="handleAdd">确 定</el-button>
            </span>
          </template>
        </el-dialog>
      </div>
    </div>
    <el-table :data="data" style="width: 100%">
      { id: number teacher_id: number teaching_attitude: number teaching_level: number score_end:
      number teacher_morality: number attendance_attitude: number }
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="teacher_id" label="教师ID"></el-table-column>
      <el-table-column prop="teaching_attitude" label="教学态度"></el-table-column>
      <el-table-column prop="teaching_level" label="教学水平"></el-table-column>
      <el-table-column prop="score_end" label="期末捞人"></el-table-column>
      <el-table-column prop="teacher_morality" label="教师人品"></el-table-column>
      <el-table-column prop="attendance_attitude" label="考勤态度"></el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" plain @click="handleEdit(scope.row.id)">编 辑</el-button>
          <el-button type="danger" plain @click="handleDelete(scope.row.id)">删 除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="编辑评分" v-model="dialogTableVisible" width="800px">
      <el-form>
        <el-form-item label="教师ID">
          <el-input v-model="score.teacher_id" type="number" disabled></el-input>
        </el-form-item>
        <el-form-item label="教学态度">
          <el-input-number v-model="score.teaching_attitude" :min="0" :max="5" />
        </el-form-item>
        <el-form-item label="教学水平">
          <el-input-number v-model="score.teaching_level" :min="0" :max="5" />
        </el-form-item>
        <el-form-item label="期末捞人">
          <el-input-number v-model="score.score_end" :min="0" :max="5" />
        </el-form-item>
        <el-form-item label="教师人品">
          <el-input-number v-model="score.teacher_morality" :min="0" :max="5" />
        </el-form-item>
        <el-form-item label="考勤态度">
          <el-input-number v-model="score.attendance_attitude" :min="0" :max="5" />
        </el-form-item>
      </el-form>
      <template v-slot:footer>
        <span class="dialog-footer">
          <el-button @click="dialogTableVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleSave">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { Score } from '@/themes/Score'
import { ElMessage } from 'element-plus'
import type { Response } from '@/themes/Response'

const dialogFormVisible = ref(false)
const dialogTableVisible = ref(false)
const data = ref<Score[]>([])

const score = ref<Score>({
  id: 0,
  teacher_id: 0,
  teaching_attitude: 0,
  teaching_level: 0,
  score_end: 0,
  teacher_morality: 0,
  attendance_attitude: 0
})

const fetchData = () => {
  fetch('api/admin/teacher/evaluate/all', {
    method: 'GET',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token')
    }
  })
    .then((res) => res.json())
    .then((res: Response) => {
      if (res.code === 200) {
        data.value = res.data
      } else {
        ElMessage.error(res.message)
      }
    })
}
fetchData()

const openAddDialog = () => {
  score.value = {
    id: 0,
    teacher_id: 0,
    teaching_attitude: 0,
    teaching_level: 0,
    score_end: 0,
    teacher_morality: 0,
    attendance_attitude: 0
  }
  dialogFormVisible.value = true
}

const handleAdd = () => {
  scoreToNumberAndCheck()
  fetch('api/admin/teacher/evaluate', {
    method: 'POST',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(score.value)
  })
    .then((res) => res.json())
    .then((res: Response) => {
      if (res.code === 200) {
        ElMessage.success(res.message)
        fetchData()
        dialogFormVisible.value = false
      } else {
        ElMessage.error(res.message)
      }
    })
}

const handleEdit = (id: number) => {
  score.value = Object.assign(
    {},
    data.value.find((item) => item.id === id)
  )
  dialogTableVisible.value = true
}

const handleSave = () => {
  scoreToNumberAndCheck()
  console.log(JSON.stringify(score.value))
  fetch(`api/admin/teacher/evaluate/${score.value.id}`, {
    method: 'PUT',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(score.value)
  })
    .then((res) => res.json())
    .then((res: Response) => {
      if (res.code === 200) {
        ElMessage.success(res.message)
        fetchData()
        dialogTableVisible.value = false
      } else {
        ElMessage.error(res.message)
      }
    })
}

const handleDelete = (id: number) => {
  fetch(`api/admin/teacher/evaluate/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token'),
      'Content-Type': 'application/json'
    }
  })
    .then((res) => res.json())
    .then((res: Response) => {
      if (res.code === 200) {
        ElMessage.success(res.message)
        fetchData()
      } else {
        ElMessage.error(res.message)
      }
    })
}

const scoreToNumberAndCheck = () => {
  // 将Score对象的属性值转换为数字类型
  score.value.teacher_id = Number(score.value.teacher_id)
  score.value.teaching_attitude = Number(score.value.teaching_attitude)
  score.value.teaching_level = Number(score.value.teaching_level)
  score.value.score_end = Number(score.value.score_end)
  score.value.teacher_morality = Number(score.value.teacher_morality)
  score.value.attendance_attitude = Number(score.value.attendance_attitude)
  // 检查评分是否在0-5之间
  if (
    score.value.teaching_attitude < 0 ||
    score.value.teaching_attitude > 5 ||
    score.value.teaching_level < 0 ||
    score.value.teaching_level > 5 ||
    score.value.score_end < 0 ||
    score.value.score_end > 5 ||
    score.value.teacher_morality < 0 ||
    score.value.teacher_morality > 5 ||
    score.value.attendance_attitude < 0 ||
    score.value.attendance_attitude > 5
  ) {
    ElMessage.error('评分必须在0-5之间')
    throw new Error('评分必须在0-5之间')
  }
}
</script>

<style></style>
