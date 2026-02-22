<template>
  <q-page class="pvz-page">

    <!-- ── Mobile Header ───────────────────────────────────── -->
    <div class="pvz-page-header">
      <q-btn flat round dense icon="arrow_back" color="white" @click="$router.back()" />
      <h4 class="header-title">Профиль</h4>
      <q-btn flat round dense :icon="showMobileEdit ? 'close' : 'edit'" color="white" @click="toggleEdit" />
    </div>

    <!-- ── Desktop Title Bar ───────────────────────────────── -->
    <div class="page-titlebar">
      <div>
        <h2 class="page-titlebar__title">Профиль</h2>
        <p class="page-titlebar__sub">Управляйте своими данными</p>
      </div>
      <button :class="['edit-toggle', { 'edit-toggle--cancel': isEditing }]" @click="toggleEdit">
        <q-icon :name="isEditing ? 'close' : 'edit'" size="16px" />
        {{ isEditing ? 'Отменить' : 'Редактировать' }}
      </button>
    </div>

    <!-- ── Desktop Profile Card ────────────────────────────── -->
    <div class="profile-card">
      <div class="profile-card__identity">
        <div class="p-avatar">
          <span class="p-avatar__letter">{{ userInitial }}</span>
        </div>

        <!-- Editing -->
        <div v-if="isEditing" class="inline-edit">
          <label class="inline-edit__label">Имя пользователя</label>
          <div class="inline-edit__field">
            <q-icon name="person" size="16px" />
            <input
              ref="desktopInput"
              v-model="editForm.username"
              class="inline-edit__input"
              placeholder="Введите имя"
              maxlength="30"
              @keyup.enter="saveChanges"
            />
          </div>
          <div class="inline-edit__footer">
            <span class="inline-edit__count">{{ editForm.username.length }}/30</span>
            <button class="btn-save" :disabled="saving || !editForm.username.trim()" @click="saveChanges">
              <q-spinner-dots v-if="saving" size="14px" color="white" />
              <q-icon v-else name="check" size="14px" />
              {{ saving ? 'Сохраняем...' : 'Сохранить' }}
            </button>
          </div>
        </div>

        <!-- Viewing -->
        <div v-else class="profile-card__info">
          <h3 class="profile-card__name">{{ authStore.user?.username || 'Пользователь' }}</h3>
          <p class="profile-card__email">{{ authStore.user?.email }}</p>
          <span class="verified-badge"><q-icon name="verified" size="12px" /> Подтверждён</span>
        </div>
      </div>

      <div class="profile-card__stats">
        <div class="p-stat" v-for="s in statsItems" :key="s.label">
          <span class="p-stat__value">{{ s.value }}</span>
          <span class="p-stat__label">{{ s.label }}</span>
        </div>
      </div>
    </div>

    <!-- ── Mobile Profile Block ────────────────────────────── -->
    <div class="profile-mobile">
      <div class="p-avatar p-avatar--lg">
        <span class="p-avatar__letter">{{ userInitial }}</span>
        <div class="p-avatar__ring"></div>
      </div>
      <h3 class="profile-mobile__name">{{ authStore.user?.username || 'Пользователь' }}</h3>
      <p class="profile-mobile__email">{{ authStore.user?.email }}</p>
      <span class="verified-badge q-mb-lg"><q-icon name="verified" size="12px" /> Подтверждён</span>

      <div class="mobile-stats">
        <div class="mobile-stat" v-for="s in statsItems" :key="s.label">
          <div class="mobile-stat__icon" :class="s.iconBg">
            <q-icon :name="s.icon" size="20px" color="white" />
          </div>
          <span class="mobile-stat__value">{{ s.value }}</span>
          <span class="mobile-stat__label">{{ s.label }}</span>
        </div>
      </div>
    </div>

    <!-- ── Sections ─────────────────────────────────────────── -->
    <div class="profile-sections">

      <!-- Telegram -->
      <div class="pvz-section-card">
        <div class="section-header">
          <div class="section-icon icon-bg--telegram"><q-icon name="send" size="20px" /></div>
          <h5 class="section-title">Telegram</h5>
        </div>
        <div v-if="authStore.isTelegramLinked" class="pvz-telegram-linked">
          <div class="tg-user">
            <div class="tg-user__avatar">✈️</div>
            <div>
              <p class="tg-user__name">{{ authStore.user?.telegram_user?.nick_name }}</p>
              <p class="tg-user__handle">@{{ authStore.user?.telegram_user?.nick_name }}</p>
            </div>
          </div>
          <q-btn flat round dense icon="delete_outline" color="negative" @click="onUnlinkTelegram" />
        </div>
        <div v-else class="pvz-telegram-empty">
          <p>Привяжите Telegram для быстрого доступа к заказам</p>
          <q-btn label="Привязать аккаунт" color="info" unelevated rounded
            class="full-btn" icon="send" @click="onLinkTelegram" />
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
            <q-icon name="chevron_right" color="grey-5" />
          </div>
          <div class="setting-item" @click="onNotifications">
            <div class="setting-left">
              <div class="setting-icon-wrapper icon-bg--warning"><q-icon name="notifications" size="20px" color="warning" /></div>
              <span class="setting-label">Уведомления</span>
            </div>
            <q-icon name="chevron_right" color="grey-5" />
          </div>
          <div class="setting-item" @click="onLanguage">
            <div class="setting-left">
              <div class="setting-icon-wrapper icon-bg--info"><q-icon name="language" size="20px" color="info" /></div>
              <span class="setting-label">Язык</span>
            </div>
            <div class="setting-right">
              <span class="setting-value">Русский</span>
              <q-icon name="chevron_right" color="grey-5" />
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
            <q-icon name="chevron_right" color="grey-5" />
          </div>
          <div class="setting-item" @click="onPrivacy">
            <div class="setting-left">
              <div class="setting-icon-wrapper"><q-icon name="privacy_tip" size="20px" color="grey-7" /></div>
              <span class="setting-label">Политика конфиденциальности</span>
            </div>
            <q-icon name="chevron_right" color="grey-5" />
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
      <div class="logout-wrap">
        <q-btn label="Выйти из аккаунта" color="negative" outline rounded
          class="logout-btn" icon="logout" @click="onLogout" />
      </div>

    </div>

    <!-- ── Mobile Edit Sheet ───────────────────────────────── -->
    <q-dialog v-model="showMobileEdit" position="bottom" transition-show="slide-up" transition-hide="slide-down">
      <div class="edit-sheet">
        <div class="edit-sheet__handle"></div>
        <h5 class="edit-sheet__title">Редактировать профиль</h5>

        <div class="edit-sheet__fields">
          <div class="sheet-field">
            <label class="sheet-field__label">Имя пользователя</label>
            <div class="sheet-field__wrap">
              <q-icon name="person" size="18px" />
              <input v-model="editForm.username" class="sheet-field__input"
                placeholder="Введите имя пользователя" maxlength="30" @keyup.enter="saveChanges" />
            </div>
            <span class="sheet-field__count">{{ editForm.username.length }}/30 символов</span>
          </div>

          <div class="sheet-field">
            <label class="sheet-field__label">
              Email
              <span class="sheet-field__badge">нельзя изменить</span>
            </label>
            <div class="sheet-field__wrap sheet-field__wrap--disabled">
              <q-icon name="mail" size="18px" />
              <input :value="authStore.user?.email" class="sheet-field__input" disabled />
              <q-icon name="lock" size="14px" />
            </div>
          </div>
        </div>

        <div class="edit-sheet__actions">
          <button class="edit-sheet__cancel" @click="showMobileEdit = false">Отменить</button>
          <button class="edit-sheet__save" :disabled="saving || !editForm.username.trim()" @click="saveChanges">
            <q-spinner-dots v-if="saving" size="16px" color="white" />
            <template v-else><q-icon name="check" size="16px" /> Сохранить</template>
          </button>
        </div>
      </div>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'
