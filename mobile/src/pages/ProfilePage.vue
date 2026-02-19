<template>
  <q-page class="pvz-page">

    <!-- Mobile header -->
    <div class="pvz-page-header">
      <q-btn flat round dense icon="arrow_back" color="white" size="md" @click="$router.back()" />
      <h4 class="header-title">Профиль</h4>
      <div class="header-spacer"></div>
    </div>

    <!-- Desktop page title -->
    <div class="desktop-profile-title">
      <h2>Профиль</h2>
    </div>

    <!-- Desktop: горизонтальная шапка -->
    <div class="profile-desktop-header">
      <div class="pvz-avatar">
        <div style="position:relative; display:inline-block;">
          <div class="pvz-avatar__circle">
            <span class="pvz-avatar__letter">
              {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
            </span>
          </div>
          <div class="pvz-avatar__ring"></div>
        </div>
        <div class="pvz-avatar__meta">
          <h3 class="pvz-avatar__name">{{ authStore.user?.username || 'Пользователь' }}</h3>
          <p class="pvz-avatar__email">{{ authStore.user?.email }}</p>
          <q-badge v-if="authStore.user?.email" color="positive" label="Подтверждён" class="verify-badge">
            <q-icon name="verified" size="14px" class="q-ml-xs" />
          </q-badge>
        </div>
      </div>

      <div class="pvz-quick-stats">
        <div class="stat-item">
          <div class="stat-icon icon-bg--primary"><q-icon name="inventory_2" size="24px" color="white" /></div>
          <div class="stat-value">{{ getTotalOrders() }}</div>
          <div class="stat-label">Заказов</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon icon-bg--success"><q-icon name="done_all" size="24px" color="white" /></div>
          <div class="stat-value">{{ getCompletedOrders() }}</div>
          <div class="stat-label">Выполнено</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon icon-bg--warning"><q-icon name="local_shipping" size="24px" color="white" /></div>
          <div class="stat-value">{{ getActiveOrders() }}</div>
          <div class="stat-label">В пути</div>
        </div>
      </div>
    </div>

    <!-- Mobile only: avatar + quick stats отдельно -->
    <div class="profile-mobile-header">
      <div class="pvz-avatar">
        <div style="position:relative; display:inline-block; margin-bottom: 16px;">
          <div class="pvz-avatar__circle">
            <span class="pvz-avatar__letter">
              {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
            </span>
          </div>
          <div class="pvz-avatar__ring"></div>
        </div>
        <h3 class="pvz-avatar__name">{{ authStore.user?.username || 'Пользователь' }}</h3>
        <p class="pvz-avatar__email">{{ authStore.user?.email }}</p>
        <q-badge v-if="authStore.user?.email" color="positive" label="Подтверждён" class="verify-badge">
          <q-icon name="verified" size="14px" class="q-ml-xs" />
        </q-badge>
      </div>
      <div class="pvz-quick-stats">
        <div class="stat-item">
          <div class="stat-icon icon-bg--primary"><q-icon name="inventory_2" size="24px" color="white" /></div>
          <div class="stat-value">{{ getTotalOrders() }}</div>
          <div class="stat-label">Заказов</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon icon-bg--success"><q-icon name="done_all" size="24px" color="white" /></div>
          <div class="stat-value">{{ getCompletedOrders() }}</div>
          <div class="stat-label">Выполнено</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon icon-bg--warning"><q-icon name="local_shipping" size="24px" color="white" /></div>
          <div class="stat-value">{{ getActiveOrders() }}</div>
          <div class="stat-label">В пути</div>
        </div>
      </div>
    </div>

    <!-- Sections grid -->
    <div class="profile-container">

      <!-- Telegram -->
      <div class="pvz-section-card">
        <div class="section-header">
          <div class="section-icon icon-bg--telegram"><q-icon name="send" size="20px" /></div>
          <h5 class="section-title">Telegram</h5>
        </div>
        <div v-if="authStore.isTelegramLinked" class="pvz-telegram-linked">
          <div class="tg-user">
            <div class="tg-avatar">✈️</div>
            <div>
              <p class="tg-name">{{ authStore.user?.telegram_user?.nick_name }}</p>
              <p class="tg-handle">@{{ authStore.user?.telegram_user?.nick_name }}</p>
            </div>
          </div>
          <q-btn flat round dense icon="delete_outline" color="negative" @click="onUnlinkTelegram" />
        </div>
        <div v-else class="pvz-telegram-empty">
          <p>Привяжите Telegram для быстрого доступа к заказам</p>
          <q-btn label="Привязать аккаунт" color="info" unelevated rounded class="tg-link-btn" icon="send" @click="onLinkTelegram" />
        </div>
      </div>

      <!-- Settings -->
      <div class="pvz-section-card">
        <div class="section-header">
          <div class="section-icon icon-bg--settings"><q-icon name="settings" size="20px" /></div>
          <h5 class="section-title">Настройки</h5>
        </div>
        <div class="pvz-settings-list">
          <div class="setting-item" @click="onChangePassword">
            <div class="setting-left">
              <div class="setting-icon-wrapper icon-bg--primary"><q-icon name="lock" size="20px" color="primary" /></div>
              <span class="setting-label">Изменить пароль</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>
          <div class="setting-item" @click="onNotifications">
            <div class="setting-left">
              <div class="setting-icon-wrapper icon-bg--warning"><q-icon name="notifications" size="20px" color="warning" /></div>
              <span class="setting-label">Уведомления</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>
          <div class="setting-item" @click="onLanguage">
            <div class="setting-left">
              <div class="setting-icon-wrapper icon-bg--info"><q-icon name="language" size="20px" color="info" /></div>
              <span class="setting-label">Язык</span>
            </div>
            <div class="setting-right">
              <span class="setting-value">Русский</span>
              <q-icon name="chevron_right" size="20px" color="grey-5" />
            </div>
          </div>
        </div>
      </div>

      <!-- About -->
      <div class="pvz-section-card">
        <div class="section-header">
          <div class="section-icon icon-bg--about"><q-icon name="info" size="20px" /></div>
          <h5 class="section-title">О приложении</h5>
        </div>
        <div class="pvz-settings-list">
          <div class="setting-item" @click="onHelp">
            <div class="setting-left">
              <div class="setting-icon-wrapper"><q-icon name="help_outline" size="20px" color="grey-7" /></div>
              <span class="setting-label">Помощь</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>
          <div class="setting-item" @click="onPrivacy">
            <div class="setting-left">
              <div class="setting-icon-wrapper"><q-icon name="privacy_tip" size="20px" color="grey-7" /></div>
              <span class="setting-label">Политика конфиденциальности</span>
            </div>
            <q-icon name="chevron_right" size="20px" color="grey-5" />
          </div>
          <div class="setting-item">
            <div class="setting-left">
              <div class="setting-icon-wrapper"><q-icon name="info_outline" size="20px" color="grey-7" /></div>
              <span class="setting-label">Версия</span>
            </div>
            <span class="setting-value">1.0.0</span>
          </div>
        </div>
      </div>

      <!-- Logout -->
      <div class="logout-section">
        <q-btn label="Выйти из аккаунта" color="negative" outline rounded
          class="logout-btn" icon="logout" @click="onLogout" />
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

onMounted(() => authStore.getMe())

const getTotalOrders    = () => 0
const getCompletedOrders = () => 0
const getActiveOrders   = () => 0

const wip = () => $q.notify({ color: 'info', message: 'Функция в разработке', position: 'top' })

const onLogout = () => {
  $q.dialog({
    title: 'Выход',
    message: 'Вы уверены, что хотите выйти из аккаунта?',
    cancel: { label: 'Отмена', flat: true, color: 'grey-7' },
    ok:     { label: 'Выйти', color: 'negative', unelevated: true },
    persistent: true,
  }).onOk(() => { authStore.logout(); $q.notify({ color: 'positive', message: 'Вы вышли из аккаунта', position: 'top', icon: 'check_circle' }); router.push('/login') })
}

const onLinkTelegram = () => $q.notify({ color: 'info', message: 'Откройте бота для привязки Telegram', position: 'top', icon: 'send' })
const onUnlinkTelegram = () => {
  $q.dialog({
    title: 'Отвязать Telegram',
    message: 'Вы уверены?',
    cancel: { label: 'Отмена', flat: true, color: 'grey-7' },
    ok:     { label: 'Отвязать', color: 'negative', unelevated: true },
    persistent: true,
  }).onOk(() => $q.notify({ color: 'positive', message: 'Telegram отвязан', position: 'top', icon: 'check_circle' }))
}

const onChangePassword = wip
const onNotifications  = wip
const onLanguage       = wip
const onHelp           = wip
const onPrivacy        = wip
</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;
@use 'src/css/mixins' as *;

// Mobile
.profile-container {
  padding: 0 16px;
  margin-top: 20px;
}

.verify-badge {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.tg-user   { display: flex; align-items: center; gap: 12px; }
.tg-avatar { width: 48px; height: 48px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.tg-name   { margin: 0 0 2px; font-size: 15px; font-weight: 600; color: #2c3e50; }
.tg-handle { margin: 0; font-size: 13px; color: #6b7280; }
.tg-link-btn { width: 100%; height: 44px; font-weight: 600; }

.logout-section { margin-top: 24px; padding: 0 4px; }
.logout-btn     { width: 100%; height: 52px; font-size: 15px; font-weight: 600; border-width: 2px; }

// Desktop-only блок скрыт на мобиле
.profile-desktop-header { display: none; }
.desktop-profile-title  { display: none; }

// Mobile-only блок
.profile-mobile-header { display: block; }

// ── Desktop ───────────────────────────────────────────────────
@include desktop {

  // Скрываем мобильный блок, показываем десктопный
  .profile-mobile-header { display: none; }

  .desktop-profile-title {
    display: block;
    font-size: 22px;
    font-weight: 700;
    color: $color-text-dark;
    letter-spacing: -0.4px;
    padding: 28px 32px 0;
    max-width: 900px;
    margin: 0 auto;
    width: 100%;

    h2 { margin: 0; font-size: 22px; font-weight: 700; }
  }

  .profile-desktop-header {
    display: flex;
    align-items: center;
    gap: 0;
    background: #fff;
    border: 1px solid $color-border;
    border-radius: $radius-xl;
    padding: 24px 28px;
    max-width: 900px;
    margin: 16px auto 0;
    width: calc(100% - 64px);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);

    .pvz-avatar {
      display: flex;
      align-items: center;
      gap: 16px;
      text-align: left;
      flex: 1;
      margin-bottom: 0;

      &__circle {
        width: 64px !important;
        height: 64px !important;
        border-radius: 16px !important;
        margin: 0 !important;
      }
      &__letter { font-size: 26px !important; }
      &__ring   { display: none; }

      &__meta { display: flex; flex-direction: column; }

      &__name  { margin: 0 0 2px !important; font-size: 18px !important; color: $color-text-dark !important; }
      &__email { margin: 0 0 6px !important; color: $color-text-muted !important; }
    }

    .pvz-quick-stats {
      display: flex !important;
      background: none !important;
      padding: 0 !important;
      margin: 0 !important;
      box-shadow: none !important;
      border-radius: 0 !important;
      gap: 0;

      .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 8px 28px;
        border-left: 1px solid $color-border;
        background: none !important;
        border-radius: 0 !important;
      }

      .stat-icon { display: none; }

      .stat-value {
        font-size: 24px !important;
        font-weight: 700 !important;
        background: $gradient-brand;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent !important;
      }

      .stat-label {
        font-size: 11px !important;
        color: $color-text-muted !important;
        margin-top: 2px;
      }
    }
  }

  .profile-container {
    display: grid !important;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    padding: 16px 32px 32px !important;
    max-width: 900px;
    margin: 0 auto !important;
    width: 100%;

    // Телеграм — полная ширина
    > .pvz-section-card:first-child { grid-column: 1 / -1; }

    // Кнопка выхода — полная ширина
    .logout-section { grid-column: 1 / -1; margin-top: 0; }
  }

  .logout-btn {
    max-width: 240px !important;
    margin: 0 !important;
  }
}
</style>