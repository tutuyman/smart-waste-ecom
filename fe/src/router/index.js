import { createRouter, createWebHistory } from 'vue-router';
import Cookies from 'js-cookie'; // Untuk membaca token dari cookies
import Login from '../views/Login.vue';
import ProductView from '@/views/ProductView.vue';
import BidView from '@/views/BidView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
      meta: { layout: 'auth', requiresAuth: false }, // Tidak memerlukan autentikasi
    },
    {
      path: '/product',
      name: 'Product',
      component: ProductView,
      meta: { requiresAuth: true }, // Hanya dapat diakses jika login
    },
    {
      path: '/bid',
      name: 'Bid',
      component: BidView,
      meta: { requiresAuth: true }, // Hanya dapat diakses jika login
    },
  ],
});

// Tambahkan navigation guard
router.beforeEach((to, from, next) => {
  const token = Cookies.get('token'); // Ambil token dari cookies

  // Jika mencoba akses halaman login dan token ada, redirect ke /product
  if (to.name === 'Login' && token) {
    next({ path: '/product' });
  } 
  // Jika halaman memerlukan autentikasi tetapi token tidak ada, redirect ke login
  else if (to.meta.requiresAuth && !token) {
    next({ path: '/' });
  } 
  // Izinkan akses ke halaman
  else {
    next();
  }
});

export default router;