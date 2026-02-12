const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      // Главная со списком заказов
      { path: '', component: () => import('pages/IndexPage.vue') },
      
      // Страница добавления нового заказа
      { path: 'add', component: () => import('pages/AddOrder.vue') },
      
      // Страница входа
      { path: 'login', component: () => import('pages/LoginPage.vue') }
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]



export default routes
