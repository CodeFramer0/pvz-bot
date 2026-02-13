<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const step = ref('form') // form, verify
const loading = ref(false)
const showPassword = ref(false)
const useTelegram = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const registrationData = ref(null)

const verifyForm = ref({
  code: ''
})

const onRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    $q.notify({
      color: 'negative',
      message: 'Пароли не совпадают',
      position: 'top'
    })
    return
  }

  loading.value = true
  try {
    const data = await authStore.register(
      form.value.username,
      form.value.email,
      form.value.password,
      useTelegram.value ? 'your_telegram_id' : null
    )

    registrationData.value = data
    step.value = 'verify'

    $q.notify({
      color: 'info',
      message: 'Код подтверждения отправлен на вашу почту',
      position: 'top'
    })
  } catch (error) {
    $q.notify({
      color: 'negative',
      message: error.message,
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}

const onVerify = async () => {
  loading.value = true
  try {
    const success = await authStore.verifyEmail(
      registrationData.value.user_id,
      verifyForm.value.code
    )

    if (success) {
      $q.notify({
        color: 'positive',
        message: 'Email подтвержден! Добро пожаловать!',
        position: 'top',
        icon: 'check_circle'
      })
      router.push('/orders')
    } else {
      $q.notify({
        color: 'negative',
        message: 'Неверный код',
        position: 'top'
      })
    }
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}

const resendCode = async () => {
  $q.notify({
    color: 'info',
    message: 'Код отправлен повторно на почту',
    position: 'top'
  })
}
</script>

<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="logo-section">
          <div class="logo">🎉</div>
          <h4>Создать аккаунт</h4>
          <p class="subtitle">Присоединяйтесь к PVZ Bot</p>
        </div>

        <!-- Step 1: Registration Form -->
        <div v-if="step === 'form'">
          <q-form @submit.prevent="onRegister" class="q-gutter-md">
            <q-input
              v-model="form.username"
              label="Имя пользователя"
              outlined
              dense
              prefix-icon="person"
              :rules="[
                val => val && val.length > 0 || 'Введите имя пользователя',
                val => val.length >= 3 || 'Минимум 3 символа'
              ]"
            />

            <q-input
              v-model="form.email"
              label="Email"
              type="email"
              outlined
              dense
              prefix-icon="mail"
              :rules="[
                val => val && val.length > 0 || 'Введите email',
                val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Некорректный email'
              ]"
            />

            <q-input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              label="Пароль"
              outlined
              dense
              prefix-icon="lock"
              :rules="[
                val => val && val.length > 0 || 'Введите пароль',
                val => val.length >= 6 || 'Минимум 6 символов'
              ]"
            >
              <template v-slot:append>
                <q-icon
                  :name="showPassword ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="showPassword = !showPassword"
                />
              </template>
            </q-input>

            <q-input
              v-model="form.confirmPassword"
              :type="showPassword ? 'text' : 'password'"
              label="Подтвердите пароль"
              outlined
              dense
              prefix-icon="lock"
              :rules="[
                val => val === form.password || 'Пароли не совпадают'
              ]"
            />

            <q-toggle
              v-model="useTelegram"
              label="Привязать Telegram аккаунт (опционально)"
              color="primary"
            />

            <q-btn
              type="submit"
              label="Продолжить"
              color="primary"
              class="full-width"
              size="lg"
              :loading="loading"
              unelevated
              rounded
            />
          </q-form>

          <div class="q-mt-lg text-center">
            <p class="text-grey-7">
              Уже есть аккаунт?
              <q-btn
                label="Войти"
                flat
                color="primary"
                size="sm"
                @click="goToLogin"
                class="q-ml-xs"
              />
            </p>
          </div>
        </div>

        <!-- Step 2: Email Verification -->
        <div v-if="step === 'verify'">
          <div class="verify-section q-gutter-md">
            <div class="verify-icon">📧</div>
            <p class="text-center">
              Введите код подтверждения, отправленный на
              <strong>{{ registrationData?.email }}</strong>
            </p>

            <q-form @submit.prevent="onVerify">
              <q-input
                v-model="verifyForm.code"
                label="Код (6 цифр)"
                outlined
                dense
                maxlength="6"
                type="text"
                input-class="text-center"
                :rules="[
                  val => val && val.length === 6 || 'Введите 6 цифр'
                ]"
              />

              <q-btn
                type="submit"
                label="Подтвердить"
                color="primary"
                class="full-width q-mt-md"
                size="lg"
                :loading="loading"
                unelevated
                rounded
              />
            </q-form>

            <div class="text-center q-mt-md">
              <p class="text-caption text-grey-6">Не получили код?</p>
              <q-btn
                label="Отправить заново"
                flat
                color="primary"
                size="sm"
                @click="resendCode"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 500px;
}

.register-card {
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
  font-size: 24px;
}

.subtitle {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.verify-section {
  padding: 20px;
}

.verify-icon {
  text-align: center;
  font-size: 64px;
  margin-bottom: 20px;
}

@media (max-width: 600px) {
  .register-card {
    padding: 30px 20px;
  }

  h4 {
    font-size: 20px;
  }
}
</style>