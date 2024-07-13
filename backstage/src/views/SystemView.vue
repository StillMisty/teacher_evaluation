<template>
  <div class="flex flex-col h-full p-0">
    <div>
      <el-card v-loading="loading">
        <div>
          <el-row>
            <el-col :span="8">
              <el-card class="h-full flex flex-col justify-center">
                <p>操作系统: {{ systemInfo.system }}</p>
                <p>处理器架构: {{ systemInfo.machine }}</p>
                <p>CPU: {{ systemInfo.cpu }}</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <p>总内存: {{ systemInfo.memory_total }} GB</p>
                <p>可用内存: {{ systemInfo.memory_available }} GB</p>
                <el-progress
                  type="circle"
                  :percentage="
                    ((systemInfo.memory_available / systemInfo.memory_total) * 100).toFixed(2)
                  "
                />
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <p>磁盘总空间: {{ systemInfo.disk_total }} GB</p>
                <p>磁盘可用空间: {{ systemInfo.disk_used }} GB</p>
                <el-progress
                  type="circle"
                  :percentage="((systemInfo.disk_used / systemInfo.disk_total) * 100).toFixed(2)"
                />
              </el-card>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-card>
                <p>CPU使用率: {{ systemInfo.cpu_percent.toFixed(2) }}%</p>
                <el-progress :percentage="systemInfo.cpu_percent" />
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { SystemInfo } from '@/themes/SystemInfo'
import type { Response } from '@/themes/Response'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
const loading = ref(true)
const systemInfo = ref<SystemInfo>({
  system: '',
  machine: '',
  cpu: '',
  cpu_percent: 0.0,
  memory_total: 0,
  memory_available: 0,
  disk_total: 0,
  disk_used: 0
})

const fetchData = () => {
  fetch('api/admin/system/info', {
    method: 'GET',
    headers: {
      Authorization:
        sessionStorage.getItem('token_type') + ' ' + sessionStorage.getItem('access_token')
    }
  })
    .then((res) => res.json())
    .then((res: Response) => {
      if (res.code === 200) {
        loading.value = false
        systemInfo.value = res.data
      } else {
        ElMessage.error(res.message)
      }
    })
}
fetchData()
setInterval(fetchData, 5000)
</script>

<style></style>
