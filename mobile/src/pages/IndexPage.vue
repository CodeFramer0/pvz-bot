<template>
  <q-page class="pvz-page orders-page">

    <!-- MOBILE HERO (скрыт на десктопе) -->
    <div class="pvz-hero-header">
      <div class="pvz-hero-header__inner">
        <div>
          <h3 class="pvz-hero-header__greeting">Привет, {{ auth.user?.username || 'Гость' }} 👋</h3>
          <p class="pvz-hero-header__sub">Управляй своими заказами</p>
        </div>
        <q-btn flat round dense icon="account_circle" color="white" size="md"
          class="pvz-hero-header__profile-btn" @click="$router.push('/profile')" />
      </div>
    </div>

    <!-- DESKTOP LAYOUT -->
    <div class="desktop-wrapper">

      <!-- Top Bar -->
      <div class="topbar">
        <div class="topbar-row1">
          <div>
            <h2 class="topbar-greeting">Привет, {{ auth.user?.username || 'Гость' }} 👋</h2>
            <p class="topbar-sub">Вот все ваши заказы</p>
          </div>
          <div class="topbar-stats">
            <div class="stat-pill">
              <span class="stat-pill-dot stat-pill-dot--orange"></span>
              <span>В пути:</span>
              <strong>{{ countByStatus('В пути') }}</strong>
            </div>
            <div class="stat-pill">
              <span class="stat-pill-dot stat-pill-dot--blue"></span>
              <span>На складе:</span>
              <strong>{{ countByStatus('На складе РФ') }}</strong>
            </div>
            <div class="stat-pill">
              <span class="stat-pill-dot stat-pill-dot--green"></span>
              <span>Выдано:</span>
              <strong>{{ countByStatus('Выдан') }}</strong>
            </div>
          </div>
        </div>

        <div class="topbar-row2">
          <div class="search-box" :class="{ focused: searchFocused }">
            <q-icon name="search" size="16px" class="search-icon" />
            <input ref="searchInput" v-model="searchQuery" class="search-input"
              placeholder="Имя получателя, номер заказа..."
              @focus="searchFocused = true" @blur="searchFocused = false" />
            <span v-if="searchQuery" class="search-clear" @click="searchQuery = ''">✕</span>
            <span v-else class="search-kbd">⌘K</span>
          </div>

          <div class="filter-tabs">
            <button v-for="t in tabs" :key="t.value"
              :class="['filter-tab', { active: tab === t.value }]"
              @click="tab = t.value; selectedOrder = null">
              {{ t.label }}
              <span v-if="getTabCount(t.value) > 0" class="filter-tab-count">{{ getTabCount(t.value) }}</span>
            </button>
          </div>

          <button class="create-btn" @click="$router.push('/add')">
            <q-icon name="add" size="18px" />
            Создать заказ
          </button>
        </div>
      </div>

      <!-- Split Content -->
      <div class="split-content" :class="{ 'has-detail': selectedOrder !== null }">

        <!-- Orders Panel -->
        <div class="orders-panel">
          <div class="orders-panel-head">
            <span class="orders-panel-title">Заказы</span>
            <span class="orders-count-badge">{{ filteredOrders.length }}</span>
          </div>

          <div v-if="loading" class="list-loading">
            <q-spinner-dots color="primary" size="36px" />
            <p>Загружаем заказы...</p>
          </div>

          <div v-else-if="filteredOrders.length === 0" class="list-empty">
            <div class="list-empty-icon">📭</div>
            <p class="list-empty-text">{{ searchQuery ? 'Ничего не найдено' : tab === 'active' ? 'Нет активных заказов' : 'История пуста' }}</p>
            <button v-if="!searchQuery && tab === 'active'" class="list-empty-btn" @click="$router.push('/add')">Создать первый заказ</button>
          </div>

          <div v-else class="orders-list">
            <div v-for="order in filteredOrders" :key="order.id"
              :class="['order-row', { 'order-row--active': selectedOrder?.id === order.id }, { 'order-row--archived': isArchived(order) }]"
              @click="selectOrder(order)">
              <div class="order-mp-icon">{{ getMarketplaceIcon(order.pickup_point.marketplace) }}</div>
              <div class="order-meta">
                <div class="order-meta-top">
                  <span class="order-name">{{ order.full_name || 'Без имени' }}</span>
                  <span class="order-id">#{{ order.id }}</span>
                </div>
                <div class="order-addr">{{ order.pickup_point.marketplace }} · {{ order.pickup_point.address }}</div>
              </div>
              <div class="order-right">
                <span class="order-amount">{{ formatAmount(order.amount) }} ₽</span>
                <span :class="['status-badge', getStatusClass(order.status)]">{{ order.status_display }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Detail Panel -->
        <transition name="detail-slide">
          <div v-if="selectedOrder" class="detail-panel" :key="selectedOrder.id">
            <div class="detail-header">
              <div class="detail-header-top">
                <div class="detail-mp">
                  <span class="detail-mp-icon">{{ getMarketplaceIcon(selectedOrder.pickup_point.marketplace) }}</span>
                  <div>
                    <div class="detail-mp-name">{{ selectedOrder.pickup_point.marketplace }}</div>
                    <div class="detail-order-id">Заказ #{{ selectedOrder.id }}</div>
                  </div>
                </div>
                <button class="detail-close" @click="selectedOrder = null">
                  <q-icon name="close" size="16px" />
                </button>
              </div>
              <span :class="['detail-status-badge', getStatusClass(selectedOrder.status)]">{{ selectedOrder.status_display }}</span>
            </div>

            <div class="detail-body">
              <div class="detail-section">
                <div class="detail-icon-wrap detail-icon-wrap--blue"><q-icon name="person" size="16px" color="blue-6" /></div>
                <div class="detail-info">
                  <div class="detail-label">Получатель</div>
                  <div class="detail-value">{{ selectedOrder.full_name }}</div>
                </div>
              </div>
              <div class="detail-section">
                <div class="detail-icon-wrap detail-icon-wrap--purple"><q-icon name="payments" size="16px" color="deep-purple-4" /></div>
                <div class="detail-info">
                  <div class="detail-label">Сумма заказа</div>
                  <div class="detail-value detail-value--amount">{{ formatAmount(selectedOrder.amount) }} ₽</div>
                </div>
              </div>
              <div class="detail-section">
                <div class="detail-icon-wrap detail-icon-wrap--green"><q-icon name="place" size="16px" color="green-6" /></div>
                <div class="detail-info">
                  <div class="detail-label">Пункт выдачи</div>
                  <div class="detail-value">{{ selectedOrder.pickup_point.marketplace_display }}</div>
                  <div class="detail-sub">{{ selectedOrder.pickup_point.address }}</div>
                </div>
              </div>
              <div v-if="selectedOrder.comment" class="detail-section">
                <div class="detail-icon-wrap detail-icon-wrap--orange"><q-icon name="comment" size="16px" color="orange-6" /></div>
                <div class="detail-info">
                  <div class="detail-label">Комментарий</div>
                  <div class="detail-value detail-value--comment">{{ selectedOrder.comment }}</div>
                </div>
              </div>
              <div v-if="selectedOrder.barcode_image" class="detail-barcode-section">
                <div class="detail-section" style="border-bottom:none;">
                  <div class="detail-icon-wrap detail-icon-wrap--grey"><q-icon name="qr_code" size="16px" color="grey-6" /></div>
                  <div class="detail-info"><div class="detail-label">Штрих-код</div></div>
                </div>
                <div class="barcode-box">
                  <div class="barcode-corner barcode-corner--tl"></div>
                  <div class="barcode-corner barcode-corner--tr"></div>
                  <div class="barcode-corner barcode-corner--bl"></div>
                  <div class="barcode-corner barcode-corner--br"></div>
                  <img :src="selectedOrder.barcode_image" alt="Barcode" class="barcode-img" />
                </div>
              </div>
            </div>
          </div>

          <div v-else class="detail-empty-panel">
            <div class="detail-empty-icon">👆</div>
            <p class="detail-empty-text">Выберите заказ из списка<br>чтобы увидеть детали</p>
          </div>
        </transition>

      </div>
    </div>

    <!-- MOBILE CONTENT -->
    <div class="mobile-content">
      <div class="mobile-search-wrap">
        <q-input v-model="searchQuery" outlined dense bg-color="white"
          placeholder="Поиск по заказам..." class="pvz-search">
          <template v-slot:prepend><q-icon name="search" /></template>
          <template v-slot:append v-if="searchQuery">
            <q-icon name="clear" class="cursor-pointer" @click="searchQuery = ''" />
          </template>
        </q-input>
      </div>

      <div class="pvz-tabs q-mb-md">
        <div v-for="t in tabs" :key="t.value" :class="['tab-item', { active: tab === t.value }]" @click="tab = t.value">
          <q-icon :name="t.icon" size="18px" />
          <span class="tab-label">{{ t.label }}</span>
          <div class="tab-badge" v-if="getTabCount(t.value) > 0">{{ getTabCount(t.value) }}</div>
        </div>
      </div>

      <div v-if="loading" class="orders-loading">
        <q-spinner-dots color="primary" size="50px" />
        <p>Загружаем заказы...</p>
      </div>

      <div v-else-if="filteredOrders.length === 0" class="pvz-empty">
        <div class="empty-icon anim-float-y">📦</div>
        <h5 class="empty-title">{{ tab === 'active' ? 'Нет активных заказов' : 'История пуста' }}</h5>
        <p class="empty-text">{{ tab === 'active' ? 'Создайте свой первый заказ!' : 'Завершённые заказы появятся здесь' }}</p>
        <q-btn v-if="tab === 'active'" label="Создать заказ" color="primary" unelevated rounded class="q-mt-md" icon="add" @click="$router.push('/add')" />
      </div>

      <div v-else class="mobile-orders-list">
        <div v-for="order in filteredOrders" :key="order.id" class="pvz-order-card" @click="openMobileDetail(order)">
          <div class="pvz-order-card__header">
            <div class="pvz-order-card__marketplace">
              <div class="pvz-order-card__icon">{{ getMarketplaceIcon(order.pickup_point.marketplace) }}</div>
              <div>
                <h6 class="pvz-order-card__name">{{ order.pickup_point.marketplace }}</h6>
                <p class="pvz-order-card__id">ID: {{ order.id }}</p>
              </div>
            </div>
            <span :class="['pvz-badge', getStatusClass(order.status)]">{{ order.status_display }}</span>
          </div>
          <div class="pvz-order-card__body">
            <div class="info-row"><q-icon name="person" size="16px" color="grey-6" /><span>{{ order.full_name || 'Не указано' }}</span></div>
            <div class="info-row"><q-icon name="payments" size="16px" color="grey-6" /><span class="amount">{{ formatAmount(order.amount) }} ₽</span></div>
            <div class="info-row"><q-icon name="place" size="16px" color="grey-6" /><span class="address">{{ order.pickup_point.address }}</span></div>
          </div>
          <div class="pvz-order-card__footer"><q-icon name="chevron_right" size="20px" color="grey-5" /></div>
        </div>
      </div>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 78]">
      <q-btn fab icon="add" color="primary" class="pvz-fab mobile-only-fab" @click="$router.push('/add')" />
    </q-page-sticky>

    <!-- Mobile Detail Dialog -->
    <q-dialog v-model="showMobileDetail" transition-show="slide-up" transition-hide="slide-down">
      <q-card class="pvz-detail-dialog" v-if="mobileSelectedOrder">
        <q-card-section class="pvz-detail-dialog__header">
          <div class="title-row">
            <h5>Заказ #{{ mobileSelectedOrder.id }}</h5>
            <q-btn icon="close" flat round dense v-close-popup />
          </div>
          <span :class="['pvz-badge pvz-badge--lg', getStatusClass(mobileSelectedOrder.status)]">{{ mobileSelectedOrder.status_display }}</span>
        </q-card-section>
        <q-separator />
        <q-card-section class="pvz-detail-dialog__body">
          <div class="detail-section"><h6 class="section-title"><q-icon name="person" size="20px" /> Получатель</h6><p class="section-content">{{ mobileSelectedOrder.full_name }}</p></div>
          <div class="detail-section"><h6 class="section-title"><q-icon name="payments" size="20px" /> Сумма</h6><p class="section-content section-content--amount">{{ formatAmount(mobileSelectedOrder.amount) }} ₽</p></div>
          <div class="detail-section"><h6 class="section-title"><q-icon name="place" size="20px" /> Пункт выдачи</h6><p class="section-content">{{ mobileSelectedOrder.pickup_point.marketplace_display }}</p><p class="section-sub">{{ mobileSelectedOrder.pickup_point.address }}</p></div>
          <div v-if="mobileSelectedOrder.comment" class="detail-section"><h6 class="section-title"><q-icon name="comment" size="20px" /> Комментарий</h6><p class="section-content">{{ mobileSelectedOrder.comment }}</p></div>
          <div v-if="mobileSelectedOrder.barcode_image" class="detail-section"><h6 class="section-title"><q-icon name="qr_code" size="20px" /> Штрих-код</h6><div class="barcode-wrapper"><img :src="mobileSelectedOrder.barcode_image" alt="Barcode" class="barcode-image" /></div></div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from 'src/stores/auth-store'
