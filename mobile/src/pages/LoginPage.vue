<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Animated Background Blobs -->
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>

      <div class="login-card">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-wrapper">
            <div class="logo-circle">
              <div class="logo-icon">🛍️</div>
            </div>
          </div>
          <h2 class="app-title">PVZ Bot</h2>
          <p class="app-subtitle">Умное управление заказами</p>
        </div>

        <!-- Auth Tabs -->
        <div class="auth-tabs">
          <div 
            :class="['auth-tab', { active: tab === 'email' }]"
            @click="tab = 'email'"
          >
            <q-icon name="mail" size="20px" />
            <span>Email</span>
          </div>
          <div 
            :class="['auth-tab', { active: tab === 'telegram' }]"
            @click="tab = 'telegram'"
          >
            <q-icon name="send" size="20px" />
            <span>Telegram</span>
          </div>
        </div>

        <!-- Email Login -->
        <div v-if="tab === 'email' && !showVerification" class="auth-form">
          <q-form @submit.prevent="onLoginEmail">
            <div class="form-group">
              <label class="form-label">Email адрес</label>
              <q-input
                v-model="emailForm.email"
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
                v-model="emailForm.password"
                :type="showPassword ? 'text' : 'password'"
                outlined
                dense
                placeholder="Введите пароль"
                bg-color="grey-1"
                class="form-input"
                :rules="[val => val && val.length > 0 || 'Введите пароль']"
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

            <div class="forgot-password-link">
              <q-btn
                label="Забыли пароль?"
                flat
                dense
                color="primary"
                size="sm"
                @click="openResetPassword"
              />
            </div>

            <q-btn
              type="submit"
              label="Войти"
              color="primary"
              unelevated
              rounded
              class="submit-btn"
              size="lg"
              :loading="loading"
            />
          </q-form>
        </div>

        <!-- Email Verification -->
        <div v-if="tab === 'email' && showVerification" class="auth-form">
          <div class="verification-header">
            <div class="verification-icon">✉️</div>
            <h5 class="verification-title">Проверьте почту</h5>
            <p class="verification-text">
              Мы отправили код на<br/>
              <strong>{{ userForVerification?.email }}</strong>
            </p>
          </div>

          <q-form @submit.prevent="onVerifyEmail">
            <div class="form-group">
              <label class="form-label">Код подтверждения</label>
              <q-input
                v-model="verificationForm.code"
                outlined
                dense
                placeholder="000000"
                bg-color="grey-1"
                class="form-input code-input"
                maxlength="6"
                input-class="text-center"
                :rules="[val => val && val.length === 6 || 'Введите 6-значный код']"
              >
                <template v-slot:prepend>
                  <q-icon name="vpn_key" color="primary" />
                </template>
              </q-input>
            </div>

            <q-btn
              type="submit"
              label="Подтвердить"
              color="primary"
              unelevated
              rounded
              class="submit-btn"
              size="lg"
              :loading="loading"
            />
          </q-form>
        </div>

        <!-- Telegram Login -->
        <div v-if="tab === 'telegram'" class="auth-form telegram-auth">
          <div class="telegram-hero">
            <div class="telegram-icon-big">✈️</div>
            <h5 class="telegram-title">Быстрый вход</h5>
            <p class="telegram-text">
              Войдите через Telegram бот для мгновенного доступа к вашим заказам
            </p>
          </div>

          <q-btn
            label="Открыть бот"
            color="info"
            unelevated
            rounded
            class="submit-btn telegram-btn"
            size="lg"
            icon="open_in_new"
            @click="onLoginTelegram"
          />

          <div class="telegram-note">
            <q-icon name="info" size="16px" color="grey-6" />
            <span>Бот автоматически создаст аккаунт</span>
          </div>
        </div>

        <!-- Register Link -->
        <div class="register-section">
          <span class="register-text">Нет аккаунта?</span>
          <q-btn
            label="Зарегистрироваться"
            flat
            dense
            color="primary"
            class="register-btn"
            @click="goToRegister"
          />
        </div>
      </div>
    </div>

    <!-- Password Reset Dialog -->
    <q-dialog v-model="showResetPassword" transition-show="slide-up" transition-hide="slide-down">
      <q-card class="reset-card">
        <q-card-section class="reset-header">
          <h5 class="reset-title">Восстановление пароля</h5>
          <q-btn
            icon="close"
            flat
            round
            dense
            v-close-popup
            @click="closeResetPassword"
          />
        </q-card-section>

        <q-separator />

        <q-card-section class="reset-body">
          <!-- Step 1: Email -->
          <div v-if="resetStep === 1">
            <p class="reset-description">
              Введите email, связанный с вашим аккаунтом. Мы отправим код для сброса пароля.
            </p>

            <div class="form-group">
              <label class="form-label">Email адрес</label>
              <q-input
                v-model="resetPasswordForm.email"
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

            <q-btn
              label="Отправить код"
              color="primary"
              unelevated
              rounded
              class="submit-btn"
              @click="sendPasswordResetCode"
              :loading="loading"
            />
          </div>

          <!-- Step 2: Code and New Password -->
          <div v-if="resetStep === 2">
            <div class="reset-sent-message">
              <q-icon name="mark_email_read" size="48px" color="positive" />
              <p class="reset-sent-text">
                Код отправлен на<br/>
                <strong>{{ resetPasswordForm.email }}</strong>
              </p>
            </div>

            <div class="form-group">
              <label class="form-label">Код из письма</label>
              <q-input
                v-model="resetPasswordForm.code"
                outlined
                dense
                placeholder="000000"
                bg-color="grey-1"
                class="form-input"
                maxlength="6"
                :rules="[val => val && val.length > 0 || 'Введите код']"
              >
                <template v-slot:prepend>
                  <q-icon name="vpn_key" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <label class="form-label">Новый пароль</label>
              <q-input
                v-model="resetPasswordForm.password"
                type="password"
                outlined
                dense
                placeholder="Минимум 8 символов"
                bg-color="grey-1"
                class="form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите пароль',
                  val => val.length >= 8 || 'Минимум 8 символов'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="lock" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <label class="form-label">Подтвердите пароль</label>
              <q-input
                v-model="resetPasswordForm.passwordConfirm"
                type="password"
                outlined
                dense
                placeholder="Повторите пароль"
                bg-color="grey-1"
                class="form-input"
                :rules="[
                  val => val && val.length > 0 || 'Подтвердите пароль',
                  val => val === resetPasswordForm.password || 'Пароли не совпадают'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="lock_outline" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="reset-actions">
              <q-btn
                label="Назад"
                outline
                color="primary"
                class="reset-back-btn"
                @click="backToStep1"
                :disable="loading"
              />
              <q-btn
                label="Сбросить"
                color="primary"
                unelevated
                class="reset-submit-btn"
                @click="resetPassword"
                :loading="loading"
              />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth-store'
