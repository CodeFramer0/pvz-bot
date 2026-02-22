<template>
  <q-layout view="lHh LpR lFf" class="main-layout">

    <!-- ═══════════════════════════════════════════════════════
         DESKTOP SIDEBAR
    ════════════════════════════════════════════════════════ -->
    <q-drawer
      v-if="showNav && isDesktop"
      :model-value="true"
      :width="sidebarCollapsed ? 68 : 240"
      :breakpoint="0"
      class="sidebar"
      :class="{ 'sidebar--collapsed': sidebarCollapsed }"
    >
      <div class="sidebar__inner">

        <!-- Logo -->
        <div class="sidebar__logo" :class="{ 'sidebar__logo--collapsed': sidebarCollapsed }">
          <div class="sidebar__logo-icon">🛍️</div>
          <transition name="fade-slide">
            <div v-if="!sidebarCollapsed" class="sidebar__logo-text">
              <span class="sidebar__logo-title">PVZ Bot</span>
              <span class="sidebar__logo-badge">BETA</span>
            </div>
          </transition>
          <button
            v-if="!sidebarCollapsed"
            class="sidebar__collapse-btn"
            @click="sidebarCollapsed = true"
          >
            <q-icon name="chevron_left" size="18px" />
          </button>
        </div>

        <!-- Nav -->
        <nav class="sidebar__nav">
          <p class="sidebar__nav-label" v-if="!sidebarCollapsed">Навигация</p>
          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            custom
            v-slot="{ isExactActive, navigate }"
          >
            <button
              :class="['sidebar__nav-item', { 'sidebar__nav-item--active': isExactActive }]"
              @click="navigate"
              :title="sidebarCollapsed ? item.label : ''"
            >
              <div class="sidebar__nav-item-icon">
                <q-icon :name="isExactActive ? item.iconActive : item.icon" size="20px" />
              </div>
              <transition name="fade-slide">
                <span v-if="!sidebarCollapsed" class="sidebar__nav-item-label">{{ item.label }}</span>
              </transition>
              <div v-if="isExactActive" class="sidebar__nav-item-indicator"></div>
            </button>
          </router-link>
        </nav>

        <div class="sidebar__spacer"></div>

        <!-- CTA -->
        <div class="sidebar__cta" :class="{ 'sidebar__cta--collapsed': sidebarCollapsed }">
          <router-link to="/add" custom v-slot="{ navigate }">
            <button class="sidebar__cta-btn" @click="navigate" :title="sidebarCollapsed ? 'Создать заказ' : ''">
              <q-icon name="add" size="20px" />
              <transition name="fade-slide">
                <span v-if="!sidebarCollapsed">Создать заказ</span>
              </transition>
            </button>
          </router-link>
        </div>

        <!-- User -->
        <div class="sidebar__user" :class="{ 'sidebar__user--collapsed': sidebarCollapsed }">
          <div class="sidebar__user-avatar" v-ripple>
            {{ userInitial }}
            <q-menu anchor="top right" self="bottom left" :offset="[0, 8]">
              <q-list style="min-width: 180px; border-radius: 12px; overflow: hidden;">
                <q-item clickable v-ripple @click="$router.push('/profile')">
                  <q-item-section avatar><q-icon name="person_outline" /></q-item-section>
                  <q-item-section>Профиль</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable v-ripple @click="onLogout">
                  <q-item-section avatar><q-icon name="logout" color="negative" /></q-item-section>
                  <q-item-section class="text-negative">Выйти</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </div>
          <transition name="fade-slide">
            <div v-if="!sidebarCollapsed" class="sidebar__user-info">
              <span class="sidebar__user-name">{{ auth.user?.username }}</span>
              <span class="sidebar__user-email">{{ auth.user?.email }}</span>
            </div>
          </transition>
          <transition name="fade-slide">
            <button
              v-if="!sidebarCollapsed"
              class="sidebar__user-logout"
              @click="onLogout"
              title="Выйти"
            >
              <q-icon name="logout" size="16px" />
            </button>
          </transition>
        </div>

        <!-- Expand button when collapsed -->
        <transition name="fade">
          <div v-if="sidebarCollapsed" class="sidebar__expand">
            <button class="sidebar__expand-btn" @click="sidebarCollapsed = false" title="Развернуть">
              <q-icon name="chevron_right" size="18px" />
            </button>
          </div>
        </transition>

      </div>
    </q-drawer>

    <!-- ═══════════════════════════════════════════════════════
         MOBILE HEADER
    ════════════════════════════════════════════════════════ -->
    <q-header v-if="showNav && !isDesktop" class="mobile-header" elevated>
      <div class="mobile-header__bar">
        <div class="mobile-header__logo">
          <span class="mobile-header__logo-icon">🛍️</span>
          <span class="mobile-header__logo-title">PVZ Bot</span>
        </div>
        <router-link to="/profile" class="mobile-header__avatar">
          {{ userInitial }}
        </router-link>
      </div>
    </q-header>

    <!-- ═══════════════════════════════════════════════════════
         PAGE CONTENT
    ════════════════════════════════════════════════════════ -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- ═══════════════════════════════════════════════════════
         MOBILE BOTTOM NAV
    ════════════════════════════════════════════════════════ -->
    <q-footer v-if="showNav && !isDesktop" class="mobile-footer">
      <div class="bottom-nav">
        <router-link
          v-for="item in bottomNavItems"
          :key="item.to"
          :to="item.to"
          custom
          v-slot="{ isExactActive, navigate }"
        >
          <button
            :class="['bottom-nav__item', { 'bottom-nav__item--active': isExactActive }]"
            @click="navigate"
          >
            <div class="bottom-nav__icon-wrap">
              <q-icon :name="isExactActive ? item.iconActive : item.icon" size="22px" />
              <div v-if="isExactActive" class="bottom-nav__dot"></div>
            </div>
            <span class="bottom-nav__label">{{ item.label }}</span>
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