import api from 'src/api/client'

const auth = useAuthStore()
const orders = ref([])
const loading = ref(true)
const searchQuery = ref('')
const searchFocused = ref(false)
const tab = ref('active')
const selectedOrder = ref(null)
const mobileSelectedOrder = ref(null)
const showMobileDetail = ref(false)
const searchInput = ref(null)

const DONE = ['Выдан']
const tabs = [
  { value: 'active',  label: 'Активные', icon: 'inbox'   },
  { value: 'history', label: 'Архив',    icon: 'archive' },
]

const filteredOrders = computed(() => {
  let list = orders.value
  if (tab.value === 'active')  list = list.filter(o => !DONE.includes(o.status))
  if (tab.value === 'history') list = list.filter(o =>  DONE.includes(o.status))
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(o =>
      String(o.id).includes(q) ||
      (o.full_name && o.full_name.toLowerCase().includes(q)) ||
      o.pickup_point.marketplace.toLowerCase().includes(q) ||
      o.pickup_point.address.toLowerCase().includes(q)
    )
  }
  return list
})

const isArchived    = (o) => DONE.includes(o.status)
const getTabCount   = (v) => v === 'active' ? orders.value.filter(o => !DONE.includes(o.status)).length : orders.value.filter(o => DONE.includes(o.status)).length
const countByStatus = (s) => orders.value.filter(o => o.status === s).length
const formatAmount  = (a) => Number(a).toLocaleString('ru-RU')
const getMarketplaceIcon = (mp) => ({ 'Wildberries': '🟣', 'Ozon': '🔵', 'Яндекс.Маркет': '🟡', 'СДЭК': '🟢' }[mp] || '📦')
const getStatusClass = (s) => ({ 'Выдан': 'pvz-badge--success', 'В пути': 'pvz-badge--warning', 'На складе РФ': 'pvz-badge--info' }[s] || 'pvz-badge--default')
const selectOrder = (o) => { selectedOrder.value = selectedOrder.value?.id === o.id ? null : o }
const openMobileDetail = (o) => { mobileSelectedOrder.value = o; showMobileDetail.value = true }

