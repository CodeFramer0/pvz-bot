<template>
  <div class="register-page">
    <div class="register-container">
      <!-- Animated Background Blobs -->
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>

      <!-- Progress Indicator -->
      <div class="progress-bar">
        <div :class="['progress-step', { active: step === 'form' }]">
          <div class="progress-circle">1</div>
          <span class="progress-label">Регистрация</span>
        </div>
        <div class="progress-line" :class="{ active: step === 'verify' }"></div>
        <div :class="['progress-step', { active: step === 'verify' }]">
          <div class="progress-circle">2</div>
          <span class="progress-label">Подтверждение</span>
        </div>
      </div>

      <div class="register-card">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-wrapper">
            <div class="logo-circle">
              <div class="logo-icon">{{ step === 'form' ? '🎉' : '✉️' }}</div>
            </div>
          </div>
          <h2 class="app-title">
            {{ step === 'form' ? 'Создать аккаунт' : 'Подтверждение' }}
          </h2>
          <p class="app-subtitle">
            {{ step === 'form' ? 'Присоединяйтесь к PVZ Bot' : 'Проверьте вашу почту' }}
          </p>
        </div>

        <!-- Registration Form -->
        <div v-if="step === 'form'" class="auth-form">
          <q-form @submit.prevent="onRegister">
            <div class="form-group">
              <label class="form-label">Имя пользователя</label>
              <q-input
                v-model="form.username"
                outlined
                dense
                placeholder="Введите имя"
                bg-color="grey-1"
                class="form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите имя пользователя',
                  val => val.length >= 3 || 'Минимум 3 символа'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="person" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <label class="form-label">Email адрес</label>
              <q-input
                v-model="form.email"
                type="email"
                outlined
                dense
                placeholder="your@email.com"
                bg-color="grey-1"
                class="form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите email',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Некорректный email'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="mail" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <label class="form-label">Пароль</label>
              <q-input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                outlined
                dense
                placeholder="Минимум 6 символов"
                bg-color="grey-1"
                class="form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите пароль',
                  val => val.length >= 6 || 'Минимум 6 символов'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="lock" color="primary" />
                </template>
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <label class="form-label">Подтвердите пароль</label>
              <q-input
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                outlined
                dense
                placeholder="Повторите пароль"
                bg-color="grey-1"
                class="form-input"
                :rules="[
                  val => val === form.password || 'Пароли не совпадают'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="lock_outline" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="telegram-option">
              <q-checkbox
                v-model="useTelegram"
                color="primary"
                class="telegram-checkbox"
              />
              <div class="telegram-option-text">
                <span class="telegram-option-label">Привязать Telegram</span>
                <span class="telegram-option-desc">(опционально)</span>
              </div>
            </div>

            <q-btn
              type="submit"
              label="Продолжить"
              color="primary"
              unelevated
              rounded
              class="submit-btn"
              size="lg"
              icon="arrow_forward"
              :loading="loading"
            />
          </q-form>
        </div>

        <!-- Verification Form -->
        <div v-if="step === 'verify'" class="auth-form">
          <div class="verification-header">
            <div class="verification-badge">
              <q-icon name="mark_email_read" size="48px" color="primary" />
            </div>
            <h5 class="verification-title">Код отправлен!</h5>
            <p class="verification-text">
              Введите 6-значный код, который мы отправили на<br/>
              <strong>{{ registrationData?.email }}</strong>
            </p>
          </div>

          <q-form @submit.prevent="onVerify">
            <div class="form-group">
              <label class="form-label">Код подтверждения</label>
              <q-input
                v-model="verifyForm.code"
                outlined
                dense
                placeholder="000000"
                bg-color="grey-1"
                class="form-input code-input"
                maxlength="6"
                input-class="text-center"
                :rules="[val => val && val.length === 6 || 'Введите 6 цифр']"
              >
                <template v-slot:prepend>
                  <q-icon name="vpn_key" color="primary" />
                </template>
              </q-input>
            </div>

            <q-btn
              type="submit"
              label="Подтвердить email"
              color="primary"
              unelevated
              rounded
              class="submit-btn"
              size="lg"
              icon="check_circle"
              :loading="loading"
            />

            <div class="resend-section">
              <p class="resend-text">Не получили код?</p>
              <q-btn
                label="Отправить заново"
                flat
                dense
                color="primary"
                class="resend-btn"
                @click="resendCode"
              />
            </div>
          </q-form>
        </div>

        <!-- Login Link -->
        <div class="login-section">
          <span class="login-text">Уже есть аккаунт?</span>
          <q-btn
            label="Войти"
            flat
            dense
            color="primary"
            class="login-btn"
            @click="goToLogin"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const step = ref('form')
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
      position: 'top',
      icon: 'error'
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
      color: 'positive',
      message: 'Код отправлен на вашу почту! 📧',
      position: 'top',
      icon: 'check_circle'
    })
  } catch (error) {
    $q.notify({
      color: 'negative',
      message: error.message || 'Ошибка регистрации',
      position: 'top',
      icon: 'error'
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
        message: 'Email подтверждён! Добро пожаловать! 🎉',
        position: 'top',
        icon: 'check_circle'
      })
      router.push('/orders')
    } else {
      $q.notify({
        color: 'negative',
        message: 'Неверный код',
        position: 'top',
        icon: 'error'
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
    message: 'Код отправлен повторно! 📧',
    position: 'top',
    icon: 'mail'
  })
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* Animated Blobs */
.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 20s ease-in-out infinite;
}