// ── Responsive ──────────────────────────────────────────────
const windowWidth = ref(window.innerWidth)
const isDesktop = computed(() => windowWidth.value >= 1024)
const onResize = () => { windowWidth.value = window.innerWidth }
onMounted(async () => {
  window.addEventListener('resize', onResize)
  await auth.getMe()
})
onUnmounted(() => window.removeEventListener('resize', onResize))

// ── Show nav only outside auth pages ────────────────────────
const AUTH_ROUTES = ['login', 'register']
const showNav = computed(() => !AUTH_ROUTES.includes(route.name))

// ── Sidebar collapse ────────────────────────────────────────
const sidebarCollapsed = ref(false)

// ── User ────────────────────────────────────────────────────
const userInitial = computed(() =>
  auth.user?.username?.charAt(0).toUpperCase() || 'U'
)

// ── Nav items ───────────────────────────────────────────────
const navItems = [
  { to: '/',        label: 'Мои заказы', icon: 'inbox',  iconActive: 'inbox' },
  { to: '/profile', label: 'Профиль',    icon: 'person', iconActive: 'person' },
]

const bottomNavItems = [
  { to: '/',        label: 'Заказы',  icon: 'inbox',      iconActive: 'inbox'      },
  { to: '/add',     label: 'Создать', icon: 'add_circle_outline', iconActive: 'add_circle' },
  { to: '/profile', label: 'Профиль', icon: 'person_outline',     iconActive: 'person'     },
]

// ── Logout ──────────────────────────────────────────────────
const onLogout = () => {
  $q.dialog({
    title: 'Выход',
    message: 'Вы уверены, что хотите выйти?',
    cancel: { label: 'Отмена', flat: true, color: 'grey-7' },
    ok:     { label: 'Выйти', color: 'negative', unelevated: true },
    persistent: true,
  }).onOk(() => {
    auth.logout()
    router.push('/login')
  })
}

</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;

// ════════════════════════════════════════════════════════════
// SIDEBAR
// ════════════════════════════════════════════════════════════

.sidebar {
  background: linear-gradient(180deg, #0e0e14 0%, #13131d 100%) !important;
  border-right: 1px solid rgba(255, 255, 255, 0.06) !important;

  // Top accent line
  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: $gradient-brand;
    z-index: 10;
  }
}

.sidebar__inner {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0;
  overflow: hidden;
}

// ── Logo ──────────────────────────────────────────────────

.sidebar__logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px 18px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  min-height: 72px;

  &--collapsed {
    justify-content: center;
    padding: 20px 0 18px;
  }
}

.sidebar__logo-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
  border: 1.5px solid rgba(102,126,234,0.4);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.sidebar__logo-text {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.sidebar__logo-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
  white-space: nowrap;
}

.sidebar__logo-badge {
  font-size: 9px;
  font-weight: 800;
  color: $primary-start;
  background: rgba(102,126,234,0.15);
  border: 1px solid rgba(102,126,234,0.35);
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.8px;
  flex-shrink: 0;
}

.sidebar__collapse-btn {
  margin-left: auto;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 7px;
  color: rgba(255,255,255,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.7);
  }
}

// ── Nav ───────────────────────────────────────────────────

