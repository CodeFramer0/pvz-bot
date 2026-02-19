<template>
  <div class="pvz-auth-page">
    <div class="pvz-auth-page__container">

      <!-- Blobs -->
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>

      <div class="pvz-auth-page__card">

        <!-- Logo -->
        <div class="pvz-logo-section">
          <div class="pvz-logo-section__circle anim-bounce">🛍️</div>
          <h2 class="pvz-logo-section__title">PVZ Bot</h2>
          <p class="pvz-logo-section__subtitle">Умное управление заказами</p>
        </div>

        <!-- Auth Tabs -->
        <div class="pvz-auth-tabs">
          <div :class="['auth-tab', { active: tab === 'email' }]" @click="tab = 'email'">
            <q-icon name="mail" size="20px" />
            <span>Email</span>
          </div>
          <div :class="['auth-tab', { active: tab === 'telegram' }]" @click="tab = 'telegram'">
            <q-icon name="send" size="20px" />
            <span>Telegram</span>
          </div>
        </div>

        <!-- Email Login -->
        <div v-if="tab === 'email' && !showVerification" class="auth-body">
          <q-form @submit.prevent="onLoginEmail">
            <div class="pvz-form-group">
              <label class="pvz-form-label">Email адрес</label>
              <q-input
                v-model="emailForm.email"
                type="email" outlined dense
                placeholder="your@email.com"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите email',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Некорректный email'
                ]"
              >
                <template v-slot:prepend><q-icon name="mail" color="primary" /></template>
              </q-input>
            </div>

            <div class="pvz-form-group">
              <label class="pvz-form-label">Пароль</label>
              <q-input
                v-model="emailForm.password"
                :type="showPassword ? 'text' : 'password'"
                outlined dense
                placeholder="Введите пароль"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[val => val && val.length > 0 || 'Введите пароль']"
              >
                <template v-slot:prepend><q-icon name="lock" color="primary" /></template>
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>
            </div>

            <div class="forgot-link">
              <q-btn label="Забыли пароль?" flat dense color="primary" size="sm" @click="openResetPassword" />
            </div>

            <q-btn
              type="submit"
              label="Войти"
              color="primary" unelevated rounded
              class="pvz-btn-primary"
              size="lg"
              :loading="loading"
            />
          </q-form>
        </div>

        <!-- Email Verification -->
        <div v-if="tab === 'email' && showVerification" class="auth-body">
          <div class="verify-header">
            <div class="verify-icon">✉️</div>
            <h5 class="verify-title">Проверьте почту</h5>
            <p class="verify-text">
              Мы отправили код на<br/>
              <strong>{{ userForVerification?.email }}</strong>
            </p>
          </div>

          <q-form @submit.prevent="onVerifyEmail">
            <div class="pvz-form-group">
              <label class="pvz-form-label">Код подтверждения</label>
              <q-input
                v-model="verificationForm.code"
                outlined dense
                placeholder="000000"
                bg-color="grey-1"
                class="pvz-form-input pvz-form-input--code"
                maxlength="6"
                :rules="[val => val && val.length === 6 || 'Введите 6-значный код']"
              >
                <template v-slot:prepend><q-icon name="vpn_key" color="primary" /></template>
              </q-input>
            </div>

            <q-btn
              type="submit"
              label="Подтвердить"
              color="primary" unelevated rounded
              class="pvz-btn-primary"
              size="lg"
              :loading="loading"
            />
          </q-form>
        </div>

        <!-- Telegram Login -->
        <div v-if="tab === 'telegram'" class="auth-body tg-auth">
          <div class="tg-hero">
            <div class="tg-icon">✈️</div>
            <h5 class="tg-title">Быстрый вход</h5>
            <p class="tg-text">Войдите через Telegram бот для мгновенного доступа к вашим заказам</p>
          </div>

          <q-btn
            label="Открыть бот"
            color="info" unelevated rounded
            class="pvz-btn-primary q-mb-md"
            size="lg"
            icon="open_in_new"
            @click="onLoginTelegram"
          />

          <div class="tg-note">
            <q-icon name="info" size="16px" color="grey-6" />
            <span>Бот автоматически создаст аккаунт</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="pvz-auth-footer">
          <span class="pvz-auth-footer__text">Нет аккаунта?</span>
          <q-btn label="Зарегистрироваться" flat dense color="primary" class="pvz-auth-footer__link" @click="goToRegister" />
        </div>

      </div>
    </div>

    <!-- Reset Password Dialog -->
    <q-dialog v-model="showResetPassword" transition-show="slide-up" transition-hide="slide-down">
      <q-card class="reset-dialog">
        <q-card-section class="reset-dialog__header">
          <h5>Восстановление пароля</h5>
          <q-btn icon="close" flat round dense v-close-popup @click="closeResetPassword" />
        </q-card-section>

        <q-separator />

        <q-card-section class="reset-dialog__body">

          <!-- Step 1: Email -->
          <div v-if="resetStep === 1">
            <p class="reset-desc">
              Введите email, связанный с вашим аккаунтом. Мы отправим код для сброса пароля.
            </p>
            <div class="pvz-form-group">
              <label class="pvz-form-label">Email адрес</label>
              <q-input
                v-model="resetPasswordForm.email"
                type="email" outlined dense
                placeholder="your@email.com"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите email',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Некорректный email'
                ]"
              >
                <template v-slot:prepend><q-icon name="mail" color="primary" /></template>
              </q-input>
            </div>
            <q-btn
              label="Отправить код"
              color="primary" unelevated rounded
              class="pvz-btn-primary"
              :loading="loading"
              @click="sendPasswordResetCode"
            />
          </div>

          <!-- Step 2: Code + New Password -->
          <div v-if="resetStep === 2">
            <div class="reset-sent">
              <q-icon name="mark_email_read" size="48px" color="positive" />
              <p>Код отправлен на<br/><strong>{{ resetPasswordForm.email }}</strong></p>
            </div>

            <div class="pvz-form-group">
              <label class="pvz-form-label">Код из письма</label>
              <q-input v-model="resetPasswordForm.code" outlined dense placeholder="000000" bg-color="grey-1" class="pvz-form-input" maxlength="6" :rules="[val => val && val.length > 0 || 'Введите код']">
                <template v-slot:prepend><q-icon name="vpn_key" color="primary" /></template>
              </q-input>
            </div>
            <div class="pvz-form-group">
              <label class="pvz-form-label">Новый пароль</label>
              <q-input v-model="resetPasswordForm.password" type="password" outlined dense placeholder="Минимум 8 символов" bg-color="grey-1" class="pvz-form-input" :rules="[val => val && val.length > 0 || 'Введите пароль', val => val.length >= 8 || 'Минимум 8 символов']">
                <template v-slot:prepend><q-icon name="lock" color="primary" /></template>
              </q-input>
            </div>
            <div class="pvz-form-group">
              <label class="pvz-form-label">Подтвердите пароль</label>
              <q-input v-model="resetPasswordForm.passwordConfirm" type="password" outlined dense placeholder="Повторите пароль" bg-color="grey-1" class="pvz-form-input" :rules="[val => val && val.length > 0 || 'Подтвердите пароль', val => val === resetPasswordForm.password || 'Пароли не совпадают']">
                <template v-slot:prepend><q-icon name="lock_outline" color="primary" /></template>
              </q-input>
            </div>

            <div class="pvz-btn-group">
              <q-btn label="Назад" outline color="primary" class="pvz-btn-back" @click="backToStep1" :disable="loading" />
              <q-btn label="Сбросить" color="primary" unelevated class="pvz-btn-primary" :loading="loading" @click="resetPassword" />
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
const showVerification = ref(false)
const resetStep = ref(1)
const userForVerification = ref(null)

