import { createRouter, createWebHistory } from 'vue-router';
import Chat from '@/components/Chat.vue';
import UserAuth from '@/components/UserAuth.vue';
import LandingPage from '@/components/LandingPage.vue';
import NotFoundPage from '@/components/NotFoundPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: LandingPage
    },
    {
      path: '/chats',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/auth',
      name: 'UserAuth',
      component: UserAuth
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFoundPage
    }
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken') !== null;

  // 1. If trying to access Chat without a token, redirect to Auth
  if (to.path === '/chats' && !isAuthenticated) {
    next('/auth');
  }
  // 2. If already authenticated and trying to go to Auth, skip to Chat
  else if (to.path === '/auth' && isAuthenticated) {
    next('/chats');
  }
  // 3. Otherwise (Landing page or authorized access), proceed as usual
  else {
    next();
  }
});

export default router;