import { Notify } from 'quasar'
import apiClient from 'src/api/client'

const router = useRouter()
const authStore = useAuthStore()

const tab = ref('email')
const loading = ref(false)
const showPassword = ref(false)
const showResetPassword = ref(false)

const emailForm = ref({
  email: '',
  password: '',
})

const verificationForm = ref({
  code: '',
})

const resetPasswordForm = ref({
  email: '',
  code: '',
  password: '',
  passwordConfirm: '',
})

const resetStep = ref(1)
const userForVerification = ref(null)
const showVerification = ref(false)

const onLoginEmail = async () => {
  loading.value = true
  try {
    const response = await authStore.login(emailForm.value.email, emailForm.value.password)

    if (response.status === 'success') {
      Notify.create({ 
        color: 'positive', 
        message: 'Добро пожаловать! 🎉', 
        position: 'top', 
        icon: 'check_circle' 
      })
      router.push('/')
    } else if (response.status === 'verification_needed') {
      showVerification.value = true
      userForVerification.value = { id: response.user_id, email: response.email }
      Notify.create({ 
        color: 'info', 
        message: response.message, 
        position: 'top' 
      })
    } else {
      Notify.create({ 
        color: 'negative', 
        message: response.error || 'Ошибка входа', 
        position: 'top', 
        icon: 'error' 
      })
    }
  } finally {
    loading.value = false
  }
}

const onVerifyEmail = async () => {
  if (!userForVerification.value) return
  loading.value = true
  try {
    const success = await authStore.verifyEmail(
      userForVerification.value.id, 
      verificationForm.value.code
    )
    if (success) {
      Notify.create({ 
        color: 'positive', 
        message: 'Email подтверждён! 🎉', 
        position: 'top', 
        icon: 'check_circle' 
      })
      router.push('/')
    } else {
      Notify.create({ 
        color: 'negative', 
        message: 'Неверный код', 
        position: 'top', 
        icon: 'error' 
      })
    }
  } catch (err) {
    console.error(err)
    Notify.create({ 
      color: 'negative', 
      message: 'Ошибка подтверждения', 
      position: 'top', 
      icon: 'error' 
    })
  } finally {
    loading.value = false
  }
}

const onLoginTelegram = async () => {
  Notify.create({ 
    color: 'info', 
    message: 'Откройте Telegram бота для входа', 
    position: 'top' 
  })
}

const goToRegister = () => {
  router.push('/register')
}

const openResetPassword = () => {
  showResetPassword.value = true
  resetStep.value = 1
  resetPasswordForm.value = {
    email: '',
    code: '',
    password: '',
    passwordConfirm: '',
  }
}

const closeResetPassword = () => {
  showResetPassword.value = false
  resetStep.value = 1
  resetPasswordForm.value = {
    email: '',
    code: '',
    password: '',
    passwordConfirm: '',
  }
}

