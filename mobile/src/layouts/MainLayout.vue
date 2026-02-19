<template>
  <q-layout view="lHh LpR lFf" class="pvz-layout">

    <!-- ═══════════════════════════════════════════════════════
         DESKTOP SIDEBAR
    ════════════════════════════════════════════════════════ -->
    <q-drawer
      v-if="isDesktop"
      :model-value="true"
      :width="240"
      :breakpoint="0"
      class="pvz-sidebar"
    >
      <!-- Logo -->
      <div class="pvz-sidebar__logo">
        <div class="pvz-sidebar__logo-mark">🛍️</div>
        <div class="pvz-sidebar__logo-text">
          <span class="pvz-sidebar__logo-title">PVZ Bot</span>
          <span class="pvz-sidebar__logo-tag">beta</span>
        </div>
      </div>

      <!-- Nav -->
      <nav class="pvz-sidebar__nav">
        <p class="pvz-sidebar__nav-label">Навигация</p>

        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          custom
          v-slot="{ isExactActive, navigate }"
        >
          <div
            :class="['pvz-sidebar__item', { 'pvz-sidebar__item--active': isExactActive }]"
            @click="navigate"
          >
            <div class="pvz-sidebar__item-icon">
              <q-icon :name="item.icon" size="18px" />
            </div>
            <span class="pvz-sidebar__item-label">{{ item.label }}</span>
            <div v-if="item.badge && getCount() > 0" class="pvz-sidebar__badge">
              {{ getCount() }}
            </div>
          </div>
        </router-link>
      </nav>

      <!-- Create CTA -->
      <div class="pvz-sidebar__cta">
        <router-link to="/add" custom v-slot="{ navigate }">
          <button class="pvz-sidebar__cta-btn" @click="navigate">
            <q-icon name="add" size="18px" />
            <span>Создать заказ</span>
          </button>
        </router-link>
      </div>

      <!-- Spacer -->
      <div style="flex: 1" />

      <!-- User block -->
      <div class="pvz-sidebar__user" v-if="auth.user">
        <div class="pvz-sidebar__user-avatar">
          {{ auth.user.username?.charAt(0).toUpperCase() || 'U' }}
        </div>
        <div class="pvz-sidebar__user-info">
          <span class="pvz-sidebar__user-name">{{ auth.user.username }}</span>
          <span class="pvz-sidebar__user-email">{{ auth.user.email }}</span>
        </div>
        <button class="pvz-sidebar__user-logout" @click="onLogout" title="Выйти">
          <q-icon name="logout" size="16px" />
        </button>
      </div>
    </q-drawer>

    <!-- ═══════════════════════════════════════════════════════
         MOBILE HEADER
    ════════════════════════════════════════════════════════ -->
    <q-header v-if="!isDesktop" class="pvz-mobile-header">
      <q-toolbar>
        <q-toolbar-title class="pvz-mobile-header__title">
          {{ currentPageTitle }}
        </q-toolbar-title>
        <router-link to="/profile">
          <q-btn flat round dense icon="account_circle" color="white" size="md" />
        </router-link>
      </q-toolbar>
    </q-header>

    <!-- ═══════════════════════════════════════════════════════
         CONTENT
    ════════════════════════════════════════════════════════ -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- ═══════════════════════════════════════════════════════
         MOBILE BOTTOM NAV
    ════════════════════════════════════════════════════════ -->
    <q-footer v-if="!isDesktop" class="pvz-bottom-nav">
      <div class="pvz-bottom-tabs">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          custom
          v-slot="{ isExactActive, navigate }"
        >
          <button
            :class="['pvz-bottom-tab', { 'pvz-bottom-tab--active': isExactActive }]"
            @click="navigate"
          >
            <q-icon :name="isExactActive ? item.iconActive : item.icon" size="22px" />
            <span>{{ item.label }}</span>
          </button>
        </router-link>
      </div>
    </q-footer>

  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'

const $q = useQuasar()
const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const windowWidth = ref(window.innerWidth)
const isDesktop = computed(() => windowWidth.value >= 1024)

const navItems = [
  { to: '/',        label: 'Заказы',    icon: 'inbox',      iconActive: 'inbox',      badge: true },
  { to: '/profile', label: 'Профиль',   icon: 'person',     iconActive: 'person',     badge: false },
]

const pageTitles = { '/': 'Мои заказы', '/add': 'Создать заказ', '/profile': 'Профиль' }
const currentPageTitle = computed(() => pageTitles[route.path] || 'PVZ Bot')

const getCount = () => 0

const onLogout = () => {
  $q.dialog({
    title: 'Выход',
    message: 'Вы уверены, что хотите выйти?',
    cancel: { label: 'Отмена', flat: true, color: 'grey-7' },
    ok:     { label: 'Выйти', color: 'negative', unelevated: true },
    persistent: true,
  }).onOk(() => { auth.logout(); router.push('/login') })
}

