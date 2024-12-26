import { createRouter, createWebHashHistory } from 'vue-router';

const HomePage = () => import('../views/HomePage.vue')
const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
