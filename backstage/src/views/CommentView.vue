<template>
  <div class="flex flex-col h-full p-0">
    <div>
      <el-button type="primary" @click="dialogFormVisible = true">添加评论</el-button>
      <el-dialog v-model="dialogFormVisible" title="添加评论" width="800">
        <el-form>
          <el-form-item label="教师ID">
            <el-input v-model="commentInfo.teacher_id" type="number"></el-input>
          </el-form-item>
          <el-form-item label="评论内容">
            <el-input
              v-model="commentInfo.content"
              minlength="5"
              maxlength="300"
              type="text"
            ></el-input>
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
    <el-table :data="data" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="teacher_id" label="教师ID"></el-table-column>
      <el-table-column prop="content" label="评论内容"></el-table-column>
      <el-table-column prop="is_delete" label="是否软删除">
        <template #default="{ row }">
          <el-tag v-if="row.is_delete === false" type="success">否</el-tag>
          <el-tag v-else type="danger">是</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" plain @click="handleEdit(scope.row.id)">编 辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog title="编辑评论" v-model="dialogTableVisible" width="800px">
    <el-form>
      <el-form-item label="教师ID">
        <el-input v-model="commentInfo.teacher_id" type="number" disabled></el-input>
      </el-form-item>
      <el-form-item label="评论内容">
        <el-input
          v-model="commentInfo.content"
          minlength="5"
          maxlength="300"
          type="text"
        ></el-input>
      </el-form-item>
      <el-form-item label="是否软删除">
        <el-radio-group v-model="commentInfo.is_delete">
          <el-radio :label="false" checked>否</el-radio>
          <el-radio :label="true">是</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button @click="dialogTableVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSave">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, type Ref } from 'vue'
import type { Response } from '@/themes/Response'
import type { Comment } from '@/themes/Comment'
import { ElMessage } from 'element-plus'

const dialogTableVisible = ref(false)
const dialogFormVisible = ref(false)
const data: Ref<Comment[]> = ref([])
const commentInfo = ref<Comment>({
  id: 0,
  teacher_id: 0,
  content: '',
  is_delete: false
})
const fetchData = () => {
  fetch('/api/admin/teacher/comment/all', {
    method: 'GET',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token')
    }
  })
    .then((res) => res.json())
    .then((res: Response) => {
      console.log(res)
      // 解包赋值，去除不用的属性
      data.value = res.data.map(
        (item: { create_time: any; id: any; teacher_id: any; content: any; is_delete: any }) => ({
          id: item.id,
          teacher_id: item.teacher_id,
          content: item.content,
          is_delete: item.is_delete
        })
      )
      console.log(data.value)
    })
}
fetchData()

const handleEdit = (id: number) => {
  console.log(id)
  dialogTableVisible.value = true
  commentInfo.value = Object.assign(
    {},
    data.value.find((item) => item.id === id)
  )
}

const handleAdd = () => {
  console.log(JSON.stringify(commentInfo.value))
  if (commentInfo.value.teacher_id === 0) {
    ElMessage.warning('教师ID不能为空')
    return
  }
  if (commentInfo.value.content.length < 5) {
    ElMessage.warning('评论内容不能少于5个字符')
    return
  }
  if (commentInfo.value.content.length > 300) {
    ElMessage.warning('评论内容不能多于300个字符')
    return
  }
  fetch('/api/admin/teacher/comment', {
    method: 'POST',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: Number(commentInfo.value.teacher_id),
      content: commentInfo.value.content
    })
  })
    .then((res) => res.json())
    .then((res: Response) => {
      console.log(res)
      if (res.code === 200) {
        fetchData()
        dialogFormVisible.value = false
        ElMessage.success('添加成功')
      }
      if (res.code === 404) {
        ElMessage.error('教师ID不存在')
      }
    })
}

const handleSave = () => {
  console.log(JSON.stringify(commentInfo.value))
  if (commentInfo.value.teacher_id === 0) {
    ElMessage.warning('教师ID不能为空')
    return
  }
  if (commentInfo.value.content.length < 5) {
    ElMessage.warning('评论内容不能少于5个字符')
    return
  }
  if (commentInfo.value.content.length > 300) {
    ElMessage.warning('评论内容不能多于300个字符')
    return
  }
  fetch(`/api/admin/teacher/comment/${commentInfo.value.id}`, {
    method: 'PUT',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(commentInfo.value)
  })
    .then((res) => res.json())
    .then((res: Response) => {
      console.log(res)
      if (res.code === 200) {
        fetchData()
        ElMessage.success('修改成功')
        dialogTableVisible.value = false
      }
    })
}
</script>
