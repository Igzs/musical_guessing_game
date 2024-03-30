import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import UserProfile from '@/components/UserProfile.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/user_profile', component: UserProfile }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
