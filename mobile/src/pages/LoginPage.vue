<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const tab = ref('email')
const loading = ref(false)
const showPassword = ref(false)

const emailForm = ref({
  email: '',
  password: ''
})

const onLoginEmail = async () => {
  loading.value = true
  try {
    const success = await authStore.login(emailForm.value.email, emailForm.value.password)
    if (success) {
      $q.notify({
        color: 'positive',
        message: 'Успешный вход!',
        position: 'top',
        icon: 'check_circle'
      })
      router.push('/orders')
    } else {
      $q.notify({
        color: 'negative',
        message: 'Неверный email или пароль',
        position: 'top',
        icon: 'error'
      })
    }
  } finally {
    loading.value = false
  }
}

const onLoginTelegram = async () => {
  $q.notify({
    color: 'info',
    message: 'Откройте Telegram бота для входа',
    position: 'top'
  })
  // Здесь будет логика с ботом
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

        <q-tabs
          v-model="tab"
          dense
          class="text-teal"
          active-color="primary"
          indicator-color="primary"
          align="justify"
        >
          <q-tab name="email" label="📧 Email" />
          <q-tab name="telegram" label="✈️ Telegram" />
        </q-tabs>

        <!-- Email Tab -->
        <q-tab-panels v-model="tab" animated class="q-mt-md">
          <q-tab-panel name="email">
            <q-form @submit.prevent="onLoginEmail" class="q-gutter-md">
              <q-input
                v-model="emailForm.email"
                label="Email"
                type="email"
                outlined
                dense
                prefix-icon="mail"
                :rules="[
                  val => val && val.length > 0 || 'Введите email',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Некорректный email'
                ]"
                class="animated-input"
              />

              <q-input
                v-model="emailForm.password"
                :type="showPassword ? 'text' : 'password'"
                label="Пароль"
                outlined
                dense
                prefix-icon="lock"
                :rules="[val => val && val.length > 0 || 'Введите пароль']"
                class="animated-input"
              >
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer hover-icon"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>

              <q-btn
                type="submit"
                label="Войти"
                color="primary"
                class="full-width"
                size="lg"
                :loading="loading"
                unelevated
                rounded
              />
            </q-form>
          </q-tab-panel>

          <!-- Telegram Tab -->
          <q-tab-panel name="telegram">
            <div class="telegram-section q-gutter-md">
              <div class="telegram-icon">✈️</div>
              <p class="text-center text-grey-7">
                Откройте нашего Telegram бота для быстрого входа
              </p>
              <q-btn
                label="Открыть бот @pvz_bot"
                color="info"
                class="full-width"
                size="lg"
                unelevated
                rounded
                icon="open_in_new"
                @click="onLoginTelegram"
              />
              <p class="text-center text-caption text-grey-6">
                Вас автоматически перенаправит в приложение после входа
              </p>
            </div>
          </q-tab-panel>
        </q-tab-panels>

        <div class="q-mt-lg register-section">
          <p class="text-center text-grey-7">
            Нет аккаунта?
            <q-btn
              label="Создать"
              flat
              color="primary"
              size="sm"
              @click="goToRegister"
              class="q-ml-xs"
            />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  font-size: 48px;
  margin-bottom: 15px;
  animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

h4 {
  margin: 0 0 5px 0;
  color: #333;
  font-weight: 600;
}

.subtitle {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.animated-input {
  transition: all 0.3s ease;
}

.hover-icon {
  transition: color 0.2s;
}

.hover-icon:hover {
  color: #667eea;
}

.telegram-section {
  padding: 20px;
  text-align: center;
}

.telegram-icon {
  font-size: 64px;
  margin-bottom: 15px;
}

.register-section {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.register-section p {
  margin: 0;
}

@media (max-width: 600px) {
  .login-card {
    padding: 30px 20px;
  }

  .logo-section {
    margin-bottom: 20px;
  }

  .logo {
    font-size: 40px;
  }

  h4 {
    font-size: 22px;
  }
}
</style>