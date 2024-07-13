<template>
  <div
    class="flex min-h-screen w-full justify-center items-center bg-[linear-gradient(to_bottom,_#e6f7ff,_#ffffff)]"
  >
    <el-form
      :model="loginForm"
      status-icon
      :rules="loginRules"
      ref="loginFormRef"
      label-width="80px"
      class="w-96 p-8 mb-16 bg-opacity-20 backdrop-filter backdrop-blur-md rounded-md shadow-md"
    >
      <el-form-item
        ><el-text class="my-8" type="primary" size="large">教师评价系统后台</el-text></el-form-item
      >

      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="loginForm.username"
          type="text"
          placeholder="请输入用户名"
          autocomplete="off"
        />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="请输入密码"
          autocomplete="off"
        />
      </el-form-item>
      <el-form-item class="mt-8">
        <el-button type="primary" @click="submitForm">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { Token } from '@/themes/Token'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['loginSuccess'])
interface LoginForm {
  username: string
  password: string
}

const loginForm = ref<LoginForm>({
  username: '',
  password: ''
})

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const submitForm = () => {
  if (loginForm.value.username === '' || loginForm.value.password === '') {
    ElMessage.warning('用户名或密码不能为空')
    return
  }
  fetch('api/token', {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      grant_type: 'password',
      username: loginForm.value.username,
      password: loginForm.value.password,
      scope: '',
      client_id: 'string',
      client_secret: 'string'
    })
  })
    .then((res) => {
      if (!res.ok) {
        ElMessage.error('账号或密码错误')
        throw new Error('response was not ok')
      }
      return res.json()
    })
    .then((data: Token) => {
      sessionStorage.setItem('access_token', data.access_token)
      sessionStorage.setItem('token_type', data.token_type)
      sessionStorage.setItem('username', loginForm.value.username)
      emit('loginSuccess')
    })
}
</script>

<style></style>
