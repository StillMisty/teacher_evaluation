
<template>
    <main>
        <el-tabs type="border-card" style="width: 100%;">
            <el-tab-pane label="大众点评" style="height: 250px;display: flex;flex-direction: column;justify-content: center;align-items: stretch;">
                <template v-for="teacherGrade in Props.teacherGrades" :key="teacherGrade.name">
                <div class="TeacherGeade">                    
                    <p class="TeacherGradeName"><el-text>{{ teacherGrade.name }} :</el-text></p>
                    <el-rate
                    v-model="teacherGrade.value" disabled show-score>
                    </el-rate>
                </div>
                </template>
            </el-tab-pane>
            <el-tab-pane label="个人打分" style="height: 250px;">
                <div style="display: flex;flex-direction: column;justify-content: space-between;height: 100%;">
                <p><el-text type="primary" size="large">对于这位老师,你的评价是: </el-text></p>
                <div>
                    <template v-for="grade in PersonalGrade" :key="grade.key">
                        <div class="TeacherGeade">                    
                            <p class="TeacherGradeName"><el-text>{{ grade.name }}   :</el-text></p>
                            <el-rate
                            v-model="grade.value" show-score clearable :disabled="isPostScores">
                            </el-rate>
                        </div>
                    </template>
                </div>
                <div class="commit" @click="postScores">
                    <el-button type="primary" :plain="true" :disabled="isPostScores">提交</el-button>
                </div> 
                </div>
            </el-tab-pane>
            <el-tab-pane label="发表评论" style="height: 250px;">
                <div style="display: flex;flex-direction: column;justify-content: space-between;height: 100%;">
                    <el-input
                    v-model="comment"
                    minlength="5"
                    maxlength="300"
                    placeholder="发出你的声音"
                    show-word-limit
                    type="textarea"
                    resize="none"
                    :autosize="{ minRows: 9, maxRows: 9 }"
                />
                <div class="commit" @click="postComment">
                    <el-button type="primary" plain>提交</el-button>
                </div> 
                </div>
            </el-tab-pane>
        </el-tabs>
    </main>


</template>

<script setup>

import { ref, defineProps} from 'vue'
import { ElMessage } from 'element-plus'

const Props = defineProps({
    teacherGrades: {
        type: Array,
        defineProps: []
    },
    teacherId: {
        type: Number,
        default: 0
    },
    baseUrl: {
        type: String,
        default: ''
    },
    updataComments: {
        type: Function,
        default: () => {}
    }
})

const PersonalGrade = ref([
    {
        name:"教学态度",
        value: 0,
    },
    {
        name:"教学水平",
        value: 0,
    },
    {
        name:"期末捞人",
        value: 0,
    },
    {
        name:"教师人品",
        value: 0,
    },
    {
        name:"考勤宽松",
        value: 0,
    }
])
const comment = ref('')

const isPostScores = ref(false)

function postScores(){

    fetch(`${Props.baseUrl}/api/teacher/post_teacher_score`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: Props.teacherId,
            teaching_attitude: PersonalGrade.value[0].value,
            teaching_level: PersonalGrade.value[1].value,
            score_end: PersonalGrade.value[2].value,
            teacher_morality: PersonalGrade.value[3].value,
            attendance_attitude: PersonalGrade.value[4].value
        })
    })
    .then(res => res.json())
    .then(res => {
        if (res.code === 200) {
            ElMessage({
                message: '提交成功',
                type: 'success',
            })

            isPostScores.value = true
            
        }else if (res.code === 403) {
            ElMessage({
                message: 'IP不在允许内，请连接校园网后重试',
                type: 'error',
            })
        }
    })
}

function postComment(){
    if (comment.value.length < 5) {
        ElMessage({
            message: '评论字数不得少于5个字',
            type: 'error',
        })
        return
    }


    fetch(`${Props.baseUrl}/api/teacher/post_teacher_comment`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: Props.teacherId,
            content: comment.value
        })
    })  
    .then(res => res.json())
    .then(res => {
        if (res.code === 200) {
            ElMessage({
                message: '提交成功',
                type: 'success',
            })

            Props.updataComments({
                id: Props.teacherId,
                content: comment.value,
                create_time: new Date().toLocaleString()
            })
            comment.value = ''
        }else if (res.code === 403) {
            ElMessage({
                message: 'IP不在允许内，请连接校园网后重试',
                type: 'error',
            })
        }
    })
}

</script>


<style scoped>

main {
    width: 100%;
}

.TeacherGeade {
    display: flex;
    align-items: center;
    justify-content: center;
}

.TeacherGeade .TeacherGradeName {
    padding-right: 16px;
}

.commit {
    display: flex;
    justify-content: end;
    width: 100%;
}
</style>