.blob-1 {
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.3);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.2);
  bottom: -150px;
  right: -150px;
  animation-delay: 5s;
}

.blob-3 {
  width: 250px;
  height: 250px;
  background: rgba(255, 255, 255, 0.25);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.register-container {
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 1;
}

/* Progress Bar */
.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  padding: 0 20px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.progress-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
}

.progress-step.active .progress-circle {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.progress-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
  transition: all 0.3s ease;
}

.progress-step.active .progress-label {
  color: white;
}

.progress-line {
  width: 60px;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  margin: 0 12px;
  transition: all 0.3s ease;
}

.progress-line.active {
  background: white;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.3);
}

/* Register Card */
.register-card {
  background: white;
  border-radius: 32px;
  padding: 40px 32px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo Section */
.logo-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo-wrapper {
  margin-bottom: 16px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  border-radius: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
  animation: bounce 0.8s ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.logo-icon {
  font-size: 40px;
}

.app-title {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: -0.5px;
}

.app-subtitle {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

/* Forms */
.auth-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  letter-spacing: 0.3px;
}

.form-input :deep(.q-field__control) {
  border-radius: 12px;
  height: 48px;
}

.code-input :deep(input) {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 4px;
}

.telegram-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  margin-bottom: 20px;
}

.telegram-checkbox :deep(.q-checkbox__inner) {
  width: 24px;
  height: 24px;
}

.telegram-option-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.telegram-option-label {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.telegram-option-desc {
  font-size: 12px;
  color: #6b7280;
}

.submit-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

/* Verification */
.verification-header {
  text-align: center;
  margin-bottom: 24px;
}

.verification-badge {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.verification-title {
  margin: 0 0 8px 0;
  font-size: 22px;
  font-weight: 700;
  color: #2c3e50;
}

.verification-text {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.resend-section {
  margin-top: 20px;
  text-align: center;
}

.resend-text {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: #6b7280;
}

.resend-btn {
  font-size: 14px;
  font-weight: 600;
}

/* Login Section */
.login-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.login-text {
  font-size: 14px;
  color: #6b7280;
  margin-right: 4px;
}

.login-btn {
  font-weight: 600;
  font-size: 14px;
}

@media (max-width: 480px) {
  .register-card {
    padding: 32px 24px;
  }

  .app-title {
    font-size: 24px;
  }

  .progress-bar {
    padding: 0 10px;
  }

  .progress-line {
    width: 40px;
  }

  .progress-label {
    font-size: 11px;
  }
}
</style>
