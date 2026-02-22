<template>
  <q-page class="pvz-page">

    <!-- Mobile header -->
    <div class="pvz-page-header">
      <q-btn flat round dense icon="arrow_back" color="white" size="md" @click="$router.back()" />
      <h4 class="header-title">Профиль</h4>
      <q-btn
        flat round dense
        :icon="showMobileEdit ? 'close' : 'edit'"
        color="white"
        size="md"
        @click="toggleEdit"
      />
    </div>

    <!-- Desktop page title + edit button -->
    <div class="desktop-profile-title">
      <div>
        <h2>Профиль</h2>
        <p class="desktop-profile-subtitle">Управляйте своими данными</p>
      </div>
      <button
        :class="['desktop-edit-btn', { 'desktop-edit-btn--active': isEditing }]"
        @click="toggleEdit"
      >
        <q-icon :name="isEditing ? 'close' : 'edit'" size="16px" />
        {{ isEditing ? 'Отменить' : 'Редактировать' }}
      </button>
    </div>

    <!-- Desktop: горизонтальная шапка профиля -->
    <div class="profile-desktop-header">
      <div class="pvz-avatar">
        <div class="avatar-wrap">
          <div class="pvz-avatar__circle">
            <span class="pvz-avatar__letter">
              {{ (editForm.username || authStore.user?.username)?.charAt(0).toUpperCase() || 'U' }}
            </span>
          </div>
          <div class="pvz-avatar__ring"></div>
        </div>

        <div class="pvz-avatar__meta">
          <!-- Edit mode -->
          <div v-if="isEditing" class="desktop-edit-form">
            <div class="edit-field-group">
              <label class="edit-label">Имя пользователя</label>
              <div class="edit-input-wrap">
                <q-icon name="person" size="16px" color="grey-5" />
                <input
                  v-model="editForm.username"
                  class="edit-input"
                  placeholder="Введите имя"
                  maxlength="30"
                  @keyup.enter="saveChanges"
                  ref="desktopInput"
                />
              </div>
              <span class="edit-char-count">{{ editForm.username.length }}/30</span>
            </div>
            <div class="desktop-edit-actions">
              <button class="save-btn" :disabled="saving || !editForm.username.trim()" @click="saveChanges">
                <q-spinner-dots v-if="saving" size="14px" color="white" />
                <q-icon v-else name="check" size="14px" />
                {{ saving ? 'Сохраняем...' : 'Сохранить' }}
              </button>
            </div>
          </div>

          <!-- View mode -->
          <template v-else>
            <h3 class="pvz-avatar__name">{{ authStore.user?.username || 'Пользователь' }}</h3>
            <p class="pvz-avatar__email">{{ authStore.user?.email }}</p>
            <q-badge v-if="authStore.user?.email" color="positive" label="Подтверждён" class="verify-badge">
              <q-icon name="verified" size="14px" class="q-ml-xs" />
            </q-badge>
          </template>
        </div>
      </div>

      <!-- Stats в шапке -->
      <div class="pvz-quick-stats">
        <div class="stat-item">
          <div class="stat-value">{{ getTotalOrders() }}</div>
          <div class="stat-label">Заказов</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ getCompletedOrders() }}</div>
          <div class="stat-label">Выполнено</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ getActiveOrders() }}</div>
          <div class="stat-label">В пути</div>
        </div>
      </div>
    </div>

    <!-- Mobile: avatar + quick stats -->
    <div class="profile-mobile-header">
      <div class="pvz-avatar">
        <div class="avatar-wrap" style="margin-bottom: 16px;">
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

    <!-- Sections -->
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

    <!-- ═══════════════════════════════════════════════════════
         MOBILE BOTTOM SHEET — редактирование профиля
    ════════════════════════════════════════════════════════ -->
    <q-dialog
      v-model="showMobileEdit"
      position="bottom"
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <div class="mobile-edit-sheet">
        <div class="mobile-edit-sheet__handle"></div>
        <h5 class="mobile-edit-sheet__title">Редактировать профиль</h5>

        <div class="mobile-edit-sheet__fields">
          <!-- Username -->
          <div class="sheet-field">
            <label class="sheet-label">Имя пользователя</label>
            <div class="sheet-input-wrap">
              <q-icon name="person" size="18px" color="grey-5" />
              <input
                v-model="editForm.username"
                class="sheet-input"
                placeholder="Введите имя пользователя"
                maxlength="30"
                @keyup.enter="saveChanges"
              />
            </div>
            <span class="sheet-char-count">{{ editForm.username.length }}/30 символов</span>
          </div>

          <!-- Email (readonly — не редактируется) -->
          <div class="sheet-field">
            <label class="sheet-label">Email <span class="sheet-readonly-tag">нельзя изменить</span></label>
            <div class="sheet-input-wrap sheet-input-wrap--readonly">
              <q-icon name="mail" size="18px" color="grey-5" />
              <input
                :value="authStore.user?.email"
                class="sheet-input"
                disabled
              />
              <q-icon name="lock" size="14px" color="grey-5" />
            </div>
          </div>
        </div>

        <div class="mobile-edit-sheet__actions">
          <button class="sheet-cancel-btn" @click="showMobileEdit = false">Отменить</button>
          <button
            class="sheet-save-btn"
            :disabled="saving || !editForm.username.trim()"
            @click="saveChanges"
          >
            <q-spinner-dots v-if="saving" size="16px" color="white" />
            <template v-else>
              <q-icon name="check" size="16px" />
              Сохранить
            </template>
          </button>
        </div>
      </div>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'
