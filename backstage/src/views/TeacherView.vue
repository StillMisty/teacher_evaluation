<template>
  <div class="flex flex-col justify-between items-center h-full p-0">
    <el-table :data="teacherList" class="w-full">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column prop="phone" label="电话"></el-table-column>
      <el-table-column prop="photo" label="照片">
        <template #default="scope">
          <div>
            <el-image
              style="width: 100px; height: 100px"
              :src="scope.row.photo"
              fit="cover"
              error="无"
            />
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="academicDegree" label="学位"></el-table-column>
      <el-table-column prop="academicTitle" label="职称"></el-table-column>
      <el-table-column prop="deptName" label="学院"></el-table-column>
      <el-table-column prop="views" label="浏览量"></el-table-column>
      <el-table-column label="管理">
        <template #header>
          <el-autocomplete
            v-model="search"
            :fetch-suggestions="querySearch"
            placeholder="请输入姓名"
            @select="select"
            value-key="name"
            highlight-first-item="true"
          ></el-autocomplete>
        </template>
        <template #default="scope">
          <!-- 气泡框 -->
          <el-button type="primary" plain @click="handleEdit(scope.$index, scope.row)"
            >编 辑</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑 -->
    <el-dialog v-model="dialogTableVisible" title="编辑信息" width="800">
      <el-form>
        <el-form-item label="姓名">
          <el-input v-model="teacherInfo.name"></el-input>
        </el-form-item>

        <el-form-item label="邮箱">
          <el-input v-model="teacherInfo.email"></el-input>
        </el-form-item>

        <el-form-item label="电话">
          <el-input v-model="teacherInfo.phone"></el-input>
        </el-form-item>

        <el-form-item label="照片">
          <!-- <el-input v-model="teacherInfo.photo"></el-input> -->
          <el-upload
            :action="`/api/admin/teacher/photo?id=${teacherInfo.id}`"
            :headers="headers"
            method="POST"
            :on-success="handleSuccess"
            list-type="picture-card"
            :auto-upload="true"
            limit="1"
          >
            <el-image
              style="width: 100px; height: 100px"
              :src="teacherInfo.photo"
              fit="cover"
              error="无"
            />
          </el-upload>
        </el-form-item>

        <el-form-item label="学位">
          <el-input v-model="teacherInfo.academicDegree"></el-input>
        </el-form-item>

        <el-form-item label="职称">
          <el-input v-model="teacherInfo.academicTitle"></el-input>
        </el-form-item>

        <el-form-item label="学院">
          <el-input v-model="teacherInfo.deptName"></el-input>
        </el-form-item>

        <el-form-item label="浏览量">
          <el-input v-model="teacherInfo.views"></el-input>
        </el-form-item>

        <el-form-item label="办公地址">
          <el-input v-model="teacherInfo.officeAddr"></el-input>
        </el-form-item>

        <el-form-item label="研究领域">
          <el-input v-model="teacherInfo.researchFields"></el-input>
        </el-form-item>

        <el-form-item label="学科">
          <el-input v-model="teacherInfo.subject"></el-input>
        </el-form-item>

        <div class="w-full flex justify-end mb-8">
          <el-button @click="dialogTableVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleSave">确 定</el-button>
        </div>

        <el-form-item label="栏目信息">
          <el-form-item v-for="col in teacherInfo.columnInfo" :key="col.name">
            <br />
            <el-input v-model="col.name"></el-input>
            <div class="flex flex-col w-full">
              <el-input
                v-model="col.content"
                type="textarea"
                resize="vertical"
                class="w-full"
              ></el-input>
              <div v-html="col.content"></div>
            </div>
          </el-form-item>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-pagination
      class="mt-4"
      layout="prev, pager, next"
      :total="total"
      :page-size="size"
      :current-page="currentPage"
      @update:current-page="currentPage = $event"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import type { Response } from '@/themes/Response'
import type { Teacher, TeacherInfo, TeacherPer } from '@/themes/Teacher'
import { ElMessage } from 'element-plus'

const teacherList = ref<Teacher[]>([])
const total = ref(0)
const size = ref(12)
const currentPage = ref(1)
const headers = {
  Authorization: sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token')
}

const fetchData = () => {
  fetch(`/api/admin/teacher?page=${currentPage.value}&size=${size.value}`, {
    method: 'GET',
    headers
  })
    .then((res) => res.json())
    .then((res: Response) => {
      teacherList.value = res.data.teacher_list as Teacher[]
      total.value = res.data.total
      teacherList.value.forEach((teacher) => {
        teacher.photo = `${window.location.origin}/headimgs/${teacher.photo}`
      })
    })
}
fetchData()
// 监听 currentPage 的变化
watch(currentPage, fetchData)

const teacherInfo = ref<TeacherInfo>({
  id: 0,
  name: '',
  email: '',
  phone: '',
  photo: '',
  academicDegree: '',
  academicTitle: '',
  deptName: '',
  views: 0,
  officeAddr: '',
  researchFields: '',
  subject: '',
  columnInfo: []
})
const fetchTeacherInfo = (id: number) => {
  fetch(`/api/admin/teacher/${id}`, {
    method: 'GET',
    headers
  })
    .then((res) => res.json())
    .then((res: Response) => {
      teacherInfo.value = res.data as TeacherInfo
      teacherInfo.value.photo = `${window.location.origin}/headimgs/${teacherInfo.value.photo}`
    })
}
const saveTeacherInfo = () => {
  fetch(`/api/admin/teacher`, {
    method: 'PUT',
    headers: {
      ...headers,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(teacherInfo.value)
  })
    .then((res) => res.json())
    .then(() => {
      ElMessage.success('保存成功')
    })
    .catch(() => {
      ElMessage.error('保存失败')
    })
}
const dialogTableVisible = ref(false)
const handleEdit = (index: number, row: Teacher) => {
  dialogTableVisible.value = true
  console.log(index, row)
  fetchTeacherInfo(row.id)
}
const handleSave = () => {
  dialogTableVisible.value = false
  saveTeacherInfo()
  fetchData()
}

const handleSuccess = () => {
  ElMessage.success('上传成功')
}

const search = ref('')
const teacherPerList = ref<TeacherPer[]>([])
const searchTeacher = (name: string) => {
  fetch(`/api/admin/teacher/search?name=${name}`, {
    method: 'GET',
    headers
  })
    .then((res) => res.json())
    .then((res: Response) => {
      teacherPerList.value = res.data as TeacherPer[]
    })
}

let timeout: any
const querySearch = (queryString: string, cb: (arg0: TeacherPer[]) => void) => {
  if (timeout) {
    clearTimeout(timeout)
  }
  timeout = setTimeout(() => {
    searchTeacher(queryString)
    const results = queryString
      ? teacherPerList.value.filter((item) => filterMethod(queryString, item))
      : []
    cb(results)
  }, 300)
}

const filterMethod = (query: string, item: TeacherPer) => {
  return item.name.indexOf(query) > -1
}

const select = (item: TeacherPer) => {
  fetchTeacherInfo(item.id)
  dialogTableVisible.value = true
}
</script>
