<template>
  <div>
    <el-menu class="min-h-screen fixed" default-active="/" :router="router">
      <el-menu-item index="/">
        <span>系统详情</span>
      </el-menu-item>
      <el-sub-menu>
        <template #title>
          <span>数据管理</span>
        </template>
        <el-menu-item index="/teacher">
          <span>教师管理</span>
        </el-menu-item>
        <el-menu-item index="/score">
          <span>评分管理</span>
        </el-menu-item>
        <el-menu-item index="/comment">
          <span>评论管理</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/script">
        <span>脚本管理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
import router from '@/router'
</script>

<style></style>
