import '../node_modules/element-plus/theme-chalk/el-var.css'
import './assets/base.css'
import "element-plus/theme-chalk/el-message.css";
import "element-plus/theme-chalk/el-message-box.css"; 

import { createApp } from 'vue'
import App from './App.vue'

let app = createApp(App)

app.mount('#app')
