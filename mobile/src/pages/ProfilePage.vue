<template>
  <q-page class="profile-page">
    <!-- Header -->
    <div class="profile-header">
      <q-btn
        flat
        round
        dense
        icon="arrow_back"
        color="white"
        size="md"
        @click="$router.back()"
        class="back-btn"
      />
      <h4 class="header-title">Профиль</h4>
      <div class="header-spacer"></div>
    </div>

    <!-- Profile Card -->
    <div class="profile-container">
      <!-- Avatar Section -->
      <div class="avatar-section">
        <div class="avatar-wrapper">
          <div class="avatar-circle">
            <span class="avatar-letter">
              {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
            </span>
            <div class="avatar-ring"></div>
          </div>
        </div>
        <h3 class="profile-name">{{ authStore.user?.username || 'Пользователь' }}</h3>
        <p class="profile-email">{{ authStore.user?.email }}</p>
        <q-badge 
          v-if="authStore.user?.email"
          color="positive" 
          label="Подтверждён"
          class="verify-badge"
        >
          <q-icon name="verified" size="14px" class="q-ml-xs" />
        </q-badge>
      </div>

      <!-- Quick Stats -->
      <div class="quick-stats">
        <div class="stat-item">
          <div class="stat-icon stat-icon-primary">
            <q-icon name="inventory_2" size="24px" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ getTotalOrders() }}</div>
            <div class="stat-label">Заказов</div>
          </div>
        </div>
        <div class="stat-item">
          <div class="stat-icon stat-icon-success">
            <q-icon name="done_all" size="24px" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ getCompletedOrders() }}</div>
            <div class="stat-label">Выполнено</div>
          </div>
        </div>
        <div class="stat-item">
          <div class="stat-icon stat-icon-warning">
            <q-icon name="local_shipping" size="24px" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ getActiveOrders() }}</div>
            <div class="stat-label">В пути</div>
          </div>
        </div>
      </div>

      <!-- Telegram Section -->
      <div class="section-card">
        <div class="section-header">
          <div class="section-icon telegram-icon">
            <q-icon name="send" size="20px" />
          </div>
          <h5 class="section-title">Telegram</h5>
        </div>

        <div v-if="authStore.isTelegramLinked" class="telegram-linked">
          <div class="telegram-user">
            <div class="telegram-avatar">✈️</div>
            <div class="telegram-info">
              <p class="telegram-name">{{ authStore.user?.telegram_user?.nick_name }}</p>
              <p class="telegram-username">@{{ authStore.user?.telegram_user?.nick_name }}</p>
            </div>
          </div>
          <q-btn
            flat
            round
            dense
            icon="delete_outline"
            color="negative"
            @click="onUnlinkTelegram"
          />
        </div>

        <div v-else class="telegram-not-linked">
          <p class="not-linked-text">Привяжите Telegram для быстрого доступа к заказам</p>
          <q-btn
            label="Привязать аккаунт"
            color="info"
            unelevated
            rounded
            class="link-btn"
            icon="send"
            @click="onLinkTelegram"
          />
        </div>
      </div>

      <!-- Settings Section -->
      <div class="section-card">
        <div class="section-header">
          <div class="section-icon settings-icon">
            <q-icon name="settings" size="20px" />
          </div>
          <h5 class="section-title">Настройки</h5>
        </div>

        <div class="settings-list">
          <div class="setting-item" @click="onChangePassword">
            <div class="setting-left">
              <div class="setting-icon-wrapper primary-bg">
                <q-icon name="lock" size="20px" color="primary" />
              </div>
              <span class="setting-label">Изменить пароль</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>

          <div class="setting-item" @click="onNotifications">
            <div class="setting-left">
              <div class="setting-icon-wrapper warning-bg">
                <q-icon name="notifications" size="20px" color="warning" />
              </div>
              <span class="setting-label">Уведомления</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>

          <div class="setting-item" @click="onLanguage">
            <div class="setting-left">
              <div class="setting-icon-wrapper info-bg">
                <q-icon name="language" size="20px" color="info" />
              </div>
              <span class="setting-label">Язык</span>
            </div>
            <div class="setting-right">
              <span class="setting-value">Русский</span>
              <q-icon name="chevron_right" size="20px" color="grey-5" />
            </div>
          </div>
        </div>
      </div>

      <!-- About Section -->
      <div class="section-card">
        <div class="section-header">
          <div class="section-icon about-icon">
            <q-icon name="info" size="20px" />
          </div>
          <h5 class="section-title">О приложении</h5>
        </div>

        <div class="settings-list">
          <div class="setting-item" @click="onHelp">
            <div class="setting-left">
              <div class="setting-icon-wrapper">
                <q-icon name="help_outline" size="20px" color="grey-7" />
              </div>
              <span class="setting-label">Помощь</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>

          <div class="setting-item" @click="onPrivacy">
            <div class="setting-left">
              <div class="setting-icon-wrapper">
                <q-icon name="privacy_tip" size="20px" color="grey-7" />
              </div>
              <span class="setting-label">Политика конфиденциальности</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>

          <div class="setting-item">
            <div class="setting-left">
              <div class="setting-icon-wrapper">
                <q-icon name="info_outline" size="20px" color="grey-7" />
              </div>
              <span class="setting-label">Версия</span>
            </div>
            <span class="setting-value">1.0.0</span>
          </div>
        </div>
      </div>

      <!-- Logout Button -->
      <div class="logout-section">
        <q-btn
          label="Выйти из аккаунта"
          color="negative"
          outline
          rounded
          class="logout-btn"
          icon="logout"
          @click="onLogout"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