import api from 'src/api/client'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const isEditing = ref(false)
const saving = ref(false)
const showMobileEdit = ref(false)
const desktopInput = ref(null)
const windowWidth = ref(window.innerWidth)
const isDesktop = computed(() => windowWidth.value >= 1024)

const editForm = reactive({ username: '' })

onMounted(async () => {
  window.addEventListener('resize', () => { windowWidth.value = window.innerWidth })
  await authStore.getMe()
  editForm.username = authStore.user?.username || ''
})

const toggleEdit = () => {
  editForm.username = authStore.user?.username || ''
  if (isDesktop.value) {
    isEditing.value = !isEditing.value
    if (isEditing.value) nextTick(() => desktopInput.value?.focus())
  } else {
    showMobileEdit.value = true
  }
}

const saveChanges = async () => {
  const trimmed = editForm.username.trim()
  if (!trimmed) {
    $q.notify({ color: 'negative', message: 'Имя не может быть пустым', position: 'top', icon: 'error' })
    return
  }
  // Ничего не менялось
  if (trimmed === authStore.user?.username) {
    isEditing.value = false
    showMobileEdit.value = false
    return
  }

  saving.value = true
  try {
    const res = await api.patch('/auth/me/', { username: trimmed })
    if (res.ok) {
      const updated = await res.json()
      if (authStore.user) authStore.user.username = updated.username
      editForm.username = updated.username
      $q.notify({ color: 'positive', message: 'Профиль обновлён ✓', position: 'top', icon: 'check_circle' })
      isEditing.value = false
      showMobileEdit.value = false
    } else {
      const err = await res.json()
      const msg = err?.username?.[0] || err?.detail || 'Ошибка сохранения'
      $q.notify({ color: 'negative', message: msg, position: 'top', icon: 'error' })
    }
  } catch {
    $q.notify({ color: 'negative', message: 'Ошибка подключения', position: 'top', icon: 'error' })
  } finally {
    saving.value = false
  }
}

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
  }).onOk(() => {
    authStore.logout()
    $q.notify({ color: 'positive', message: 'Вы вышли из аккаунта', position: 'top', icon: 'check_circle' })
    router.push('/login')
  })
}

const onLinkTelegram = () =>
  $q.notify({ color: 'info', message: 'Откройте бота для привязки Telegram', position: 'top', icon: 'send' })

