<template>
  <q-layout view="lHh LpR lFf" class="main-layout">

    <!-- ═══════════════════════════════════════════════════════
         DESKTOP SIDEBAR — красивая навигация
    ════════════════════════════════════════════════════════ -->
    <q-drawer
      v-if="isDesktop"
      :model-value="true"
      :width="240"
      :breakpoint="0"
      class="sidebar"
      :class="{ 'sidebar--collapsed': sidebarCollapsed }"
    >
      <!-- LOGO SECTION -->
      <div class="sidebar-logo">
        <div class="logo-icon">🛍️</div>
        <div v-if="!sidebarCollapsed" class="logo-text">
          <div class="logo-title">PVZ Bot</div>
          <div class="logo-tag">beta</div>
        </div>
        <button 
          v-if="!sidebarCollapsed"
          class="logo-collapse-btn"
          @click="sidebarCollapsed = true"
          title="Свернуть меню"
        >
          ‹
        </button>
      </div>

      <!-- NAVIGATION SECTION -->
      <nav class="sidebar-nav">
        <div class="nav-label">{{ sidebarCollapsed ? '' : 'Навигация' }}</div>

        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          custom
          v-slot="{ isExactActive, navigate }"
        >
          <div
            :class="['nav-item', { 'nav-item--active': isExactActive }]"
            @click="navigate"
            :title="item.label"
          >
            <div class="nav-item-icon">
              <q-icon :name="item.icon" size="20px" />
            </div>
            
            <div v-if="!sidebarCollapsed" class="nav-item-content">
              <span class="nav-item-label">{{ item.label }}</span>
              <div v-if="item.badge && getCount() > 0" class="nav-item-badge">
                {{ getCount() }}
              </div>
            </div>

            <q-badge 
              v-else-if="item.badge && getCount() > 0"
              color="negative"
              floating
              rounded
            >
              {{ getCount() }}
            </q-badge>

            <!-- Active indicator -->
            <div v-if="isExactActive && !sidebarCollapsed" class="nav-item-indicator"></div>
          </div>
        </router-link>
      </nav>

      <!-- SPACER -->
      <div class="sidebar-spacer"></div>

      <!-- CREATE ORDER BUTTON -->
      <div class="sidebar-cta">
        <router-link to="/add" custom v-slot="{ navigate }">
          <button class="cta-btn" @click="navigate" :title="sidebarCollapsed ? 'Создать заказ' : ''">
            <q-icon name="add_circle" size="24px" />
            <span v-if="!sidebarCollapsed">Создать заказ</span>
          </button>
        </router-link>
      </div>

      <!-- USER PROFILE SECTION -->
      <div class="sidebar-user">
        <div class="user-avatar">
          {{ auth.user?.username?.charAt(0).toUpperCase() || 'U' }}
        </div>
        
        <div v-if="!sidebarCollapsed" class="user-info">
          <div class="user-name">{{ auth.user?.username }}</div>
          <div class="user-email">{{ auth.user?.email }}</div>
        </div>

        <q-menu
          anchor="top right"
          self="bottom left"
          :offset="[0, 8]"
        >
          <q-list style="min-width: 180px">
            <q-item clickable v-ripple @click="$router.push('/profile')">
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>
              <q-item-section>Профиль</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-ripple @click="onLogout">
              <q-item-section avatar>
                <q-icon name="logout" color="negative" />
              </q-item-section>
              <q-item-section>Выйти</q-item-section>
            </q-item>
          </q-list>
        </q-menu>

        <button 
          v-if="!sidebarCollapsed"
          class="user-logout-btn"
          @click="onLogout"
          title="Выйти"
        >
          <q-icon name="logout" size="16px" />
        </button>
      </div>

      <!-- COLLAPSE BUTTON (when collapsed) -->
      <div v-if="sidebarCollapsed" class="sidebar-expand">
        <button 
          class="expand-btn"
          @click="sidebarCollapsed = false"
          title="Развернуть меню"
        >
          ›
        </button>
      </div>
    </q-drawer>

    <!-- ═══════════════════════════════════════════════════════
         MOBILE HEADER — красивый топ-бар
    ════════════════════════════════════════════════════════ -->
    <q-header v-if="!isDesktop" class="mobile-header">
      <q-toolbar class="mobile-toolbar">
        <q-btn
          flat
          dense
          round
          icon="menu"
          color="white"
          @click="mobileDrawerOpen = true"
          class="mobile-menu-btn"
        />
        
        <q-toolbar-title class="mobile-title">
          {{ currentPageTitle }}
        </q-toolbar-title>

        <q-btn
          flat
          dense
          round
          icon="account_circle"
          color="white"
          to="/profile"
          class="mobile-profile-btn"
        />
      </q-toolbar>
    </q-header>

    <!-- MOBILE DRAWER -->
    <q-drawer
      v-model="mobileDrawerOpen"
      side="left"
      bordered
      class="mobile-drawer"
    >
      <q-scroll-area class="drawer-scroll">
        <!-- Drawer Logo -->
        <div class="drawer-logo">
          <div class="logo-icon">🛍️</div>
          <div>
            <div class="logo-title">PVZ Bot</div>
            <div class="logo-tag">beta</div>
          </div>
        </div>

        <!-- Drawer Navigation -->
        <nav class="drawer-nav">
          <p class="nav-label">Навигация</p>

          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            custom
            v-slot="{ isExactActive, navigate }"
          >
            <div
              :class="['drawer-nav-item', { 'drawer-nav-item--active': isExactActive }]"
              @click="navigate; mobileDrawerOpen = false"
            >
              <q-icon :name="item.icon" size="20px" />
              <span class="drawer-nav-label">{{ item.label }}</span>
              <q-badge v-if="item.badge && getCount() > 0" color="negative">
                {{ getCount() }}
              </q-badge>
            </div>
          </router-link>
        </nav>

        <!-- Drawer CTA -->
        <div class="drawer-cta">
          <router-link to="/add" custom v-slot="{ navigate }">
            <button 
              class="drawer-cta-btn"
              @click="navigate; mobileDrawerOpen = false"
            >
              <q-icon name="add" size="20px" />
              <span>Создать заказ</span>
            </button>
          </router-link>
        </div>

        <!-- Drawer User -->
        <div class="drawer-spacer"></div>
        <div class="drawer-user">
          <div class="user-avatar">
            {{ auth.user?.username?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <div class="user-info">
            <div class="user-name">{{ auth.user?.username }}</div>
            <div class="user-email">{{ auth.user?.email }}</div>
          </div>
        </div>

        <!-- Drawer Actions -->
        <q-item clickable v-ripple @click="onLogout">
          <q-item-section avatar>
            <q-icon name="logout" color="negative" />
          </q-item-section>
          <q-item-section>Выйти</q-item-section>
        </q-item>
      </q-scroll-area>
    </q-drawer>

    <!-- ═══════════════════════════════════════════════════════
         PAGE CONTAINER
    ════════════════════════════════════════════════════════ -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- ═══════════════════════════════════════════════════════
         MOBILE BOTTOM NAVIGATION — красивая мобильная навигация
    ════════════════════════════════════════════════════════ -->
    <q-footer v-if="!isDesktop" class="mobile-footer">
      <div class="bottom-nav">
        <router-link
          v-for="item in bottomNavItems"
          :key="item.to"
          :to="item.to"
          custom
          v-slot="{ isExactActive, navigate }"
        >
          <button
            :class="['bottom-nav-item', { 'bottom-nav-item--active': isExactActive }]"
            @click="navigate"
          >
            <div class="nav-icon-wrapper">
              <q-icon 
                :name="isExactActive ? item.iconActive : item.icon"
                size="24px"
              />
              <q-badge 
                v-if="item.badge && getCount() > 0"
                color="negative"
                floating
                rounded
              >
                {{ getCount() }}
              </q-badge>
            </div>
            <span class="nav-label">{{ item.label }}</span>
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
const sidebarCollapsed = ref(false)
const mobileDrawerOpen = ref(false)

const navItems = [
  { to: '/',        label: 'Заказы',    icon: 'inbox',      iconActive: 'inbox',      badge: true },
  { to: '/profile', label: 'Профиль',   icon: 'person',     iconActive: 'person',     badge: false },
]

const bottomNavItems = [
  { to: '/',        label: 'Заказы',    icon: 'inbox',      iconActive: 'inbox',      badge: true },
  { to: '/add',     label: 'Создать',   icon: 'add_circle', iconActive: 'add_circle', badge: false },
  { to: '/profile', label: 'Профиль',   icon: 'person',     iconActive: 'person',     badge: false },
]

const pageTitles = { 
  '/': 'Мои заказы', 
  '/add': 'Создать заказ', 
  '/profile': 'Профиль' 
}
const currentPageTitle = computed(() => pageTitles[route.path] || 'PVZ Bot')

const getCount = () => 0

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

const onResize = () => { windowWidth.value = window.innerWidth }

onMounted(async () => { 
  window.addEventListener('resize', onResize)
  await auth.getMe()
})

onUnmounted(() => window.removeEventListener('resize', onResize))
</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;

// ────────────────────────────────────────────────────────────
// DESKTOP SIDEBAR
// ────────────────────────────────────────────────────────────

.sidebar {
  background: linear-gradient(180deg, #0e0e14 0%, #15151f 100%) !important;
  display: flex !important;
  flex-direction: column;
  padding: 0 !important;
  border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  // Top gradient bar
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: $gradient-brand;
    z-index: 10;
  }

  &--collapsed {
    :deep(.q-drawer__content) {
      padding-left: 4px;
      padding-right: 4px;
    }
  }
}

// Logo
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  position: relative;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
  border: 1.5px solid rgba(102, 126, 234, 0.4);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
  transition: all 0.3s;

  &:hover {
    border-color: rgba(102, 126, 234, 0.6);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
  }
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.logo-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
}

.logo-tag {
  font-size: 10px;
  font-weight: 700;
  color: $primary-start;
  background: rgba(102, 126, 234, 0.15);
  border: 1px solid rgba(102, 126, 234, 0.3);
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  width: fit-content;
}

.logo-collapse-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
  margin-left: auto;

  &:hover {
    color: rgba(255, 255, 255, 0.8);
  }
}