onMounted(async () => {
  await authStore.getMe()
})

const getTotalOrders = () => {
  return 12 // Replace with actual data
}

const getCompletedOrders = () => {
  return 8 // Replace with actual data
}

const getActiveOrders = () => {
  return 4 // Replace with actual data
}

const onLogout = () => {
  $q.dialog({
    title: 'Выход',
    message: 'Вы уверены, что хотите выйти из аккаунта?',
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'grey-7'
    },
    ok: {
      label: 'Выйти',
      color: 'negative',
      unelevated: true
    },
    persistent: true
  }).onOk(() => {
    authStore.logout()
    $q.notify({
      color: 'positive',
      message: 'Вы вышли из аккаунта',
      position: 'top',
      icon: 'check_circle'
    })
    router.push('/login')
  })
}

const onLinkTelegram = () => {
  $q.notify({
    color: 'info',
    message: 'Откройте бота для привязки Telegram',
    position: 'top',
    icon: 'send'
  })
}

const onUnlinkTelegram = () => {
  $q.dialog({
    title: 'Отвязать Telegram',
    message: 'Вы уверены, что хотите отвязать Telegram аккаунт?',
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'grey-7'
    },
    ok: {
      label: 'Отвязать',
      color: 'negative',
      unelevated: true
    },
    persistent: true
  }).onOk(() => {
    $q.notify({
      color: 'positive',
      message: 'Telegram отвязан',
      position: 'top',
      icon: 'check_circle'
    })
  })
}

const onChangePassword = () => {
  $q.notify({
    color: 'info',
    message: 'Функция в разработке',
    position: 'top'
  })
}

const onNotifications = () => {
  $q.notify({
    color: 'info',
    message: 'Функция в разработке',
    position: 'top'
  })
}

const onLanguage = () => {
  $q.notify({
    color: 'info',
    message: 'Функция в разработке',
    position: 'top'
  })
}

const onHelp = () => {
  $q.notify({
    color: 'info',
    message: 'Функция в разработке',
    position: 'top'
  })
}

const onPrivacy = () => {
  $q.notify({
    color: 'info',
    message: 'Функция в разработке',
    position: 'top'
  })
}
</script>

<style scoped>
.profile-page {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding-bottom: 80px;
}

/* Header */
.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.back-btn {
  flex-shrink: 0;
}

.header-title {
  margin: 0;
  color: white;
  font-size: 18px;
  font-weight: 600;
  flex-grow: 1;
  text-align: center;
}

.header-spacer {
  width: 40px;
  flex-shrink: 0;
}

/* Profile Container */
.profile-container {
  padding: 0 16px;
  margin-top: 20px;
}

/* Avatar Section */
.avatar-section {
  text-align: center;
  margin-bottom: 24px;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 2;
}

.avatar-letter {
  font-size: 40px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.avatar-ring {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.3);
  z-index: 1;
}

.profile-name {
  margin: 0 0 4px 0;
  color: white;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.profile-email {
  margin: 0 0 8px 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.verify-badge {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

/* Quick Stats */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.stat-item {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 16px 12px;
  text-align: center;
  transition: transform 0.2s;
}

.stat-item:active {
  transform: scale(0.95);
}

.stat-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 8px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-primary {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  color: white;
}

.stat-icon-success {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.2) 100%);
  color: white;
}

.stat-icon-warning {
  background: linear-gradient(135deg, rgba(251, 146, 60, 0.2) 0%, rgba(234, 88, 12, 0.2) 100%);
  color: white;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin-bottom: 2px;
}

.stat-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* Section Card */
.section-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.telegram-icon {
  background: linear-gradient(135deg, #0088cc 0%, #00a0e9 100%);
}

.settings-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.about-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.section-title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
}

/* Telegram Section */
.telegram-linked {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: linear-gradient(135deg, rgba(0, 136, 204, 0.1) 0%, rgba(0, 160, 233, 0.1) 100%);
  border: 1px solid rgba(0, 136, 204, 0.2);
  border-radius: 12px;
}

.telegram-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.telegram-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.telegram-info {
  flex: 1;
}

.telegram-name {
  margin: 0 0 2px 0;
  font-size: 15px;
  font-weight: 600;
  color: #2c3e50;
}

.telegram-username {
  margin: 0;
  font-size: 13px;
  color: #6b7280;
}

.telegram-not-linked {
  padding: 16px;
  background: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
  text-align: center;
}

.not-linked-text {
  margin: 0 0 16px 0;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
}

.link-btn {
  width: 100%;
  height: 44px;
  font-weight: 600;
}

/* Settings List */
.settings-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.setting-item:hover {
  background: #f9fafb;
}

.setting-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.setting-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.setting-icon-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.primary-bg {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.warning-bg {
  background: linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(234, 88, 12, 0.1) 100%);
}

.info-bg {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%);
}

.setting-label {
  font-size: 15px;
  font-weight: 500;
  color: #2c3e50;
}

.setting-value {
  font-size: 14px;
  color: #6b7280;
}

/* Logout Section */
.logout-section {
  margin-top: 24px;
  padding: 0 4px;
}

.logout-btn {
  width: 100%;
  height: 52px;
  font-size: 15px;
  font-weight: 600;
  border-width: 2px;
}

@media (max-width: 600px) {
  .quick-stats {
    gap: 8px;
  }

  .stat-item {
    padding: 12px 8px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
  }

  .stat-value {
    font-size: 20px;
  }
}
</style>
