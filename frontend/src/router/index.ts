import { createRouter, createWebHistory } from 'vue-router';
// import HomeView from '../views/HomeView.vue';
import Chat from '@/components/Chat.vue';
import UserAuth from '@/components/UserAuth.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView,
    // },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/auth',
      name: 'UserAuth',
      component: UserAuth
    }
  ],
})

router.beforeEach((to, from, next) => {
  if (sessionStorage.getItem('authToken') !== null || to.path === '/auth') {
    next()
  } else {
    next('/auth')
  }
})

export default router;
