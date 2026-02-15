<template>
  <q-page class="orders-page">
    <!-- Hero Header -->
    <div class="hero-header">
      <div class="header-content">
        <div class="greeting-section">
          <h3 class="greeting-text">Привет, {{ auth.user?.username || 'Гость' }} 👋</h3>
          <p class="greeting-subtitle">Управляй своими заказами</p>
        </div>
        <q-btn 
          flat 
          round 
          dense 
          icon="account_circle" 
          class="profile-btn"
          @click="$router.push('/profile')"
        />
      </div>
    </div>

    <!-- Search & Filter Bar -->
    <div class="search-section q-px-md q-pb-md">
      <q-input
        v-model="searchQuery"
        outlined
        dense
        placeholder="Поиск по ID или маркетплейсу..."
        bg-color="white"
        class="search-input"
      >
        <template v-slot:prepend>
          <q-icon name="search" />
        </template>
        <template v-slot:append v-if="searchQuery">
          <q-icon name="clear" @click="searchQuery = ''" class="cursor-pointer" />
        </template>
      </q-input>
    </div>

    <!-- Stylish Tabs -->
    <div class="tabs-container q-px-md">
      <div class="custom-tabs">
        <div 
          v-for="t in tabs" 
          :key="t.value"
          :class="['tab-item', { active: tab === t.value }]"
          @click="tab = t.value"
        >
          <q-icon :name="t.icon" size="20px" />
          <span class="tab-label">{{ t.label }}</span>
          <div class="tab-badge" v-if="t.badge && getTabCount(t.value) > 0">
            {{ getTabCount(t.value) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="content-section q-px-md q-pb-xl">
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <q-spinner-dots color="primary" size="50px" />
        <p class="loading-text">Загружаем заказы...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredOrders.length === 0 && tab !== 'stats'" class="empty-state">
        <div class="empty-icon">📦</div>
        <h5 class="empty-title">{{ tab === 'active' ? 'Нет активных заказов' : 'История пуста' }}</h5>
        <p class="empty-text">{{ tab === 'active' ? 'Создай свой первый заказ!' : 'Завершенные заказы появятся здесь' }}</p>
        <q-btn 
          v-if="tab === 'active'"
          label="Создать заказ" 
          color="primary" 
          unelevated 
          rounded
          class="q-mt-md"
          icon="add"
          @click="$router.push('/add')" 
        />
      </div>

      <!-- Orders List -->
      <div v-else-if="tab !== 'stats'" class="orders-list">
        <transition-group name="list">
          <div
            v-for="order in filteredOrders"
            :key="order.id"
            class="order-card"
            @click="goToDetails(order.id)"
          >
            <div class="order-header">
              <div class="marketplace-info">
                <div class="marketplace-icon">
                  {{ getMarketplaceIcon(order.pickup_point.marketplace) }}
                </div>
                <div class="marketplace-details">
                  <h6 class="marketplace-name">{{ order.pickup_point.marketplace }}</h6>
                  <p class="order-id">ID: {{ order.id }}</p>
                </div>
              </div>
              <q-badge 
                :class="['status-badge', getStatusClass(order.status)]"
                :label="order.status"
              />
            </div>
            
            <div class="order-body">
              <div class="order-info-row">
                <q-icon name="person" size="16px" color="grey-6" />
                <span>{{ order.full_name || 'Не указано' }}</span>
              </div>
              <div class="order-info-row">
                <q-icon name="payments" size="16px" color="grey-6" />
                <span class="order-amount">{{ order.amount }} ₽</span>
              </div>
              <div class="order-info-row">
                <q-icon name="place" size="16px" color="grey-6" />
                <span class="order-address">{{ order.pickup_point.address }}</span>
              </div>
            </div>

            <div class="order-footer">
              <q-icon name="chevron_right" size="20px" color="grey-5" />
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Statistics -->
      <div v-else class="stats-section">
        <div class="stat-card-big">
          <div class="stat-big-icon">📊</div>
          <h4 class="stat-big-number">{{ orders.length }}</h4>
          <p class="stat-big-label">Всего заказов</p>
        </div>

        <div class="stats-grid">
          <div class="stat-card stat-orange">
            <div class="stat-icon-wrapper">
              <q-icon name="local_shipping" size="32px" />
            </div>
            <h5 class="stat-number">{{ orders.filter(o => o.status === 'В пути').length }}</h5>
            <p class="stat-label">В пути</p>
          </div>

          <div class="stat-card stat-green">
            <div class="stat-icon-wrapper">
              <q-icon name="warehouse" size="32px" />
            </div>
            <h5 class="stat-number">{{ orders.filter(o => o.status === 'На складе РФ').length }}</h5>
            <p class="stat-label">На складе РФ</p>
          </div>

          <div class="stat-card stat-blue">
            <div class="stat-icon-wrapper">
              <q-icon name="done_all" size="32px" />
            </div>
            <h5 class="stat-number">{{ orders.filter(o => o.status === 'Выдан').length }}</h5>
            <p class="stat-label">Выдано</p>
          </div>

          <div class="stat-card stat-grey">
            <div class="stat-icon-wrapper">
              <q-icon name="pending" size="32px" />
            </div>
            <h5 class="stat-number">{{ orders.filter(o => !['В пути', 'На складе РФ', 'Выдан'].includes(o.status)).length }}</h5>
            <p class="stat-label">Другие</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating Add Button -->
    <q-page-sticky position="bottom-right" :offset="[18, 78]">
      <q-btn 
        fab 
        icon="add" 
        color="primary" 
        @click="$router.push('/add')"
        class="fab-btn"
      >
        <q-tooltip anchor="center left" self="center right" :offset="[10, 0]">
          Создать заказ
        </q-tooltip>
      </q-btn>
    </q-page-sticky>

    <!-- Order Detail Dialog -->
    <q-dialog v-model="showDetail" transition-show="slide-up" transition-hide="slide-down">
      <q-card class="detail-card">
        <q-card-section class="detail-header">
          <div class="detail-title-row">
            <h5 class="detail-title">Заказ #{{ selectedOrder?.id }}</h5>
            <q-btn 
              icon="close" 
              flat 
              round 
              dense 
              v-close-popup
              @click="closeDetail"
            />
          </div>
          <q-badge 
            :class="['status-badge-large', getStatusClass(selectedOrder?.status)]"
            :label="selectedOrder?.status"
          />
        </q-card-section>

        <q-separator />

        <q-card-section class="detail-body">
          <div class="detail-section">
            <h6 class="section-title">
              <q-icon name="person" size="20px" />
              Получатель
            </h6>
            <p class="section-content">{{ selectedOrder?.full_name }}</p>
          </div>

          <div class="detail-section">
            <h6 class="section-title">
              <q-icon name="payments" size="20px" />
              Сумма заказа
            </h6>
            <p class="section-content amount">{{ selectedOrder?.amount }} ₽</p>
          </div>

          <div class="detail-section">
            <h6 class="section-title">
              <q-icon name="place" size="20px" />
              Пункт выдачи
            </h6>
            <p class="section-content">{{ selectedOrder?.pickup_point.marketplace_display }}</p>
            <p class="section-subcontent">{{ selectedOrder?.pickup_point.address }}</p>
          </div>

          <div class="detail-section" v-if="selectedOrder?.comment">
            <h6 class="section-title">
              <q-icon name="comment" size="20px" />
              Комментарий
            </h6>
            <p class="section-content">{{ selectedOrder?.comment }}</p>
          </div>

          <div class="detail-section" v-if="selectedOrder?.barcode_image">
            <h6 class="section-title">
              <q-icon name="qr_code" size="20px" />
              Штрих-код
            </h6>
            <div class="barcode-wrapper">
              <img :src="selectedOrder.barcode_image" alt="Barcode" class="barcode-image"/>
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
  { value: 'active', label: 'Активные', icon: 'inbox', badge: true },
  { value: 'history', label: 'Архив', icon: 'archive', badge: true },
  { value: 'stats', label: 'Статистика', icon: 'bar_chart', badge: false }
]

const filteredOrders = computed(() => {
  let filtered = orders.value
  
  if (tab.value === 'active') {
    filtered = filtered.filter(o => !['Выдан'].includes(o.status))
  } else if (tab.value === 'history') {
    filtered = filtered.filter(o => ['Выдан'].includes(o.status))
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(o => 
      o.id.toString().includes(query) ||
      o.pickup_point.marketplace.toLowerCase().includes(query) ||
      (o.full_name && o.full_name.toLowerCase().includes(query))
    )
  }

  return filtered
})

const getTabCount = (tabValue) => {
  if (tabValue === 'active') {
    return orders.value.filter(o => !['Выдан'].includes(o.status)).length
  } else if (tabValue === 'history') {
    return orders.value.filter(o => ['Выдан'].includes(o.status)).length
  }
  return 0
}

const getStatusClass = (status) => {
  const statusMap = {
    'Выдан': 'status-completed',
    'На складе РФ': 'status-warehouse',
    'В пути': 'status-transit',
  }
  return statusMap[status] || 'status-default'
}

const getMarketplaceIcon = (marketplace) => {
  const icons = {
    'Wildberries': '🟣',
    'Ozon': '🔵',
    'Яндекс.Маркет': '🟡',
    'AliExpress': '🔴'
  }
  return icons[marketplace] || '📦'
}

const goToDetails = (id) => {
  selectedOrder.value = orders.value.find(o => o.id === id)
  showDetail.value = true
}

const closeDetail = () => {
  selectedOrder.value = null
  showDetail.value = false
}

onMounted(async () => {
  loading.value = true
  const meOk = await auth.getMe()
  if (!meOk) return
  
  try {
    const res = await api.get('/orders/my_orders/')
    orders.value = await res.json()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.orders-page {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding-bottom: 80px;
}

/* Hero Header */
.hero-header {
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
  backdrop-filter: blur(10px);
  padding: 24px 16px;
  border-radius: 0 0 24px 24px;
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.greeting-section {
  flex: 1;
}

.greeting-text {
  margin: 0;
  color: white;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.greeting-subtitle {
  margin: 4px 0 0 0;
  color: rgba(255,255,255,0.8);
  font-size: 14px;
}

.profile-btn {
  color: white;
  font-size: 32px;
}

/* Search Section */
.search-section {
  margin-bottom: 16px;
}

.search-input {
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.search-input :deep(.q-field__control) {
  border-radius: 16px;
}

/* Custom Tabs */
.tabs-container {
  margin-bottom: 20px;
}

.custom-tabs {
  display: flex;
  gap: 8px;
  background: rgba(255,255,255,0.15);
  padding: 6px;
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255,255,255,0.7);
  position: relative;
}

.tab-item.active {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.tab-label {
  font-size: 12px;
  font-weight: 600;
}

.tab-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #ff4444;
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

/* Content */
.content-section {
  margin-top: 8px;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.loading-text {
  color: white;
  margin-top: 16px;
  font-size: 14px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255,255,255,0.1);
  border-radius: 24px;
  backdrop-filter: blur(10px);
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-title {
  margin: 0 0 8px 0;
  color: white;
  font-size: 20px;
  font-weight: 600;
}

.empty-text {
  margin: 0;
  color: rgba(255,255,255,0.8);
  font-size: 14px;
}

/* Orders List */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.order-card {
  background: white;
  border-radius: 20px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.order-card:active {
  transform: scale(0.98);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.marketplace-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.marketplace-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
}

.marketplace-details {
  flex: 1;
}

.marketplace-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.order-id {
  margin: 2px 0 0 0;
  font-size: 12px;
  color: #95a5a6;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-completed {
  background: #ecfdf5;
  color: #059669;
}

.status-warehouse {
  background: #f0fdf4;
  color: #16a34a;
}

.status-transit {
  background: #fff7ed;
  color: #ea580c;
}

.status-default {
  background: #f3f4f6;
  color: #6b7280;
}

.order-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.order-info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #4b5563;
}

.order-amount {
  font-weight: 600;
  color: #667eea;
}

.order-address {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.order-footer {
  display: flex;
  justify-content: flex-end;
}

/* Statistics */
.stats-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-card-big {
  background: white;
  border-radius: 24px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.stat-big-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.stat-big-number {
  margin: 0;
  font-size: 48px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-big-label {
  margin: 8px 0 0 0;
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.2s;
}

.stat-card:active {
  transform: scale(0.95);
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  margin: 0 auto 12px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-orange .stat-icon-wrapper {
  background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%);
  color: #ea580c;
}

.stat-green .stat-icon-wrapper {
  background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
  color: #16a34a;
}

.stat-blue .stat-icon-wrapper {
  background: linear-gradient(135deg, #eff6ff 0%, #bfdbfe 100%);
  color: #2563eb;
}

.stat-grey .stat-icon-wrapper {
  background: linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%);
  color: #6b7280;
}

.stat-number {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
}

.stat-label {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

/* FAB */
.fab-btn {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

/* Detail Dialog */
.detail-card {
  border-radius: 24px 24px 0 0;
  max-width: 100%;
}

.detail-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px;
}

.detail-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.detail-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.status-badge-large {
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.detail-body {
  padding: 24px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-content {
  margin: 0;
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
}

.section-content.amount {
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
}

.section-subcontent {
  margin: 4px 0 0 0;
  font-size: 14px;
  color: #6b7280;
}

.barcode-wrapper {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  margin-top: 8px;
}

.barcode-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

@media (max-width: 600px) {
  .greeting-text {
    font-size: 20px;
  }
  
  .tab-label {
    font-size: 11px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