import api from 'src/api/client'

const router    = useRouter()
const $q        = useQuasar()
const authStore = useAuthStore()

// ── State ────────────────────────────────────────────────────
const isEditing      = ref(false)
const saving         = ref(false)
const showMobileEdit = ref(false)
const desktopInput   = ref(null)
const windowWidth    = ref(window.innerWidth)
const editForm       = reactive({ username: '' })

// ── Computed ─────────────────────────────────────────────────
const isDesktop   = computed(() => windowWidth.value >= 1024)
const userInitial = computed(() => (authStore.user?.username || 'U').charAt(0).toUpperCase())

const statsItems = computed(() => [
  { label: 'Заказов',   value: 0, icon: 'inventory_2',    iconBg: 'icon-bg--primary' },
  { label: 'Выполнено', value: 0, icon: 'done_all',       iconBg: 'icon-bg--success' },
  { label: 'В пути',    value: 0, icon: 'local_shipping', iconBg: 'icon-bg--warning' },
])

// ── Lifecycle ────────────────────────────────────────────────
const onResize = () => { windowWidth.value = window.innerWidth }

onMounted(async () => {
  window.addEventListener('resize', onResize)
  await authStore.getMe()
  editForm.username = authStore.user?.username || ''
})

onUnmounted(() => window.removeEventListener('resize', onResize))