const emailForm = ref({ email: '', password: '' })
const verificationForm = ref({ code: '' })
const resetPasswordForm = ref({ email: '', code: '', password: '', passwordConfirm: '' })

const notify = (color, message, icon) => Notify.create({ color, message, position: 'top', icon })

const onLoginEmail = async () => {
  loading.value = true
  try {
    const response = await authStore.login(emailForm.value.email, emailForm.value.password)
    if (response.status === 'success') {
      notify('positive', 'Добро пожаловать! 🎉', 'check_circle')
      router.push('/')
    } else if (response.status === 'verification_needed') {
      showVerification.value = true
      userForVerification.value = { id: response.user_id, email: response.email }
      Notify.create({ color: 'info', message: response.message, position: 'top' })
    } else {
      notify('negative', response.error || 'Ошибка входа', 'error')
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
      notify('positive', 'Email подтверждён! 🎉', 'check_circle')
      router.push('/')
    } else {
      notify('negative', 'Неверный код', 'error')
    }
  } catch {
    notify('negative', 'Ошибка подтверждения', 'error')
  } finally {
    loading.value = false
  }
}

const onLoginTelegram = () => Notify.create({ color: 'info', message: 'Откройте Telegram бота для входа', position: 'top' })
const goToRegister = () => router.push('/register')

