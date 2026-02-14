<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth-store'
import { Notify } from 'quasar'

const router = useRouter()
const authStore = useAuthStore()

const tab = ref('email')
const loading = ref(false)
const showPassword = ref(false)

const emailForm = ref({
  email: '',
  password: '',
})

const verificationForm = ref({
  code: '',
})

const userForVerification = ref(null)
const showVerification = ref(false)



const onLoginEmail = async () => {
  loading.value = true
  try {
    const response = await authStore.login(emailForm.value.email, emailForm.value.password)

    if (response.status === 'success') {
      Notify.create({ color: 'positive', message: 'Успешный вход!', position: 'top', icon: 'check_circle' })
      router.push('/')
    } 
    else if (response.status === 'verification_needed') {
      showVerification.value = true
      userForVerification.value = { id: response.user_id, email: response.email }
      Notify.create({ color: 'info', message: response.message, position: 'top' })
    } 
    else {
      Notify.create({ color: 'negative', message: response.error || 'Ошибка входа', position: 'top', icon: 'error' })
    }
  } finally {
    loading.value = false
  }
}
const onVerifyEmail = async () => {
  if (!userForVerification.value) return
  loading.value = true
  try {
    const success = await authStore.verifyEmail(userForVerification.value.id, verificationForm.value.code)
    if (success) {
      Notify.create({ color: 'positive', message: 'Email подтверждён!', position: 'top', icon: 'check_circle' })
      router.push('/')
    } else {
      Notify.create({ color: 'negative', message: 'Неверный код', position: 'top', icon: 'error' })
    }
  } catch (err) {
    console.error(err)
    Notify.create({ color: 'negative', message: 'Ошибка подтверждения', position: 'top', icon: 'error' })
  } finally {
    loading.value = false
  }
}

const onLoginTelegram = async () => {
  Notify.create({ color: 'info', message: 'Откройте Telegram бота для входа', position: 'top' })
  // Логика с ботом
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="logo-section">
          <div class="logo">🛍️</div>
          <h4>PVZ Bot</h4>
          <p class="subtitle">Управление заказами</p>
        </div>

        <q-tabs v-model="tab" dense class="text-teal" active-color="primary" indicator-color="primary" align="justify">
          <q-tab name="email" label="📧 Email" />
          <q-tab name="telegram" label="✈️ Telegram" />
        </q-tabs>

        <q-tab-panels v-model="tab" animated class="q-mt-md">
          <!-- Email Tab -->
          <q-tab-panel name="email">
            <q-form v-if="!showVerification" @submit.prevent="onLoginEmail" class="q-gutter-md">
              <q-input v-model="emailForm.email" label="Email" type="email" outlined dense prefix-icon="mail" 
                :rules="[val => val && val.length > 0 || 'Введите email', val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Некорректный email']"/>
              <q-input v-model="emailForm.password" :type="showPassword ? 'text' : 'password'" label="Пароль" outlined dense prefix-icon="lock"
                :rules="[val => val && val.length > 0 || 'Введите пароль']">
                <template v-slot:append>
                  <q-icon :name="showPassword ? 'visibility_off' : 'visibility'" class="cursor-pointer hover-icon" @click="showPassword = !showPassword"/>
                </template>
              </q-input>
              <q-btn type="submit" label="Войти" color="primary" class="full-width" size="lg" :loading="loading" unelevated rounded/>
            </q-form>

            <q-form v-else @submit.prevent="onVerifyEmail" class="q-gutter-md">
              <p class="text-center text-grey-7">Введите код, который мы отправили на {{ userForVerification.email }}</p>
              <q-input v-model="verificationForm.code" label="Код подтверждения" outlined dense prefix-icon="lock"
                :rules="[val => val && val.length === 6 || 'Введите 6-значный код']"/>
              <q-btn type="submit" label="Подтвердить" color="primary" class="full-width" size="lg" :loading="loading" unelevated rounded/>
            </q-form>
          </q-tab-panel>

          <!-- Telegram Tab -->
          <q-tab-panel name="telegram">
            <div class="telegram-section q-gutter-md">
              <div class="telegram-icon">✈️</div>
              <p class="text-center text-grey-7">Откройте нашего Telegram бота для быстрого входа</p>
              <q-btn label="Открыть бот @pvz_bot" color="info" class="full-width" size="lg" unelevated rounded icon="open_in_new" @click="onLoginTelegram"/>
              <p class="text-center text-caption text-grey-6">Вас автоматически перенаправит в приложение после входа</p>
            </div>
          </q-tab-panel>
        </q-tab-panels>

        <div class="q-mt-lg register-section">
          <p class="text-center text-grey-7">
            Нет аккаунта?
            <q-btn label="Создать" flat color="primary" size="sm" @click="goToRegister" class="q-ml-xs"/>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page { min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; padding: 20px;}
.login-container { width: 100%; max-width: 450px;}
.login-card { background: white; border-radius: 16px; padding: 40px 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: slideUp 0.5s ease-out; }
.logo-section { text-align: center; margin-bottom: 30px; }
.logo { font-size: 48px; margin-bottom: 15px; animation: bounce 0.6s ease-in-out; }
h4 { margin: 0 0 5px 0; color: #333; font-weight: 600; }
.subtitle { margin: 0; color: #999; font-size: 14px; }
.hover-icon { transition: color 0.2s; }
.hover-icon:hover { color: #667eea; }
.telegram-section { padding: 20px; text-align: center; }
.telegram-icon { font-size: 64px; margin-bottom: 15px; }
.register-section { border-top: 1px solid #eee; padding-top: 20px; }
.register-section p { margin: 0; }
</style>