// Navigation
.sidebar-nav {
  padding: 12px 8px;
  flex: 0;
}

.nav-label {
  font-size: 10px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.2);
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 0 8px;
  margin-bottom: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 2px;
  position: relative;
  transition: all 0.2s ease;
  cursor: pointer;
  text-decoration: none;
  color: inherit;

  &:hover:not(&--active) {
    background: rgba(255, 255, 255, 0.06);

    .nav-item-icon {
      color: rgba(255, 255, 255, 0.7);
    }
  }

  &--active {
    background: rgba(102, 126, 234, 0.15);

    .nav-item-icon {
      color: $primary-start;
      transform: scale(1.1);
    }

    .nav-item-label {
      color: #fff;
      font-weight: 600;
    }

    .nav-item-indicator {
      display: block;
    }
  }
}

.nav-item-icon {
  color: rgba(255, 255, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.nav-item-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.nav-item-label {
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-item-badge {
  background: #ef4444;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: auto;
  flex-shrink: 0;
}

.nav-item-indicator {
  display: none;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: $primary-start;
  border-radius: 0 2px 2px 0;
}

// Spacer
.sidebar-spacer {
  flex: 1;
}

// CTA Button
.sidebar-cta {
  padding: 16px 8px 12px;
}

.cta-btn {
  width: 100%;
  height: 42px;
  background: $gradient-brand;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

// User Profile
.sidebar-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 12px;
  margin: 8px 8px 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  transition: all 0.2s;
  min-width: 0;

  &:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.15);
  }
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: $gradient-brand;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-email {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.35);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-logout-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.25);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;

  &:hover {
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
  }
}

