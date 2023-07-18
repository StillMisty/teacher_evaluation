
<template>
  <div class="main">
  <HomePage :logo-url="logoUrl" :base-url="baseUrl" :search-teacher="searchTeacher"></HomePage>
  <section class="AfterSearch" v-if="search">  
    <TeacherBrief v-bind="teacher"></TeacherBrief>
    <TeacherInfo :teacher-infos="teacherInfos"></TeacherInfo>
    <TeacherGrade :teacher-grades="teacherGrades" :teacher-id="teacher.id" :base-url="baseUrl" :updata-comments="undataComments"></TeacherGrade>
    <TeacherComment :comments="comments"></TeacherComment>
  </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HomePage from './components/HomePage.vue'
import TeacherInfo from './components/TeacherInfo.vue';
import TeacherBrief from './components/TeacherBrief.vue'
import TeacherGrade from './components/TeacherGrade.vue'
import TeacherComment from './components/TeacherComment.vue';

let baseUrl = window.location.origin

// 是否搜索过
const search = ref(false)

const logoUrl = ref(`${baseUrl}/logo.png`)

const teacher = ref({})
const teacherGrades = ref([])
const teacherInfos = ref([])
const comments = ref([])

function searchTeacher(teacher_id) {

  fetch(`${baseUrl}/api/teacher/get_teacher_info?teacher_id=${teacher_id}`)
  .then((res) => res.json())
  .then((res) => {
    Object.keys(res.data).forEach((key) => {
      teacher.value[key] = res.data[key]
    });
    if (teacher.value.researchFields != ''){
      teacher.value.researchFields = teacher.value.researchFields.slice(2, -2).replace(/"/g,' ')
    }
    teacher.value.photo = `${baseUrl}/${teacher.value.photo}`
  })


  fetch(`${baseUrl}/api/teacher/id_teacher_career?teacher_id=${teacher_id}`)
    .then((res) => res.json())
    .then((res) => {
      teacherInfos.value = Object.assign({}, res.data.career)
    })

  fetch(`${baseUrl}/api/teacher/id_teacher_evaluate?teacher_id=${teacher_id}`)
    .then((res) => res.json())
    .then((res) => {
      teacherGrades.value = []
      for (let key in res.data.score){
        teacherGrades.value.push({
            name: key,
            value: res.data.score[key]
        })
    }
  }
  )
  fetch(`${baseUrl}/api/teacher/id_teacher_allcomment?teacher_id=${teacher_id}`)
    .then((res) => res.json())
    .then((res) => {
      comments.value = []
      for (let comment of res.data.comments){
        let date = new Date(comment.create_time)
        comment.create_time = date.toLocaleString()
        comments.value.push(comment)
      }
  })

  // 销毁组件
  search.value = false
  setTimeout(() => {
    search.value = true
  }, 0);
}

function undataComments(comment) {
  comments.value.unshift(comment)
}


</script>

<style scoped>
.main {
  background-color: var(--el-color-primary-light-9);
}
.AfterSearch {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100vw;
  padding: 2%;
  border: var(--el-border);
}
</style>
