<template>
  <ul class="infinite-list" style="overflow: auto">
    <li v-for="comment in Props.comments" :key="comment.id" class="infinite-list-item">
      <div>
        <el-text>
          {{ comment.content }}
        </el-text>
      </div>
      <div class="time"><el-text type="info" size="small">
        {{ comment.create_time }}
      </el-text></div>
    </li>
  </ul>
</template>

<script setup>
import { defineProps } from 'vue'


const Props = defineProps({
  comments : {
      type: Array,
      default: () => []
  }
})

</script>

<style>
.infinite-list {
  max-height: 99vh;
  width: 100%;
  list-style: none;
}

.infinite-list .infinite-list-item {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-direction: column;
  background: var(--el-color-white);
  box-shadow: var(--el-transition-box-shadow);
  padding: 10px;
  margin-top: 6px;
  border-radius: var(--el-border-radius-base);
  border: var(--el-border);
}

.time {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>