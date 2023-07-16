
<template>
    <section class="brief">
        <div class="teacher_photo">
            <el-image 
            :src="Props.photo" 
            fit="cover"  
            alt="教师照片" 
            class="photo"
            placeholder="头像加载ing"
            error="头像加载失败"
            >
            </el-image>
        </div>
        <div class="teacher_brief">
            <p><el-text type="primary" style="font-size: var(--el-font-size-extra-large);">{{ Props.name }}</el-text></p>
            <div>
                <p><el-text type="info">{{ Props.academicDegree }} {{ Props.academicTitle }}</el-text></p>
                <p><el-text type="info">{{ Props.groupname }}</el-text></p>
            </div>
            <div>
                <p v-if="Props.email != ''"><el-text>Email：{{ Props.email }}</el-text></p>
                <p v-if="Props.phone != ''"><el-text>Phone：{{ Props.phone }}</el-text></p>
            </div>
            <div>
                <p v-if="Props.researchFields != ''"><el-text type="info">研究方向：{{ Props.researchFields }}</el-text></p>
                <p v-if="Props.subject != ''"><el-text type="info">所属学科：{{ Props.subject }}</el-text></p>
            </div>
        </div>
    </section>
</template>

<script setup>
import { defineProps} from 'vue'

const Props = defineProps({
    name: {
        type: String,
        default: ''
    },
    academicDegree: {
        type: String,
        default: ''
    },
    academicTitle: {
        type: String,
        default: ''
    },
    groupname: {
        type: String,
        default: ''
    },
    email: {
        type: String,
        default: ''
    },
    phone: {
        type: String,
        default: ''
    },
    photo: {
        type: String,
        default: ''
    },
    researchFields: {
        type: String,
        default: ''
    },
    subject: {
        type: String,
        default: ''
    },
})

</script>

<style scoped>

.brief {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    height: 160px;
    width: 100%;
    background-color: var(--el-fill-color-light);
    border: var(--el-border);
    border-top-left-radius: var(--el-border-radius-base);
    border-top-right-radius: var(--el-border-radius-base);
    overflow: hidden;
}

.teacher_photo {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    flex: 1;
    height: 100%;
}

.teacher_photo .photo {
    height: 100%;
    width: auto;
}

.teacher_brief {
    flex: 2;
    padding-left: 16px;
}



</style>