.sidebar__nav {
  padding: 16px 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar__nav-label {
  font-size: 10px;
  font-weight: 700;
  color: rgba(255,255,255,0.2);
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 0 6px;
  margin: 0 0 8px;
}

.sidebar__nav-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 10px;
  border-radius: 8px;
  border: none;
  background: none;
  cursor: pointer;
  position: relative;
  transition: background 0.18s;
  text-decoration: none;
  text-align: left;

  &:hover:not(&--active) {
    background: rgba(255,255,255,0.05);

    .sidebar__nav-item-icon { color: rgba(255,255,255,0.6); }
    .sidebar__nav-item-label { color: rgba(255,255,255,0.7); }
  }

  &--active {
    background: rgba(102,126,234,0.14);

    .sidebar__nav-item-icon { color: $primary-start; }
    .sidebar__nav-item-label { color: #fff; font-weight: 600; }
  }
}

.sidebar__nav-item-icon {
  color: rgba(255,255,255,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: color 0.18s;
}

.sidebar__nav-item-label {
  font-size: 14px;
  font-weight: 500;
  color: rgba(255,255,255,0.5);
  white-space: nowrap;
  transition: color 0.18s;
}

.sidebar__nav-item-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: $primary-start;
  border-radius: 0 3px 3px 0;
  box-shadow: 0 0 8px rgba($primary-start, 0.5);
}

// ── Spacer ────────────────────────────────────────────────

.sidebar__spacer { flex: 1; }

// ── CTA ───────────────────────────────────────────────────

.sidebar__cta {
  padding: 0 10px 12px;

  &--collapsed {
    padding: 0 10px 12px;
    display: flex;
    justify-content: center;
  }
}

.sidebar__cta-btn {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: $gradient-brand;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba($primary-start, 0.3);
  transition: all 0.2s;
  white-space: nowrap;
  overflow: hidden;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba($primary-start, 0.4);
  }

  &:active { transform: none; }
}

// ── User ──────────────────────────────────────────────────

.sidebar__user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 10px;
  margin: 0 10px 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  transition: background 0.2s;
  cursor: pointer;
  min-width: 0;

  &:hover { background: rgba(255,255,255,0.07); }

  &--collapsed {
    justify-content: center;
    padding: 10px 0;
    margin: 0 10px 16px;
    background: none;
    border: none;
  }
}

.sidebar__user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: $gradient-brand;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  cursor: pointer;
  position: relative;
}

.sidebar__user-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.sidebar__user-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.85);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar__user-email {
  font-size: 11px;
  color: rgba(255,255,255,0.3);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar__user-logout {
  flex-shrink: 0;
  background: none;
  border: none;
  color: rgba(255,255,255,0.2);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;

  &:hover { color: #ef4444; background: rgba(239,68,68,0.1); }
}

// ── Expand (collapsed state) ──────────────────────────────

.sidebar__expand {
  padding: 0 10px 16px;
}

.sidebar__expand-btn {
  width: 100%;
  height: 34px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  color: rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover { background: rgba(255,255,255,0.09); color: rgba(255,255,255,0.7); }
}

// ════════════════════════════════════════════════════════════
// MOBILE HEADER
// ════════════════════════════════════════════════════════════

.mobile-header {
  background: transparent !important;
  box-shadow: none !important;
}

.mobile-header__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  padding-top: calc(12px + env(safe-area-inset-top, 0px));
  background: linear-gradient(180deg, #0e0e14 0%, transparent 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.mobile-header__logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mobile-header__logo-icon { font-size: 22px; }

.mobile-header__logo-title {
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
}

.mobile-header__avatar {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: $gradient-brand;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  box-shadow: 0 2px 10px rgba($primary-start, 0.35);
}

// ════════════════════════════════════════════════════════════
// MOBILE BOTTOM NAV
// ════════════════════════════════════════════════════════════

.mobile-footer {
  background: rgba(14, 14, 20, 0.92) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.07) !important;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.3) !important;
}

.bottom-nav {
  display: flex;
  height: calc(60px + env(safe-area-inset-bottom, 0px));
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.bottom-nav__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.3);
  transition: color 0.2s;

  &:active { opacity: 0.7; }

  &--active {
    color: $primary-start;
  }
}

.bottom-nav__icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bottom-nav__dot {
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: $primary-start;
  box-shadow: 0 0 6px rgba($primary-start, 0.8);
}

.bottom-nav__label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

// ════════════════════════════════════════════════════════════
// TRANSITIONS
// ════════════════════════════════════════════════════════════

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-6px);
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.18s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>