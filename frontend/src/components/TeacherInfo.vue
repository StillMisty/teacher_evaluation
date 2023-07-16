
<template>
    <section class="info" style="width: 100%;">
        <el-tabs type="border-card" style="min-width: 100%;max-width: 100%;">
            <template v-for="teacherInfo in Props.teacherInfos" :key="teacherInfo.name">
                <el-tab-pane :label="teacherInfo.name" v-html="teacherInfo.content" style="color: var(--el-text-color-primary);min-height: 160px;max-height: 320px;min-width: 100%;overflow-y: auto;"></el-tab-pane>
            </template>
        </el-tabs>
    </section>
</template>

<script setup>
import { defineProps } from 'vue'

const Props = defineProps({
    teacherInfos : {
        type: Object,
        default: () => {}
    }
})

</script>

<style scoped>


</style>