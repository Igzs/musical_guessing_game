import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import UserProfile from '@/components/UserProfile.vue';import store from '@/store'; // If using Vuex

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage, name: 'HomePage' },
    {
      path: '/user_profile',
      name: 'UserProfile',
      component: UserProfile,
      meta: { requiresAuth: true }, // Custom flag to indicate auth is required
    },
  ],
});


router.beforeEach(async (to, from, next) => {
  await store.dispatch('checkAuthState');
  if (to.matched.some(record => record.meta.requiresAuth) && !store.getters.isAuthenticated) {
    next({ name: 'HomePage', query: { authRequired: 'true' } });
  } else {
    next();
  }
});

export default router;