const onResize = () => { windowWidth.value = window.innerWidth }
onMounted(async () => { window.addEventListener('resize', onResize); await auth.getMe() })
onUnmounted(() => window.removeEventListener('resize', onResize))
</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;
@use 'src/css/mixins' as *;

// ─── Layout ──────────────────────────────────────────────────

.pvz-layout { overflow: hidden; }

// ─── SIDEBAR ─────────────────────────────────────────────────

.pvz-sidebar {
  background: #0e0e14 !important;
  display: flex;
  flex-direction: column;
  padding: 0;
  border-right: 1px solid rgba(255,255,255,0.06) !important;

  // Тонкая вертикальная полоска бренда сверху
  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, $primary-start, $primary-end);
  }
}

.pvz-sidebar__logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  margin-bottom: 8px;
}

.pvz-sidebar__logo-mark {
  font-size: 26px;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea22, #764ba222);
  border: 1px solid rgba(102,126,234,0.3);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.pvz-sidebar__logo-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pvz-sidebar__logo-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
}

.pvz-sidebar__logo-tag {
  font-size: 10px;
  font-weight: 600;
  color: $primary-start;
  background: rgba(102,126,234,0.15);
  border: 1px solid rgba(102,126,234,0.25);
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

// Nav
.pvz-sidebar__nav {
  padding: 8px 12px;
  flex: 0;
}

.pvz-sidebar__nav-label {
  font-size: 10px;
  font-weight: 700;
  color: rgba(255,255,255,0.25);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin: 8px 8px 6px;
}

.pvz-sidebar__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  margin-bottom: 2px;
  position: relative;

  &:hover:not(&--active) {
    background: rgba(255,255,255,0.05);
  }

  &--active {
    background: rgba(102,126,234,0.15);

    .pvz-sidebar__item-icon { color: $primary-start; }
    .pvz-sidebar__item-label { color: #fff; font-weight: 600; }

    // Левая полоска
    &::before {
      content: '';
      position: absolute;
      left: 0; top: 50%;
      transform: translateY(-50%);
      width: 3px; height: 60%;
      background: $primary-start;
      border-radius: 0 2px 2px 0;
    }
  }
}

.pvz-sidebar__item-icon {
  color: rgba(255,255,255,0.4);
  display: flex;
  align-items: center;
  flex-shrink: 0;
  transition: color 0.15s;
}

.pvz-sidebar__item-label {
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  font-weight: 500;
  flex: 1;
  transition: color 0.15s;
}

.pvz-sidebar__badge {
  background: #ef4444;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

// CTA
.pvz-sidebar__cta {
  padding: 16px 12px 8px;
}

.pvz-sidebar__cta-btn {
  width: 100%;
  height: 38px;
  background: linear-gradient(135deg, $primary-start, $primary-end);
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(102,126,234,0.3);

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(102,126,234,0.4);
  }

  &:active { transform: translateY(0); }
}

// User block
.pvz-sidebar__user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  margin: 8px 12px 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  min-width: 0;
}

.pvz-sidebar__user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, $primary-start, $primary-end);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.pvz-sidebar__user-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.pvz-sidebar__user-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pvz-sidebar__user-email {
  font-size: 11px;
  color: rgba(255,255,255,0.35);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pvz-sidebar__user-logout {
  background: none;
  border: none;
  color: rgba(255,255,255,0.25);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  transition: all 0.15s;
  flex-shrink: 0;

  &:hover { color: #ef4444; background: rgba(239,68,68,0.1); }
}

// ─── Mobile Header ───────────────────────────────────────────

.pvz-mobile-header {
  background: transparent !important;
  box-shadow: none !important;

  :deep(.q-toolbar) {
    background: $gradient-brand;
    padding-top: env(safe-area-inset-top, 0px);
    min-height: calc(56px + env(safe-area-inset-top, 0px));
  }
}

.pvz-mobile-header__title {
  font-size: 17px;
  font-weight: 600;
  color: #fff;
}

// ─── Bottom Nav ───────────────────────────────────────────────

.pvz-bottom-nav {
  background: white !important;
  border-top: 1px solid #e5e7eb;
  padding-bottom: env(safe-area-inset-bottom, 0px);
  box-shadow: 0 -4px 20px rgba(0,0,0,0.06);
}

.pvz-bottom-tabs {
  display: flex;
  height: 56px;
}

.pvz-bottom-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  color: #9ca3af;
  font-size: 11px;
  font-weight: 500;

  &--active {
    color: $primary-start;
    .q-icon { transform: translateY(-1px); }
  }

  &:active { opacity: 0.7; }
}
</style>