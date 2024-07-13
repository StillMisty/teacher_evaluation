<template>
  <el-card>
    <el-button type="primary" :loading="isLoading" @click="updateTeacher"> 更新教师信息 </el-button>
    <el-text>使用爬虫爬取江财官网教师信息，将爬取的信息保存到数据库中</el-text>
  </el-card>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
const isLoading = ref(false)
const updateTeacher = () => {
  isLoading.value = true
  fetch('api/admin/teacher/update', {
    method: 'POST',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token')
    }
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.code !== 200) {
        throw new Error(data.message)
      }
    })
    .catch((err) => {
      ElMessage.error(err.message)
    })
    .finally(() => {
      isLoading.value = false
    })
    .then(() => {
      isLoading.value = false
      ElMessage.success('更新成功')
    })
    .catch(() => {
      isLoading.value = false
      ElMessage.error('更新失败')
    })
}
</script>