const sendPasswordResetCode = async () => {
  if (!resetPasswordForm.value.email) {
    Notify.create({ 
      color: 'negative', 
      message: 'Введите email', 
      position: 'top', 
      icon: 'error' 
    })
    return
  }

  loading.value = true
  try {
    const response = await apiClient.post('auth/forgot-password/', {
      email: resetPasswordForm.value.email
    })

    if (response.ok) {
      Notify.create({ 
        color: 'positive', 
        message: 'Код отправлен на почту! 📧', 
        position: 'top', 
        icon: 'check_circle' 
      })
      resetStep.value = 2
    } else {
      const data = await response.json()
      Notify.create({ 
        color: 'negative', 
        message: data.detail || 'Ошибка при отправке кода', 
        position: 'top', 
        icon: 'error' 
      })
    }
  } catch (err) {
    console.error(err)
    Notify.create({ 
      color: 'negative', 
      message: 'Ошибка подключения', 
      position: 'top', 
      icon: 'error' 
    })
  } finally {
    loading.value = false
  }
}

const resetPassword = async () => {
  if (!resetPasswordForm.value.code) {
    Notify.create({ 
      color: 'negative', 
      message: 'Введите код', 
      position: 'top', 
      icon: 'error' 
    })
    return
  }
  if (!resetPasswordForm.value.password) {
    Notify.create({ 
      color: 'negative', 
      message: 'Введите пароль', 
      position: 'top', 
      icon: 'error' 
    })
    return
  }
  if (resetPasswordForm.value.password !== resetPasswordForm.value.passwordConfirm) {
    Notify.create({ 
      color: 'negative', 
      message: 'Пароли не совпадают', 
      position: 'top', 
      icon: 'error' 
    })
    return
  }
  if (resetPasswordForm.value.password.length < 8) {
    Notify.create({ 
      color: 'negative', 
      message: 'Пароль должен быть не менее 8 символов', 
      position: 'top', 
      icon: 'error' 
    })
    return
  }

  loading.value = true
  try {
    const response = await apiClient.post('auth/reset-password/', {
      email: resetPasswordForm.value.email,
      code: resetPasswordForm.value.code,
      new_password: resetPasswordForm.value.password,
      new_password_confirm: resetPasswordForm.value.passwordConfirm
    })

    const data = await response.json()

    if (response.ok) {
      Notify.create({ 
        color: 'positive', 
        message: 'Пароль успешно изменён! 🎉', 
        position: 'top', 
        icon: 'check_circle' 
      })
      closeResetPassword()
      await authStore.login(resetPasswordForm.value.email, resetPasswordForm.value.password)
    } else {
      Notify.create({ 
        color: 'negative', 
        message: data.detail || 'Ошибка при сбросе пароля', 
        position: 'top', 
        icon: 'error' 
      })
    }
  } catch (err) {
    console.error(err)
    Notify.create({ 
      color: 'negative', 
      message: 'Ошибка подключения', 
      position: 'top', 
      icon: 'error' 
    })
  } finally {
    loading.value = false
  }
}

const backToStep1 = () => {
  resetStep.value = 1
  resetPasswordForm.value.code = ''
  resetPasswordForm.value.password = ''
  resetPasswordForm.value.passwordConfirm = ''
}
</script>

<style scoped>
.login-page {
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

.login-container {
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 1;
}

.login-card {
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

/* Auth Tabs */
.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  background: #f3f4f6;
  padding: 4px;
  border-radius: 16px;
  margin-bottom: 24px;
}

.auth-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 14px;
  color: #6b7280;
}

.auth-tab.active {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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

.forgot-password-link {
  text-align: right;
  margin-top: -8px;
  margin-bottom: 20px;
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

.verification-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.verification-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.verification-text {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

/* Telegram */
.telegram-auth {
  text-align: center;
}

.telegram-hero {
  margin-bottom: 24px;
}

.telegram-icon-big {
  font-size: 80px;
  margin-bottom: 16px;
}

.telegram-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.telegram-text {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.telegram-btn {
  margin-bottom: 16px;
}

.telegram-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 12px;
  border-radius: 12px;
}

/* Register Section */
.register-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.register-text {
  font-size: 14px;
  color: #6b7280;
  margin-right: 4px;
}

.register-btn {
  font-weight: 600;
  font-size: 14px;
}

/* Reset Password Dialog */
.reset-card {
  border-radius: 24px;
  max-width: 440px;
  width: 90vw;
}

.reset-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
}

.reset-title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.reset-body {
  padding: 24px;
}

.reset-description {
  margin: 0 0 24px 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.reset-sent-message {
  text-align: center;
  margin-bottom: 24px;
}

.reset-sent-text {
  margin: 12px 0 0 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.reset-actions {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 12px;
}

.reset-back-btn,
.reset-submit-btn {
  height: 48px;
  font-weight: 600;
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }

  .app-title {
    font-size: 24px;
  }
}
</style>
