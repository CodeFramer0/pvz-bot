<template>
  <q-page class="pvz-page">

    <!-- ── MOBILE Hero Header ──────────────────────────────── -->
    <div class="pvz-hero-header">
      <div class="pvz-hero-header__inner">
        <div>
          <h3 class="pvz-hero-header__greeting">
            Привет, {{ auth.user?.username || 'Гость' }} 👋
          </h3>
          <p class="pvz-hero-header__sub">Управляй своими заказами</p>
        </div>
        <q-btn flat round dense icon="account_circle" color="white" size="md"
          class="pvz-hero-header__profile-btn" @click="$router.push('/profile')" />
      </div>
    </div>

    <!-- ── CONTENT (адаптивная обёртка) ──────────────────── -->
    <div class="orders-page-wrapper">

      <!-- Desktop page title -->
      <div class="desktop-orders-header">
        <div>
          <h2 class="desktop-page-title">Мои заказы</h2>
          <p class="desktop-page-subtitle">{{ orders.length }} заказов всего</p>
        </div>
        <q-btn
          label="Создать заказ"
          color="primary"
          unelevated rounded
          icon="add"
          class="desktop-create-btn"
          @click="$router.push('/add')"
        />
      </div>

      <!-- Toolbar: Search + Tabs -->
      <div class="desktop-orders-toolbar">
        <!-- Search -->
        <div class="q-pb-md search-wrap">
          <q-input
            v-model="searchQuery"
            outlined dense
            placeholder="Поиск по ID или маркетплейсу..."
            class="pvz-search"
          >
            <template v-slot:prepend><q-icon name="search" /></template>
            <template v-slot:append v-if="searchQuery">
              <q-icon name="clear" class="cursor-pointer" @click="searchQuery = ''" />
            </template>
          </q-input>
        </div>

        <!-- Tabs -->
        <div class="tabs-wrap">
          <div class="pvz-tabs">
            <div
              v-for="t in tabs"
              :key="t.value"
              :class="['tab-item', { active: tab === t.value }]"
              @click="tab = t.value"
            >
              <q-icon :name="t.icon" size="18px" />
              <span class="tab-label">{{ t.label }}</span>
              <div class="tab-badge" v-if="t.badge && getTabCount(t.value) > 0">
                {{ getTabCount(t.value) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="orders-loading">
        <q-spinner-dots color="primary" size="50px" />
        <p>Загружаем заказы...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredOrders.length === 0 && tab !== 'stats'" class="pvz-empty">
        <div class="empty-icon anim-float-y">📦</div>
        <h5 class="empty-title">
          {{ tab === 'active' ? 'Нет активных заказов' : 'История пуста' }}
        </h5>
        <p class="empty-text">
          {{ tab === 'active' ? 'Создай свой первый заказ!' : 'Завершённые заказы появятся здесь' }}
        </p>
        <q-btn v-if="tab === 'active'" label="Создать заказ" color="primary"
          unelevated rounded class="q-mt-md" icon="add" @click="$router.push('/add')" />
      </div>

      <!-- Orders -->
      <div v-else-if="tab !== 'stats'" class="orders-list">
        <transition-group name="list">
          <div
            v-for="order in filteredOrders"
            :key="order.id"
            class="pvz-order-card"
            @click="goToDetails(order.id)"
          >
            <div class="pvz-order-card__header">
              <div class="pvz-order-card__marketplace">
                <div class="pvz-order-card__icon">{{ getMarketplaceIcon(order.pickup_point.marketplace) }}</div>
                <div>
                  <h6 class="pvz-order-card__name">{{ order.pickup_point.marketplace }}</h6>
                  <p class="pvz-order-card__id">ID: {{ order.id }}</p>
                </div>
              </div>
              <span :class="['pvz-badge', getStatusClass(order.status)]">
                {{ order.status_display }}
              </span>
            </div>
            <div class="pvz-order-card__body">
              <div class="info-row">
                <q-icon name="person" size="16px" color="grey-6" />
                <span>{{ order.full_name || 'Не указано' }}</span>
              </div>
              <div class="info-row">
                <q-icon name="payments" size="16px" color="grey-6" />
                <span class="amount">{{ order.amount }} ₽</span>
              </div>
              <div class="info-row">
                <q-icon name="place" size="16px" color="grey-6" />
                <span class="address">{{ order.pickup_point.address }}</span>
              </div>
            </div>
            <div class="pvz-order-card__footer">
              <q-icon name="chevron_right" size="20px" color="grey-5" />
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Stats -->
      <div v-else class="stats-section">
        <div class="pvz-stat-card-hero">
          <div class="pvz-stat-card-hero__emoji">📊</div>
          <h4 class="pvz-stat-card-hero__number">{{ orders.length }}</h4>
          <p class="pvz-stat-card-hero__label">Всего заказов</p>
        </div>
        <div class="pvz-stats-grid q-mt-md">
          <div class="pvz-stat-card pvz-stat-card--orange">
            <div class="pvz-stat-card__icon"><q-icon name="local_shipping" size="32px" /></div>
            <h5 class="pvz-stat-card__number">{{ countByStatus('В пути') }}</h5>
            <p class="pvz-stat-card__label">В пути</p>
          </div>
          <div class="pvz-stat-card pvz-stat-card--green">
            <div class="pvz-stat-card__icon"><q-icon name="warehouse" size="32px" /></div>
            <h5 class="pvz-stat-card__number">{{ countByStatus('На складе РФ') }}</h5>
            <p class="pvz-stat-card__label">На складе РФ</p>
          </div>
          <div class="pvz-stat-card pvz-stat-card--blue">
            <div class="pvz-stat-card__icon"><q-icon name="done_all" size="32px" /></div>
            <h5 class="pvz-stat-card__number">{{ countByStatus('Выдан') }}</h5>
            <p class="pvz-stat-card__label">Выдано</p>
          </div>
          <div class="pvz-stat-card pvz-stat-card--grey">
            <div class="pvz-stat-card__icon"><q-icon name="pending" size="32px" /></div>
            <h5 class="pvz-stat-card__number">{{ countOther() }}</h5>
            <p class="pvz-stat-card__label">Другие</p>
          </div>
        </div>
      </div>

    </div><!-- /orders-page-wrapper -->


    <!-- Detail Dialog -->
    <q-dialog v-model="showDetail" transition-show="slide-up" transition-hide="slide-down">
      <q-card class="pvz-detail-dialog">
        <q-card-section class="pvz-detail-dialog__header">
          <div class="title-row">
            <h5>Заказ #{{ selectedOrder?.id }}</h5>
            <q-btn icon="close" flat round dense v-close-popup @click="closeDetail" />
          </div>
          <span :class="['pvz-badge pvz-badge--lg', getStatusClass(selectedOrder?.status)]">
            {{ selectedOrder?.status_display }}
          </span>
        </q-card-section>
        <q-separator />
        <q-card-section class="pvz-detail-dialog__body">
          <div class="detail-section">
            <h6 class="section-title"><q-icon name="person" size="20px" /> Получатель</h6>
            <p class="section-content">{{ selectedOrder?.full_name }}</p>
          </div>
          <div class="detail-section">
            <h6 class="section-title"><q-icon name="payments" size="20px" /> Сумма заказа</h6>
            <p class="section-content section-content--amount">{{ selectedOrder?.amount }} ₽</p>
          </div>
          <div class="detail-section">
            <h6 class="section-title"><q-icon name="place" size="20px" /> Пункт выдачи</h6>
            <p class="section-content">{{ selectedOrder?.pickup_point?.marketplace_display }}</p>
            <p class="section-sub">{{ selectedOrder?.pickup_point?.address }}</p>
          </div>
          <div class="detail-section" v-if="selectedOrder?.comment">
            <h6 class="section-title"><q-icon name="comment" size="20px" /> Комментарий</h6>
            <p class="section-content">{{ selectedOrder?.comment }}</p>
          </div>
          <div class="detail-section" v-if="selectedOrder?.barcode_image">
            <h6 class="section-title"><q-icon name="qr_code" size="20px" /> Штрих-код</h6>
            <div class="barcode-wrapper">
              <img :src="selectedOrder.barcode_image" alt="Barcode" class="barcode-image" />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from 'src/stores/auth-store'
import api from 'src/api/client'

const auth = useAuthStore()
const tab = ref('active')
const orders = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedOrder = ref(null)
const showDetail = ref(false)

const tabs = [
  { value: 'active',  label: 'Активные',  icon: 'inbox',     badge: true  },
  { value: 'history', label: 'Архив',      icon: 'archive',   badge: true  },
  { value: 'stats',   label: 'Статистика', icon: 'bar_chart', badge: false },
]

const DONE = ['Выдан']

const filteredOrders = computed(() => {
  let list = orders.value
  if (tab.value === 'active')  list = list.filter(o => !DONE.includes(o.status))
  if (tab.value === 'history') list = list.filter(o =>  DONE.includes(o.status))
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(o =>
      o.id.toString().includes(q) ||
      o.pickup_point.marketplace.toLowerCase().includes(q) ||
      (o.full_name && o.full_name.toLowerCase().includes(q))
    )
  }
  return list
})

const getTabCount = (v) => {
  if (v === 'active')  return orders.value.filter(o => !DONE.includes(o.status)).length
  if (v === 'history') return orders.value.filter(o =>  DONE.includes(o.status)).length
  return 0
}

const countByStatus = (s) => orders.value.filter(o => o.status === s).length
const countOther = () => orders.value.filter(o => !['В пути','На складе РФ','Выдан'].includes(o.status)).length
const getMarketplaceIcon = (mp) => ({Wildberries:'🟣',Ozon:'🔵','Яндекс.Маркет':'🟡'}[mp] || '📦')
const getStatusClass = (s) => ({'Выдан':'pvz-badge--success','В пути':'pvz-badge--warning','На складе РФ':'pvz-badge--info'}[s] || 'pvz-badge--default')

const goToDetails = (id) => { selectedOrder.value = orders.value.find(o => o.id === id); showDetail.value = true }
const closeDetail = () => { selectedOrder.value = null; showDetail.value = false }

onMounted(async () => {
  loading.value = true
  const ok = await auth.getMe()
  if (!ok) return
  try {
    const res = await api.get('/orders/my_orders/')
    orders.value = await res.json()
  } catch(e) { console.error(e) }
  finally { loading.value = false }
})
</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;
@use 'src/css/mixins' as *;

.orders-list { display: flex; flex-direction: column; gap: 12px; }
.orders-loading { text-align: center; padding: 60px 20px; color: white; p { margin-top: 16px; } }
.stats-section  { display: flex; flex-direction: column; gap: 16px; }

.barcode-wrapper {
  background: #f9fafb; border-radius: 12px; padding: 16px; text-align: center; margin-top: 8px;
}
.barcode-image { max-width: 100%; height: auto; border-radius: 8px; }

// Mobile padding
.orders-page-wrapper {
  padding: 0 $page-padding-x $page-padding-x;
}

.search-wrap { margin-bottom: 0; }
.tabs-wrap   { margin-bottom: 16px; }

.desktop-orders-header { display: none; }
.desktop-create-btn    { display: none; }

// ── Desktop overrides ──────────────────────────────────────
@include desktop {
  .orders-loading { color: $color-text-muted; }
  .orders-loading p { color: $color-text-muted; }

  .desktop-orders-header {
    display: flex;
    margin-bottom: 24px;
  }

  .desktop-create-btn { display: inline-flex; }

  .desktop-orders-toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;

    .search-wrap { flex: 1; max-width: 360px; margin-bottom: 0; padding-bottom: 0; }
    .tabs-wrap   { margin-bottom: 0; }
  }
}
</style>