<template>
  <el-card>
    <el-button type="primary" :loading="isLoading" @click="updateScore"> 更新教师评分 </el-button>
    <el-text>根据以有评分，根据时间序列权重更新教师评分</el-text>
  </el-card>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
const isLoading = ref(false)

const updateScore = () => {
  isLoading.value = true
  fetch('api/admin/teacher/evaluate/update', {
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
