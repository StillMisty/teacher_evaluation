
<template>
    <section :style="{'height': homeHeight}">
        <h1 style="margin-bottom: 20px;cursor: default;user-select: none;" v-if="!Props.isSearch">
            <el-image :src="Props.logoUrl" @error="logo_show = !logo_show" v-if="logo_show" style="height: 72px;width: 72px;vertical-align: bottom;" class="logo"/>
            <el-text type="primary" style="font-size: 36px;">教师评价</el-text>
        </h1>
        <div class="SearchBar">
            <el-autocomplete
            v-model="queryString"
            :fetch-suggestions="querySearch"
            clearable
            placeholder="搜索教师"
            value-key="name"
            @select="handleSelect"
            highlight-first-item
            style="width: 90%;max-width: 600px;"
          />
        </div>

        <p style="min-height: 200px;" v-if="!Props.isSearch"><el-text type="info"></el-text></p>
    </section>
</template>

<script setup>
import { ref,defineProps, watch } from 'vue'
import { ElMessage } from 'element-plus'

const Props = defineProps({
    logoUrl: {
        type: String,
        default: ''
    }, 
    baseUrl: {
        type: String,
        default: ''
    },
    searchTeacher: {
        type: Function,
        default: () => {}
    },
    isSearch: {
        type: Boolean,
        default: false
    }
})

const logo_show = ref(true)

const queryString = ref('')

let timeout
const querySearch = (queryString, cb) => {
    const results = queryString ? getSuggestions(queryString) : []
    clearTimeout(timeout)
    timeout = setTimeout(() => {
        cb(results)
    }, 200 * Math.random())
}

const getSuggestions = (queryString) => {
    const result = []
    fetch(`${Props.baseUrl}/api/teacher/get_teacher_list?teacher_query=${encodeURI(queryString)}`)
        .then((res) => res.json())
        .then((res) => {
            if (res.code == 200) {
                if (res.data.length == 0) {
                    result.push({
                        id: -1,
                        name: '暂无结果'
                    })
                }else{
                    result.push(...res.data)
                }
            }
        }).catch((err) => {
            console.log(err)
    })
    return result
}

const handleSelect = (item) => {
    if (item.id === -1) {
        ElMessage({
            message: '暂无结果',
            type: 'warning'
        })
        queryString.value = ''
        return
    }
    Props.searchTeacher(item.id)
}

const homeHeight = ref('100vh')
watch(()=>Props.isSearch, (newVal) => {
    if (newVal) {
        homeHeight.value = 'auto'
        queryString.value = ''
    }
})
</script>

<style scoped>

section {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    width: 100%;
    transition: all 2s;
}

.SearchBar{
    margin: 36px 0 12px 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 2s;
}

.SearchBar:deep(.el-input__inner) {
    height: 36px;
}

.logo {
    animation: 5s linear infinite rotate;
}

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>