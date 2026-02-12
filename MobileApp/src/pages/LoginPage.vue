<template>
  <q-page class="flex flex-center bg-grey-1">
    <q-card flat bordered style="width: 90%; max-width: 400px">
      <q-card-section class="text-center">
        <div class="text-h5 text-weight-bold">Вход в ПВЗ</div>
        <div class="text-caption text-grey-7">Используйте ваш ID из Telegram бота</div>
      </q-card-section>

      <q-card-section class="q-gutter-y-md">
        <q-input v-model="loginForm.user_id" label="Ваш Telegram ID" outlined mask="##########" />
        <q-input v-model="loginForm.code" label="Код подтверждения из бота" outlined />
        
        <q-btn 
          color="primary" 
          label="Войти" 
          class="full-width" 
          size="lg" 
          :loading="loading"
          @click="handleLogin" 
        />
      </q-card-section>

      <q-card-section class="text-center">
        <q-btn flat color="secondary" label="Как узнать мой ID?" size="sm" @click="showHelp = true" />
      </q-card-section>
    </q-card>

    <!-- Подсказка -->
    <q-dialog v-model="showHelp">
      <q-card>
        <q-card-section>
          <div class="text-h6">Где взять данные?</div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          Напишите нашему боту команду <b>/my_id</b>. Он пришлет ваш ID и код для входа в приложение.
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Понял" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from 'src/stores/order-store'

const router = useRouter()
const store = useOrderStore()

const loading = ref(false)
const showHelp = ref(false)
const loginForm = ref({ user_id: '', code: '' })

const handleLogin = async () => {
  loading.value = true
  // Здесь будет вызов DRF: await api.post('/auth/login/', loginForm.value)
  setTimeout(() => {
    loading.value = false
    // Сохраняем ID в стор (как будто авторизованы)
    store.setUser(loginForm.value.user_id)
    router.push('/')
  }, 1000)
}
</script>