// ── Edit ─────────────────────────────────────────────────────
const toggleEdit = () => {
  editForm.username = authStore.user?.username || ''
  if (isDesktop.value) {
    isEditing.value = !isEditing.value
    if (isEditing.value) nextTick(() => desktopInput.value?.focus())
  } else {
    showMobileEdit.value = true
  }
}

const close = () => { isEditing.value = false; showMobileEdit.value = false }

const saveChanges = async () => {
  const name = editForm.username.trim()
  if (!name) return notify('negative', 'Имя не может быть пустым', 'error')
  if (name === authStore.user?.username) { close(); return }

  saving.value = true
  try {
    const res  = await api.patch('/auth/me/', { username: name })
    const data = await res.json()
    if (res.ok) {
      if (authStore.user) authStore.user.username = data.username
      editForm.username = data.username
      notify('positive', 'Профиль обновлён ✓', 'check_circle')
      close()
    } else {
      notify('negative', data?.username?.[0] || data?.detail || 'Ошибка сохранения', 'error')
    }
  } catch {
    notify('negative', 'Ошибка подключения', 'error')
  } finally {
    saving.value = false
  }
}

// ── Helpers ──────────────────────────────────────────────────
const notify = (color, message, icon) => $q.notify({ color, message, icon, position: 'top' })
const wip    = () => notify('info', 'Функция в разработке', 'construction')

const onLogout = () => {
  $q.dialog({
    title: 'Выход',
    message: 'Вы уверены, что хотите выйти из аккаунта?',
    cancel: { label: 'Отмена', flat: true, color: 'grey-7' },
    ok:     { label: 'Выйти', color: 'negative', unelevated: true },
    persistent: true,
  }).onOk(() => {
    authStore.logout()
    notify('positive', 'Вы вышли из аккаунта', 'check_circle')
    router.push('/login')
  })
}

