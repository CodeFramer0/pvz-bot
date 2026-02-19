<template>
  <div class="pvz-auth-page">
    <div class="pvz-auth-page__container">

      <!-- Blobs -->
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>

      <!-- Progress Steps — снаружи карточки, на фоне градиента -->
      <div class="reg-steps">
        <div :class="['reg-step', { active: step === 'form' }]">
          <div class="reg-step__circle">1</div>
          <span class="reg-step__label">Регистрация</span>
        </div>
        <div class="reg-step__line" :class="{ active: step === 'verify' }"></div>
        <div :class="['reg-step', { active: step === 'verify' }]">
          <div class="reg-step__circle">2</div>
          <span class="reg-step__label">Подтверждение</span>
        </div>
      </div>

      <div class="pvz-auth-page__card">

        <!-- Logo -->
        <div class="pvz-logo-section">
          <div class="pvz-logo-section__circle anim-bounce">
            {{ step === 'form' ? '🎉' : '✉️' }}
          </div>
          <h2 class="pvz-logo-section__title">
            {{ step === 'form' ? 'Создать аккаунт' : 'Подтверждение' }}
          </h2>
          <p class="pvz-logo-section__subtitle">
            {{ step === 'form' ? 'Присоединяйтесь к PVZ Bot' : 'Проверьте вашу почту' }}
          </p>
        </div>

        <!-- Registration Form -->
        <div v-if="step === 'form'" class="auth-body">
          <q-form @submit.prevent="onRegister">

            <div class="pvz-form-group">
              <label class="pvz-form-label">Имя пользователя</label>
              <q-input
                v-model="form.username"
                outlined dense
                placeholder="Введите имя"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите имя пользователя',
                  val => val.length >= 3 || 'Минимум 3 символа'
                ]"
              >
                <template v-slot:prepend><q-icon name="person" color="primary" /></template>
              </q-input>
            </div>

            <div class="pvz-form-group">
              <label class="pvz-form-label">Email адрес</label>
              <q-input
                v-model="form.email"
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
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                outlined dense
                placeholder="Минимум 6 символов"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[
                  val => val && val.length > 0 || 'Введите пароль',
                  val => val.length >= 6 || 'Минимум 6 символов'
                ]"
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

            <div class="pvz-form-group">
              <label class="pvz-form-label">Подтвердите пароль</label>
              <q-input
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                outlined dense
                placeholder="Повторите пароль"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[val => val === form.password || 'Пароли не совпадают']"
              >
                <template v-slot:prepend><q-icon name="lock_outline" color="primary" /></template>
              </q-input>
            </div>

            <!-- Telegram checkbox — уникальный элемент -->
            <div class="tg-option">
              <q-checkbox v-model="useTelegram" color="primary" />
              <div class="tg-option__text">
                <span class="tg-option__label">Привязать Telegram</span>
                <span class="tg-option__desc">(опционально)</span>
              </div>
            </div>

            <q-btn
              type="submit"
              label="Продолжить"
              color="primary" unelevated rounded
              class="pvz-btn-primary"
              size="lg"
              icon="arrow_forward"
              :loading="loading"
            />
          </q-form>
        </div>

        <!-- Verification Form -->
        <div v-if="step === 'verify'" class="auth-body">
          <div class="verify-header">
            <div class="verify-badge">
              <q-icon name="mark_email_read" size="48px" color="primary" />
            </div>
            <h5 class="verify-title">Код отправлен!</h5>
            <p class="verify-text">
              Введите 6-значный код, который мы отправили на<br/>
              <strong>{{ registrationData?.email }}</strong>
            </p>
          </div>

          <q-form @submit.prevent="onVerify">
            <div class="pvz-form-group">
              <label class="pvz-form-label">Код подтверждения</label>
              <q-input
                v-model="verifyForm.code"
                outlined dense
                placeholder="000000"
                bg-color="grey-1"
                class="pvz-form-input pvz-form-input--code"
                maxlength="6"
                :rules="[val => val && val.length === 6 || 'Введите 6 цифр']"
              >
                <template v-slot:prepend><q-icon name="vpn_key" color="primary" /></template>
              </q-input>
            </div>

            <q-btn
              type="submit"
              label="Подтвердить email"
              color="primary" unelevated rounded
              class="pvz-btn-primary"
              size="lg"
              icon="check_circle"
              :loading="loading"
            />

            <div class="resend">
              <p class="resend__text">Не получили код?</p>
              <q-btn label="Отправить заново" flat dense color="primary" @click="resendCode" />
            </div>
          </q-form>
        </div>

        <!-- Footer -->
        <div class="pvz-auth-footer">
          <span class="pvz-auth-footer__text">Уже есть аккаунт?</span>
          <q-btn label="Войти" flat dense color="primary" class="pvz-auth-footer__link" @click="goToLogin" />
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
const registrationData = ref(null)

const form = ref({ username: '', email: '', password: '', confirmPassword: '' })
const verifyForm = ref({ code: '' })

const notify = (color, message, icon) => $q.notify({ color, message, position: 'top', icon })

const onRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    notify('negative', 'Пароли не совпадают', 'error')
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
    notify('positive', 'Код отправлен на вашу почту! 📧', 'check_circle')
  } catch (error) {
    notify('negative', error.message || 'Ошибка регистрации', 'error')
  } finally {
    loading.value = false
  }
}

const onVerify = async () => {
  loading.value = true
  try {
    const success = await authStore.verifyEmail(registrationData.value.user_id, verifyForm.value.code)
    if (success) {
      notify('positive', 'Email подтверждён! Добро пожаловать! 🎉', 'check_circle')
      router.push('/orders')
    } else {
      notify('negative', 'Неверный код', 'error')
    }
  } finally {
    loading.value = false
  }
}

const resendCode = () => notify('info', 'Код отправлен повторно! 📧', 'mail')
const goToLogin = () => router.push('/login')
</script>

<style lang="scss" scoped>
// Только уникальное для страницы регистрации

.auth-body {
  margin-bottom: 24px;
}

// Прогресс-шаги снаружи карточки — стеклянный стиль на градиентном фоне
.reg-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  padding: 0 20px;

  @media (max-width: 480px) {
    padding: 0 10px;
  }
}

.reg-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;

  &__circle {
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

  &__label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 600;
    transition: all 0.3s ease;

    @media (max-width: 480px) { font-size: 11px; }
  }

  &__line {
    width: 60px;
    height: 3px;
    background: rgba(255, 255, 255, 0.2);
    margin: 0 12px 22px; // 22px — отступ под лейбл
    transition: all 0.3s ease;

    &.active {
      background: white;
      box-shadow: 0 2px 8px rgba(255, 255, 255, 0.3);
    }

    @media (max-width: 480px) { width: 40px; }
  }

  &.active {
    .reg-step__circle {
      background: white;
      color: #667eea;
      box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
      transform: scale(1.1);
    }
    .reg-step__label { color: white; }
  }
}

// Telegram-опция
.tg-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  margin-bottom: 20px;

  &__text {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  &__label {
    font-size: 14px;
    font-weight: 600;
    color: #2c3e50;
  }

  &__desc {
    font-size: 12px;
    color: #6b7280;
  }
}

// Верификация
.verify-header {
  text-align: center;
  margin-bottom: 24px;
}

.verify-badge {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.verify-title {
  margin: 0 0 8px;
  font-size: 22px;
  font-weight: 700;
  color: #2c3e50;
}

.verify-text {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

// Переотправка кода
.resend {
  margin-top: 20px;
  text-align: center;

  &__text {
    margin: 0 0 4px;
    font-size: 13px;
    color: #6b7280;
  }
}
</style>