const onKeydown = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); searchInput.value?.focus() }
  if (e.key === 'Escape' && selectedOrder.value) selectedOrder.value = null
}

onMounted(async () => {
  window.addEventListener('keydown', onKeydown)
  await auth.getMe()
  loading.value = true
  try {
    const res = await api.get('/orders/my_orders/')
    orders.value = await res.json()
    const first = orders.value.find(o => !DONE.includes(o.status))
    if (first) selectedOrder.value = first
  } catch (e) { console.error(e) }
  finally { loading.value = false }
})

onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;
@use 'src/css/mixins' as *;

.desktop-wrapper { display: none; }
.mobile-content  { display: block; padding: 0 16px; }
.mobile-orders-list { display: flex; flex-direction: column; gap: 12px; }
.mobile-search-wrap { margin-bottom: 16px; }
.orders-loading { text-align: center; padding: 60px 20px; color: white; p { margin-top: 16px; } }
.barcode-wrapper { background: #f9fafb; border-radius: 12px; padding: 16px; text-align: center; margin-top: 8px; }
.barcode-image { max-width: 100%; border-radius: 8px; }
.mobile-only-fab { box-shadow: 0 8px 24px rgba($primary-start, 0.4); }

@include desktop {
  .mobile-content  { display: none !important; }
  .mobile-only-fab { display: none !important; }
  .pvz-hero-header { display: none !important; }

  .desktop-wrapper { display: flex; flex-direction: column; height: 100%; overflow: hidden; }

  .topbar { padding: 22px 24px 16px; display: flex; flex-direction: column; gap: 14px; flex-shrink: 0; }
  .topbar-row1 { display: flex; align-items: flex-start; justify-content: space-between; }
  .topbar-greeting { font-size: 20px; font-weight: 800; color: $color-text-dark; letter-spacing: -0.5px; margin: 0; }
  .topbar-sub { font-size: 13px; color: $color-text-muted; margin: 3px 0 0; }
  .topbar-stats { display: flex; gap: 8px; align-items: center; }
  .stat-pill { display: flex; align-items: center; gap: 5px; padding: 5px 12px; background: white; border: 1px solid $color-border; border-radius: 100px; font-size: 12.5px; color: $color-text-body; box-shadow: 0 1px 2px rgba(0,0,0,.04); strong { font-weight: 700; color: $color-text-dark; } }
  .stat-pill-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; &--orange { background: #f59e0b; } &--blue { background: #3b82f6; } &--green { background: #10b981; } }
  .topbar-row2 { display: flex; align-items: center; gap: 10px; }

  .search-box { flex: 1; display: flex; align-items: center; gap: 8px; background: white; border: 1.5px solid $color-border; border-radius: $radius-md; padding: 0 14px; height: 40px; cursor: text; transition: border-color .2s, box-shadow .2s; &.focused { border-color: $primary-start; box-shadow: 0 0 0 3px rgba($primary-start,.1); } }
  .search-icon { color: $color-text-hint; flex-shrink: 0; }
  .search-input { flex: 1; border: none; outline: none; background: none; font-size: 13.5px; color: $color-text-dark; font-family: inherit; &::placeholder { color: $color-text-hint; } }
  .search-kbd { font-size: 10.5px; font-weight: 600; color: $color-text-hint; background: $color-bg-page; border: 1px solid $color-border; border-radius: 4px; padding: 2px 6px; flex-shrink: 0; }
  .search-clear { font-size: 11px; color: $color-text-hint; cursor: pointer; padding: 2px 4px; border-radius: 4px; transition: all .15s; &:hover { color: $color-text-dark; background: $color-bg-page; } }

  .filter-tabs { display: flex; gap: 2px; background: white; border: 1px solid $color-border; border-radius: $radius-md; padding: 3px; flex-shrink: 0; }
  .filter-tab { display: flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: $radius-sm; border: none; background: none; font-size: 12.5px; font-weight: 600; color: $color-text-muted; cursor: pointer; transition: all .15s; font-family: inherit; white-space: nowrap; &:hover:not(.active) { color: $color-text-dark; } &.active { background: $gradient-brand; color: white; box-shadow: 0 2px 8px rgba($primary-start,.25); } }
  .filter-tab-count { font-size: 10px; font-weight: 700; background: rgba(0,0,0,.12); padding: 1px 5px; border-radius: 10px; .filter-tab:not(.active) & { background: $color-bg-page; color: $color-text-muted; } }

  .create-btn { display: flex; align-items: center; gap: 6px; padding: 0 16px; height: 40px; border-radius: $radius-md; border: none; background: $gradient-brand; color: white; font-size: 13px; font-weight: 600; cursor: pointer; font-family: inherit; box-shadow: 0 2px 8px rgba($primary-start,.3); transition: all .2s; flex-shrink: 0; white-space: nowrap; &:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba($primary-start,.4); } &:active { transform: none; } }

  .split-content { display: grid; grid-template-columns: 1fr 0px; gap: 0; overflow: hidden; padding: 0 24px 24px; flex: 1; transition: grid-template-columns .25s ease; &.has-detail { grid-template-columns: 1fr 360px; gap: 14px; } }

  .orders-panel { background: white; border-radius: $radius-xl; border: 1px solid $color-border; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,.05); min-width: 0; }
  .orders-panel-head { padding: 13px 18px; border-bottom: 1px solid $color-border; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
  .orders-panel-title { font-size: 12.5px; font-weight: 700; color: $color-text-muted; text-transform: uppercase; letter-spacing: .6px; }
  .orders-count-badge { font-size: 11px; font-weight: 700; color: $primary-start; background: rgba($primary-start,.1); padding: 2px 8px; border-radius: 100px; }
  .orders-list { overflow-y: auto; flex: 1; }

  .order-row { display: grid; grid-template-columns: 44px 1fr auto; align-items: center; gap: 12px; padding: 12px 18px; border-bottom: 1px solid $color-border; cursor: pointer; transition: background .1s; position: relative; &:last-child { border-bottom: none; } @include hover { &:hover { background: #fafbfc; } } &--active { background: rgba($primary-start,.04) !important; &::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: $gradient-brand; border-radius: 0 2px 2px 0; } } &--archived { opacity: .55; } }
  .order-mp-icon { width: 44px; height: 44px; background: $color-bg-page; border-radius: $radius-md; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; border: 1px solid $color-border; }
  .order-meta { min-width: 0; }
  .order-meta-top { display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }
  .order-name { font-size: 13.5px; font-weight: 600; color: $color-text-dark; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .order-id   { font-size: 11px; color: $color-text-hint; font-weight: 500; flex-shrink: 0; }
  .order-addr { font-size: 12px; color: $color-text-muted; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .order-right { display: flex; flex-direction: column; align-items: flex-end; gap: 5px; flex-shrink: 0; }
  .order-amount { font-size: 13px; font-weight: 700; color: $color-text-dark; }

  .status-badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px; border-radius: 100px; font-size: 10.5px; font-weight: 700; white-space: nowrap; &::before { content: ''; width: 5px; height: 5px; border-radius: 50%; } &.pvz-badge--success { background: #ecfdf5; color: #047857; &::before { background: #10b981; } } &.pvz-badge--warning { background: #fffbeb; color: #b45309; &::before { background: #f59e0b; } } &.pvz-badge--info { background: #eff6ff; color: #1d4ed8; &::before { background: #3b82f6; } } &.pvz-badge--default { background: $color-bg-page; color: $color-text-muted; &::before { background: $color-text-hint; } } }

  .list-loading { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; color: $color-text-muted; p { font-size: 13px; } }
  .list-empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; text-align: center; }
  .list-empty-icon { font-size: 40px; margin-bottom: 12px; opacity: .5; }
  .list-empty-text { font-size: 14px; color: $color-text-muted; font-weight: 500; margin-bottom: 16px; }
  .list-empty-btn { padding: 8px 20px; background: $gradient-brand; color: white; border: none; border-radius: $radius-md; font-size: 13px; font-weight: 600; cursor: pointer; font-family: inherit; }

  .detail-panel { background: white; border-radius: $radius-xl; border: 1px solid $color-border; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,.05); min-width: 0; }
  .detail-slide-enter-active { transition: all .22s ease; }
  .detail-slide-leave-active { transition: all .15s ease; }
  .detail-slide-enter-from   { opacity: 0; transform: translateX(16px); }
  .detail-slide-leave-to     { opacity: 0; transform: translateX(8px); }

  .detail-header { background: $gradient-brand; padding: 18px 18px 16px; position: relative; overflow: hidden; flex-shrink: 0; &::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 80% 20%, rgba(255,255,255,.12) 0%, transparent 60%); pointer-events: none; } }
  .detail-header-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; position: relative; z-index: 1; }
  .detail-mp { display: flex; align-items: center; gap: 10px; }
  .detail-mp-icon { font-size: 26px; }
  .detail-mp-name { font-size: 11px; font-weight: 700; color: rgba(255,255,255,.7); text-transform: uppercase; letter-spacing: .8px; }
  .detail-order-id { font-size: 18px; font-weight: 800; color: white; letter-spacing: -.3px; }
  .detail-close { width: 28px; height: 28px; background: rgba(255,255,255,.15); border: none; border-radius: 7px; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background .15s; flex-shrink: 0; position: relative; z-index: 1; &:hover { background: rgba(255,255,255,.25); } }
  .detail-status-badge { display: inline-flex; align-items: center; gap: 5px; padding: 5px 12px; border-radius: 100px; font-size: 11px; font-weight: 700; position: relative; z-index: 1; &.pvz-badge--success { background: rgba(16,185,129,.25); color: #d1fae5; } &.pvz-badge--warning { background: rgba(245,158,11,.25); color: #fef3c7; } &.pvz-badge--info { background: rgba(59,130,246,.25); color: #dbeafe; } &.pvz-badge--default { background: rgba(255,255,255,.15); color: rgba(255,255,255,.85); } }

  .detail-body { flex: 1; overflow-y: auto; }
  .detail-section { display: flex; align-items: flex-start; gap: 12px; padding: 13px 18px; border-bottom: 1px solid $color-border; &:last-of-type { border-bottom: none; } }
  .detail-icon-wrap { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; &--blue { background: #eff6ff; } &--purple { background: rgba($primary-start,.1); } &--green { background: #f0fdf4; } &--orange { background: #fff7ed; } &--grey { background: $color-bg-page; } }
  .detail-info { flex: 1; min-width: 0; }
  .detail-label { font-size: 10px; font-weight: 700; color: $color-text-hint; text-transform: uppercase; letter-spacing: .7px; margin-bottom: 3px; }
  .detail-value { font-size: 14px; font-weight: 600; color: $color-text-dark; line-height: 1.4; }
  .detail-value--amount { font-size: 20px; font-weight: 800; background: $gradient-brand; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  .detail-value--comment { font-weight: 500; color: $color-text-body; }
  .detail-sub { font-size: 12px; color: $color-text-muted; margin-top: 2px; }

  .detail-barcode-section { border-top: 1px solid $color-border; }
  .barcode-box { margin: 0 18px 16px; background: $color-bg-page; border-radius: $radius-md; padding: 14px; text-align: center; border: 1px solid $color-border; position: relative; }
  .barcode-corner { position: absolute; width: 14px; height: 14px; border-color: $primary-start; border-style: solid; &--tl { top: 6px; left: 6px; border-width: 2px 0 0 2px; border-radius: 3px 0 0 0; } &--tr { top: 6px; right: 6px; border-width: 2px 2px 0 0; border-radius: 0 3px 0 0; } &--bl { bottom: 6px; left: 6px; border-width: 0 0 2px 2px; border-radius: 0 0 0 3px; } &--br { bottom: 6px; right: 6px; border-width: 0 2px 2px 0; border-radius: 0 0 3px 0; } }
  .barcode-img { max-width: 100%; height: auto; border-radius: 6px; display: block; margin: 0 auto; }

  .detail-empty-panel { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px 24px; color: $color-text-hint; background: white; border-radius: $radius-xl; border: 1.5px dashed $color-border; }
  .detail-empty-icon { font-size: 44px; margin-bottom: 14px; opacity: .4; }
  .detail-empty-text { font-size: 14px; font-weight: 500; line-height: 1.6; color: $color-text-muted; }
}
</style>