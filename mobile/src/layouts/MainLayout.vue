<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>ПВЗ Доставка</q-toolbar-title>
        <!-- Кнопка выхода, показываем только если залогинен -->
        <q-btn v-if="store.user" flat round icon="logout" @click="logout" />
      </q-toolbar>
    </q-header>

    <q-footer v-if="store.user" bordered class="bg-white text-primary">
      <q-tabs no-caps active-color="primary" indicator-color="transparent" class="text-grey">
        <q-route-tab icon="list" label="Заказы" to="/" exact />
        <q-route-tab icon="add_circle" label="Создать" to="/add" />
      </q-tabs>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useOrderStore } from 'src/stores/order-store'
import { useRouter } from 'vue-router'

const store = useOrderStore()
const router = useRouter()

const logout = () => {
  store.logout()
  router.push('/login')
}
</script>
