<template>
  <LoginBox v-if="!isLogin" @loginSuccess="isLogin = true" />

  <div v-else class="min-h-screen min-w-full">
    <el-container>
      <el-aside>
        <side-bar />
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import SideBar from './components/SideBar.vue'
import LoginBox from './components/LoginBox.vue'
import { ref } from 'vue'

const isLogin = ref(false)
</script>