const onLinkTelegram   = () => notify('info', 'Откройте бота для привязки Telegram', 'send')
const onUnlinkTelegram = () => {
  $q.dialog({
    title: 'Отвязать Telegram', message: 'Вы уверены?',
    cancel: { label: 'Отмена', flat: true, color: 'grey-7' },
    ok:     { label: 'Отвязать', color: 'negative', unelevated: true },
    persistent: true,
  }).onOk(() => notify('positive', 'Telegram отвязан', 'check_circle'))
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

// ════════════════════════════════════════════════════════════
// PROFILE PAGE — scoped
// Все цвета через var(--pvz-*) → тема меняется автоматически
// ════════════════════════════════════════════════════════════

// ─── Avatar ───────────────────────────────────────────────────

.p-avatar {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: $gradient-brand;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;

  &__letter { font-size: 22px; font-weight: 700; color: #fff; }
  &__ring   { position: absolute; inset: -7px; border-radius: 50%; border: 3px solid rgba(255,255,255,0.3); pointer-events: none; }

  &--lg {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    margin: 0 auto 12px;
    .p-avatar__letter { font-size: 36px; }
  }
}

// ─── Verified badge ───────────────────────────────────────────

.verified-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: $color-success;
  background: $color-success-bg;
  padding: 4px 10px;
  border-radius: 8px;
}

// ─── Desktop: Title bar ───────────────────────────────────────

.page-titlebar {
  display: none;
  &__title { margin: 0; font-size: 22px; font-weight: 700; color: var(--pvz-text); letter-spacing: -0.4px; }
  &__sub   { margin: 3px 0 0; font-size: 13px; color: var(--pvz-text-muted); }
}

.edit-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1.5px solid var(--pvz-border);
  background: var(--pvz-bg-card);
  color: var(--pvz-text-body);
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;

  @include hover { &:hover { border-color: $primary-start; color: $primary-start; } }
  &--cancel { border-color: #ef4444; color: #ef4444; background: rgba(239,68,68,0.06); }
}

// ─── Desktop: Profile card ────────────────────────────────────

.profile-card {
  display: none;

  &__identity { display: flex; align-items: center; gap: 20px; flex: 1; min-width: 0; }
  &__info     { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
  &__name     { margin: 0; font-size: 18px; font-weight: 700; color: var(--pvz-text); }
  &__email    { margin: 0; font-size: 13px; color: var(--pvz-text-muted); }
  &__stats    { display: flex; flex-shrink: 0; }
}

// ─── Desktop: Header stats ────────────────────────────────────

.p-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 28px;
  border-left: 1px solid var(--pvz-border);

  &__value {
    font-size: 24px;
    font-weight: 700;
    background: $gradient-brand;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  &__label { font-size: 11px; color: var(--pvz-text-muted); margin-top: 2px; }
}

// ─── Desktop: Inline edit form ────────────────────────────────

.inline-edit {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 250px;

  &__label {
    font-size: 11px;
    font-weight: 700;
    color: var(--pvz-text-hint);
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  &__field {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--pvz-bg);
    border: 1.5px solid var(--pvz-border);
    border-radius: 10px;
    padding: 0 12px;
    height: 42px;
    color: var(--pvz-text-hint);
    transition: border-color 0.2s, box-shadow 0.2s;

    &:focus-within {
      border-color: $primary-start;
      background: var(--pvz-bg-card);
      box-shadow: 0 0 0 3px rgba($primary-start, 0.1);
      color: $primary-start;
    }
  }

  &__input {
    flex: 1; border: none; background: none; outline: none;
    font-size: 15px; font-weight: 500; color: var(--pvz-text);
    font-family: inherit; min-width: 0;
    &::placeholder { color: var(--pvz-text-hint); }
  }

  &__footer { display: flex; align-items: center; justify-content: space-between; }
  &__count  { font-size: 11px; color: var(--pvz-text-hint); }
}

.btn-save {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border-radius: 7px;
  border: none;
  background: $gradient-brand;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  box-shadow: 0 2px 8px rgba($primary-start, 0.3);
  transition: all 0.2s;

  @include hover { &:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 14px rgba($primary-start, 0.4); } }
  &:disabled { opacity: 0.6; cursor: not-allowed; }
}

// ─── Mobile: Profile block ────────────────────────────────────

.profile-mobile {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 32px $page-padding-x 24px;

  &__name  { margin: 0 0 4px; color: #fff; font-size: 22px; font-weight: 700; }
  &__email { margin: 0 0 10px; color: rgba(255,255,255,0.7); font-size: 14px; }
}

.mobile-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  width: 100%;
  margin-top: 20px;
}

.mobile-stat {
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(10px);
  border-radius: $radius-lg;
  padding: 14px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;

  &__icon  { width: 40px; height: 40px; border-radius: $radius-md; display: flex; align-items: center; justify-content: center; }
  &__value { font-size: 20px; font-weight: 700; color: #fff; }
  &__label { font-size: 10px; color: rgba(255,255,255,0.7); font-weight: 500; }
}

// ─── Sections container ───────────────────────────────────────

.profile-sections {
  padding: 0 $page-padding-x;
  margin-top: 16px;
}

// ─── Telegram ─────────────────────────────────────────────────

.tg-user {
  display: flex;
  align-items: center;
  gap: 12px;

  &__avatar { width: 44px; height: 44px; border-radius: 50%; background: var(--pvz-bg-input); display: flex; align-items: center; justify-content: center; font-size: 22px; }
  &__name   { margin: 0 0 2px; font-size: 14px; font-weight: 600; color: var(--pvz-text); }
  &__handle { margin: 0; font-size: 12px; color: var(--pvz-text-muted); }
}

.full-btn   { width: 100%; height: 44px; font-weight: 600; }
.logout-wrap { margin-top: 8px; }
.logout-btn  { width: 100%; height: 50px; font-size: 15px; font-weight: 600; border-width: 2px; }

// ─── Mobile Edit Sheet ────────────────────────────────────────

.edit-sheet {
  background: var(--pvz-bg-card);
  border-radius: 24px 24px 0 0;
  padding: 12px 24px calc(32px + env(safe-area-inset-bottom, 0px));

  &__handle { width: 36px; height: 4px; background: var(--pvz-border); border-radius: 2px; margin: 0 auto 24px; }
  &__title  { margin: 0 0 28px; font-size: 19px; font-weight: 700; color: var(--pvz-text); }
  &__fields { display: flex; flex-direction: column; gap: 20px; margin-bottom: 32px; }
  &__actions { display: grid; grid-template-columns: 1fr 2fr; gap: 12px; }

  &__cancel {
    height: 54px; border-radius: 14px;
    border: 1.5px solid var(--pvz-border); background: none;
    cursor: pointer; font-size: 15px; font-weight: 600;
    color: var(--pvz-text-muted); font-family: inherit;
    transition: background 0.2s;
    &:active { background: var(--pvz-bg); }
  }

  &__save {
    height: 54px; border-radius: 14px; border: none;
    background: $gradient-brand; color: #fff;
    cursor: pointer; font-size: 15px; font-weight: 600;
    font-family: inherit;
    display: flex; align-items: center; justify-content: center; gap: 8px;
    box-shadow: 0 4px 16px rgba($primary-start, 0.3);
    transition: all 0.2s;
    &:active:not(:disabled) { transform: scale(0.97); }
    &:disabled { opacity: 0.55; cursor: not-allowed; }
  }
}

// ─── Sheet fields ─────────────────────────────────────────────

.sheet-field {
  display: flex;
  flex-direction: column;
  gap: 8px;

  &__label {
    display: flex; align-items: center; gap: 8px;
    font-size: 12px; font-weight: 700; color: var(--pvz-text-muted);
    text-transform: uppercase; letter-spacing: 0.7px;
  }

  &__badge {
    font-size: 10px; font-weight: 600;
    color: var(--pvz-text-hint); background: var(--pvz-bg);
    padding: 2px 8px; border-radius: 4px;
    text-transform: none; letter-spacing: 0;
  }

  &__wrap {
    display: flex; align-items: center; gap: 10px;
    background: var(--pvz-bg); border: 1.5px solid var(--pvz-border);
    border-radius: 14px; padding: 0 16px; height: 56px;
    color: var(--pvz-text-hint);
    transition: border-color 0.2s, box-shadow 0.2s;

    &:focus-within {
      border-color: $primary-start; background: var(--pvz-bg-card);
      box-shadow: 0 0 0 3px rgba($primary-start, 0.12); color: $primary-start;
    }

    &--disabled {
      opacity: 0.55; cursor: not-allowed;
      &:focus-within { border-color: var(--pvz-border); background: var(--pvz-bg); box-shadow: none; }
    }
  }

  &__input {
    flex: 1; border: none; background: none; outline: none;
    font-size: 16px; font-weight: 500; color: var(--pvz-text); font-family: inherit;
    &::placeholder { color: var(--pvz-text-hint); }
    &:disabled     { cursor: not-allowed; color: var(--pvz-text-muted); }
  }

  &__count { font-size: 11px; color: var(--pvz-text-hint); text-align: right; }
}

// ─── Desktop overrides ────────────────────────────────────────

@include desktop {
  .profile-mobile { display: none; }

  .page-titlebar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px $page-padding-x-lg 0;
    max-width: 900px;
    margin: 0 auto;
    width: 100%;
  }

  .profile-card {
    display: flex;
    align-items: center;
    background: var(--pvz-bg-card);
    border: 1px solid var(--pvz-border);
    border-radius: $radius-xl;
    padding: 24px 28px;
    max-width: 900px;
    margin: 16px auto 0;
    width: calc(100% - #{$page-padding-x-lg * 2});
    box-shadow: var(--pvz-shadow-card);
    transition: box-shadow 0.2s;
  }

  .profile-sections {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    padding: 16px $page-padding-x-lg 40px;
    max-width: 900px;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;

    > .pvz-section-card:first-child,
    .logout-wrap { grid-column: 1 / -1; }
    .logout-wrap { margin-top: 0; }
    .logout-btn  { max-width: 220px; }
  }

  .pvz-section-card {
    margin-bottom: 0 !important;
    transition: box-shadow 0.2s;
    @include hover { &:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important; } }
  }
}
</style>