const emptyResetForm = () => ({ email: '', code: '', password: '', passwordConfirm: '' })

const openResetPassword = () => {
  showResetPassword.value = true
  resetStep.value = 1
  resetPasswordForm.value = emptyResetForm()
}

const closeResetPassword = () => {
  showResetPassword.value = false
  resetStep.value = 1
  resetPasswordForm.value = emptyResetForm()
}

const sendPasswordResetCode = async () => {
  if (!resetPasswordForm.value.email) { notify('negative', 'Введите email', 'error'); return }
  loading.value = true
  try {
    const res = await apiClient.post('/auth/forgot-password/', { email: resetPasswordForm.value.email })
    if (res.ok) {
      notify('positive', 'Код отправлен на почту! 📧', 'check_circle')
      resetStep.value = 2
    } else {
      const data = await res.json()
      notify('negative', data.detail || 'Ошибка при отправке кода', 'error')
    }
  } catch {
    notify('negative', 'Ошибка подключения', 'error')
  } finally {
    loading.value = false
  }
}

const resetPassword = async () => {
  const { code, password, passwordConfirm, email } = resetPasswordForm.value
  if (!code)                        { notify('negative', 'Введите код', 'error'); return }
  if (!password)                    { notify('negative', 'Введите пароль', 'error'); return }
  if (password !== passwordConfirm) { notify('negative', 'Пароли не совпадают', 'error'); return }
  if (password.length < 8)         { notify('negative', 'Пароль должен быть не менее 8 символов', 'error'); return }

  loading.value = true
  try {
    const res = await apiClient.post('/auth/reset-password/', {
      email, code, new_password: password, new_password_confirm: passwordConfirm
    })
    const data = await res.json()
    if (res.ok) {
      notify('positive', 'Пароль успешно изменён! 🎉', 'check_circle')
      closeResetPassword()
      await authStore.login(email, password)
    } else {
      notify('negative', data.detail || 'Ошибка при сбросе пароля', 'error')
    }
  } catch {
    notify('negative', 'Ошибка подключения', 'error')
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

<style lang="scss" scoped>
// Только уникальное для страницы логина

// Забыли пароль — выравнивание вправо
.forgot-link {
  text-align: right;
  margin-top: -8px;
  margin-bottom: 20px;
}

// Отступ под формой
.auth-body {
  margin-bottom: 24px;
}

// Верификация email
.verify-header {
  text-align: center;
  margin-bottom: 24px;

  .verify-icon  { font-size: 64px; margin-bottom: 16px; }
  .verify-title { margin: 0 0 8px; font-size: 20px; font-weight: 700; color: #2c3e50; }
  .verify-text  { margin: 0; font-size: 14px; color: #6b7280; line-height: 1.6; }
}

// Telegram-блок
.tg-auth { text-align: center; }

.tg-hero {
  margin-bottom: 24px;
  .tg-icon  { font-size: 80px; margin-bottom: 16px; }
  .tg-title { margin: 0 0 8px; font-size: 20px; font-weight: 700; color: #2c3e50; }
  .tg-text  { margin: 0; font-size: 14px; color: #6b7280; line-height: 1.6; }
}

.tg-note {
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

// Reset dialog
.reset-dialog {
  border-radius: 24px;
  max-width: 440px;
  width: 90vw;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px;
    h5 { margin: 0; font-size: 20px; font-weight: 700; color: #2c3e50; }
  }

  &__body { padding: 24px; }
}

.reset-desc {
  margin: 0 0 24px;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.reset-sent {
  text-align: center;
  margin-bottom: 24px;
  p { margin: 12px 0 0; font-size: 14px; color: #6b7280; line-height: 1.6; }
}
</style>