// Sidebar Expand (when collapsed)
.sidebar-expand {
  padding: 8px;
}

.expand-btn {
  width: 100%;
  height: 36px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
  }
}

// ────────────────────────────────────────────────────────────
// MOBILE HEADER
// ────────────────────────────────────────────────────────────

.mobile-header {
  background: transparent !important;
  box-shadow: none !important;
}

.mobile-toolbar {
  background: $gradient-brand;
  padding-top: env(safe-area-inset-top, 0px);
  min-height: calc(56px + env(safe-area-inset-top, 0px));
}

.mobile-menu-btn {
  color: #fff;
}

.mobile-title {
  font-size: 17px;
  font-weight: 600;
  color: #fff;
  text-align: center;
}

.mobile-profile-btn {
  color: #fff;
}

// Mobile Drawer
.mobile-drawer {
  background: #fafbfc;
}

.drawer-scroll {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.drawer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.drawer-nav {
  padding: 12px 0;
  flex: 0;
}

.drawer-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: inherit;
  margin: 0 8px;
  border-radius: 8px;

  &:hover:not(&--active) {
    background: rgba(0, 0, 0, 0.04);
  }

  &--active {
    background: rgba(102, 126, 234, 0.1);
    color: $primary-start;
    font-weight: 600;
  }
}

.drawer-nav-label {
  font-size: 14px;
  font-weight: 500;
  flex: 1;
}

.drawer-cta {
  padding: 12px 8px;
}

.drawer-cta-btn {
  width: 100%;
  height: 40px;
  background: $gradient-brand;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);

  &:active {
    opacity: 0.9;
  }
}

.drawer-spacer {
  flex: 1;
}

.drawer-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  margin: 0 8px 8px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

// ────────────────────────────────────────────────────────────
// MOBILE BOTTOM NAVIGATION
// ────────────────────────────────────────────────────────────

.mobile-footer {
  background: #fff !important;
  border-top: 1px solid #e5e7eb !important;
  padding-bottom: env(safe-area-inset-bottom, 0px);
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.08);
}

.bottom-nav {
  display: flex;
  height: calc(56px + env(safe-area-inset-bottom, 0px));
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  color: #9ca3af;
  font-size: 11px;
  font-weight: 500;
  text-decoration: none;

  &:hover:not(&--active) {
    color: #6b7280;
  }

  &--active {
    color: $primary-start;

    .nav-icon-wrapper {
      transform: scale(1.15);
    }
  }
}

.nav-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.nav-label {
  font-size: 10px;
  white-space: nowrap;
  transition: color 0.2s;
}


</style>