const onUnlinkTelegram = () => {
  $q.dialog({
    title: 'Отвязать Telegram', message: 'Вы уверены?',
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

// ─── Mobile base ─────────────────────────────────────────────

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

.avatar-wrap { position: relative; display: inline-block; }

.tg-user   { display: flex; align-items: center; gap: 12px; }
.tg-avatar { width: 48px; height: 48px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.tg-name   { margin: 0 0 2px; font-size: 15px; font-weight: 600; color: $color-text-dark; }
.tg-handle { margin: 0; font-size: 13px; color: $color-text-muted; }
.tg-link-btn { width: 100%; height: 44px; font-weight: 600; }

.logout-section { margin-top: 24px; padding: 0 4px; }
.logout-btn     { width: 100%; height: 52px; font-size: 15px; font-weight: 600; border-width: 2px; }

// Desktop блоки скрыты на мобиле
.profile-desktop-header { display: none; }
.desktop-profile-title  { display: none; }
// Mobile блок виден
.profile-mobile-header  { display: block; }

// ─── Mobile Bottom Sheet ──────────────────────────────────────

.mobile-edit-sheet {
  background: white;
  border-radius: 24px 24px 0 0;
  padding: 12px 24px;
  padding-bottom: calc(32px + env(safe-area-inset-bottom, 0px));

  &__handle {
    width: 36px; height: 4px;
    background: $color-border;
    border-radius: 2px;
    margin: 0 auto 24px;
  }

  &__title {
    margin: 0 0 28px;
    font-size: 19px;
    font-weight: 700;
    color: $color-text-dark;
  }

  &__fields { display: flex; flex-direction: column; gap: 20px; margin-bottom: 32px; }

  &__actions {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 12px;
  }
}

.sheet-field { display: flex; flex-direction: column; gap: 8px; }

.sheet-label {
  font-size: 12px;
  font-weight: 700;
  color: $color-text-muted;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.sheet-readonly-tag {
  font-size: 10px;
  font-weight: 600;
  color: $color-text-hint;
  background: $color-bg-page;
  padding: 2px 8px;
  border-radius: 4px;
  text-transform: none;
  letter-spacing: 0;
}

.sheet-input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  background: $color-bg-page;
  border: 1.5px solid $color-border;
  border-radius: 14px;
  padding: 0 16px;
  height: 56px;
  transition: border-color 0.2s, box-shadow 0.2s;

  &:focus-within {
    border-color: $primary-start;
    background: white;
    box-shadow: 0 0 0 3px rgba($primary-start, 0.12);
  }

  &--readonly {
    opacity: 0.6;
    cursor: not-allowed;
    &:focus-within {
      border-color: $color-border;
      background: $color-bg-page;
      box-shadow: none;
    }
  }
}

.sheet-input {
  flex: 1;
  border: none;
  background: none;
  outline: none;
  font-size: 16px;
  font-weight: 500;
  color: $color-text-dark;
  font-family: inherit;

  &::placeholder { color: $color-text-hint; }
  &:disabled { cursor: not-allowed; color: $color-text-muted; }
}

.sheet-char-count {
  font-size: 11px;
  color: $color-text-hint;
  text-align: right;
}

.sheet-cancel-btn {
  height: 56px;
  border-radius: 14px;
  border: 1.5px solid $color-border;
  background: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  color: $color-text-muted;
  transition: all 0.2s;

  &:active { background: $color-bg-page; }
}

.sheet-save-btn {
  height: 56px;
  border-radius: 14px;
  border: none;
  background: $gradient-brand;
  color: white;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba($primary-start, 0.3);
  transition: all 0.2s;

  &:active:not(:disabled) { transform: scale(0.97); }
  &:disabled { opacity: 0.55; cursor: not-allowed; }
}

// ─── Desktop ──────────────────────────────────────────────────

@include desktop {

  .profile-mobile-header { display: none; }

  // Page title bar
  .desktop-profile-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px 32px 0;
    max-width: 900px;
    margin: 0 auto;
    width: 100%;

    h2 {
      margin: 0;
      font-size: 22px;
      font-weight: 700;
      color: $color-text-dark;
      letter-spacing: -0.4px;
    }
  }

  .desktop-profile-subtitle {
    margin: 3px 0 0;
    font-size: 13px;
    color: $color-text-muted;
  }

  // Edit toggle button
  .desktop-edit-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 8px;
    border: 1.5px solid $color-border;
    background: white;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    color: $color-text-body;
    transition: all 0.2s;
    font-family: inherit;

    @include hover {
      &:hover {
        border-color: $primary-start;
        color: $primary-start;
      }
    }

    &--active {
      border-color: #ef4444;
      color: #ef4444;
      background: rgba(239, 68, 68, 0.04);
    }
  }

  // Header card
  .profile-desktop-header {
    display: flex;
    align-items: center;
    background: white;
    border: 1px solid $color-border;
    border-radius: $radius-xl;
    padding: 24px 28px;
    max-width: 900px;
    margin: 16px auto 0;
    width: calc(100% - 64px);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    gap: 0;
    transition: box-shadow 0.2s;

    .pvz-avatar {
      display: flex;
      align-items: center;
      gap: 20px;
      text-align: left;
      flex: 1;
      margin-bottom: 0;

      .pvz-avatar__circle {
        width: 64px !important;
        height: 64px !important;
        border-radius: 16px !important;
        margin: 0 !important;
        flex-shrink: 0;
      }
      .pvz-avatar__letter { font-size: 26px !important; }
      .pvz-avatar__ring   { display: none; }
      .pvz-avatar__meta   { display: flex; flex-direction: column; flex: 1; min-width: 0; }
      .pvz-avatar__name   { margin: 0 0 2px !important; font-size: 18px !important; color: $color-text-dark !important; }
      .pvz-avatar__email  { margin: 0 0 6px !important; color: $color-text-muted !important; }
    }

    // Stats
    .pvz-quick-stats {
      display: flex !important;
      background: none !important;
      padding: 0 !important;
      margin: 0 !important;
      box-shadow: none !important;
      border-radius: 0 !important;
      gap: 0;
      flex-shrink: 0;

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

  // Inline edit form
  .desktop-edit-form {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 260px;
  }

  .edit-field-group { display: flex; flex-direction: column; gap: 6px; }

  .edit-label {
    font-size: 11px;
    font-weight: 700;
    color: $color-text-hint;
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  .edit-input-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
    background: $color-bg-page;
    border: 1.5px solid $color-border;
    border-radius: 10px;
    padding: 0 12px;
    height: 42px;
    transition: border-color 0.2s, box-shadow 0.2s;

    &:focus-within {
      border-color: $primary-start;
      background: white;
      box-shadow: 0 0 0 3px rgba($primary-start, 0.1);
    }
  }

  .edit-input {
    flex: 1;
    border: none;
    background: none;
    outline: none;
    font-size: 15px;
    font-weight: 500;
    color: $color-text-dark;
    font-family: inherit;
    min-width: 0;

    &::placeholder { color: $color-text-hint; }
  }

  .edit-char-count {
    font-size: 11px;
    color: $color-text-hint;
    text-align: right;
  }

  .desktop-edit-actions { margin-top: 4px; }

  .save-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 8px;
    border: none;
    background: $gradient-brand;
    color: white;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba($primary-start, 0.3);
    font-family: inherit;
    transition: all 0.2s;

    @include hover {
      &:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba($primary-start, 0.4);
      }
    }

    &:disabled { opacity: 0.6; cursor: not-allowed; transform: none !important; }
  }

  // Grid
  .profile-container {
    display: grid !important;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    padding: 16px 32px 40px !important;
    max-width: 900px;
    margin: 0 auto !important;
    width: 100%;

    > .pvz-section-card:first-child,
    .logout-section { grid-column: 1 / -1; }
    .logout-section { margin-top: 0; }
  }

  .logout-btn { max-width: 220px !important; margin: 0 !important; }

  .pvz-section-card {
    margin-bottom: 0 !important;
    transition: box-shadow 0.2s;
    @include hover { &:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important; } }
  }
}
</style>