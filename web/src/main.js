import App from './App.vue'
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import { createApp } from 'vue';
import ElementPlus from 'element-plus'
// import InfiniteScroll from 'element-plus';
import 'element-plus/dist/index.css'
import router from './router';

const app = createApp(App);
app.use(ElementPlus);
// app.use(InfiniteScroll);
app.use(router).mount('#app');

