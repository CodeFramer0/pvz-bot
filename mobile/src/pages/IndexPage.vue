<template>
  <q-page class="bg-gradient">
    <div class="page-wrapper q-pa-md">

      <!-- Header -->
      <div class="header text-center q-mb-lg">
        <div class="logo">🛒</div>
        <h3 class="text-h4 text-weight-bold">Привет, {{ auth.user?.username || 'Гость' }} 👋</h3>
        <p class="subtitle">Ваши заказы и статистика</p>
      </div>

      <!-- Tabs -->
      <q-tabs
        v-model="tab"
        dense
        class="bg-white text-grey rounded-tabs"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="active" label="Активные" />
        <q-tab name="history" label="Архив" />
        <q-tab name="stats" label="Статистика" />
      </q-tabs>

      <q-separator />

      <!-- Content -->
      <div class="q-pa-md">
        <q-spinner v-if="loading" size="50px" color="white" class="q-my-xl" />

        <div v-else>
          <!-- Пустой экран -->
          <div v-if="filteredOrders.length === 0 && tab !== 'stats'" class="text-center q-mt-xl text-white-6">
            <q-icon name="inventory_2" size="64px" />
            <div class="text-h6 q-mt-sm">Заказов пока нет</div>
            <q-btn label="Создать первый заказ" color="primary" flat class="q-mt-sm" @click="$router.push('/add')" />
          </div>

          <!-- Список заказов -->
          <div v-else-if="tab !== 'stats'" class="order-list">
            <q-card
              v-for="order in filteredOrders"
              :key="order.id"
              flat
              class="order-card q-my-xs"
              @click="goToDetails(order.id)"
            >
              <div class="order-content row items-center justify-between">
                <div>
                  <div class="text-h6 text-white">{{ order.pickup_point.marketplace }}</div>
                  <div class="text-subtitle2 text-white-5">ID: {{ order.id }}</div>
                </div>
                <q-badge :color="getStatusColor(order.status)" :label="order.status" />
              </div>
            </q-card>
          </div>

          <!-- Статистика -->
          <div v-else class="stats-wrapper q-gutter-md">
            <q-card flat class="stat-card q-pa-md q-mb-md">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-subtitle1 text-white-7">Всего заказов</div>
                  <div class="text-h5 text-white text-weight-bold">{{ orders.length }}</div>
                </div>
                <q-icon name="inventory_2" size="48px" class="text-white" />
              </div>
            </q-card>

            <div class="row q-gutter-sm">
              <q-card flat class="col stat-card text-center">
                <div class="text-subtitle2 text-white-6">В пути</div>
                <div class="text-h5 text-orange-6 text-weight-bold">{{ orders.filter(o => o.status === 'В пути').length }}</div>
              </q-card>
              <q-card flat class="col stat-card text-center">
                <div class="text-subtitle2 text-white-6">На складе РФ</div>
                <div class="text-h5 text-green-6 text-weight-bold">{{ orders.filter(o => o.status === 'На складе РФ').length }}</div>
              </q-card>
              <q-card flat class="col stat-card text-center">
                <div class="text-subtitle2 text-white-6">Выдано</div>
                <div class="text-h5 text-grey-5 text-weight-bold">{{ orders.filter(o => o.status === 'Выдан').length }}</div>
              </q-card>
            </div>
          </div>
        </div>
      </div>

      <!-- Floating Add Button -->
      <q-page-sticky position="bottom-right" :offset="[18,18]">
        <q-btn fab icon="add" color="primary" @click="$router.push('/add')" glossy />
      </q-page-sticky>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from 'src/stores/auth-store'
import api from 'src/api/client'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const tab = ref('active')
const orders = ref([])
const loading = ref(true)

const filteredOrders = computed(() => {
  if(tab.value==='active') return orders.value.filter(o => !['Выдан'].includes(o.status))
  if(tab.value==='history') return orders.value.filter(o => ['Выдан'].includes(o.status))
  return orders.value
})

const getStatusColor = status => {
  switch(status){
    case 'Выдан': return 'grey-7'
    case 'На складе РФ': return 'green'
    case 'В пути': return 'orange'
    default: return 'blue'
  }
}

const goToDetails = id => router.push(`/orders/${id}`)

onMounted(async () => {
  loading.value = true
  const meOk = await auth.getMe()
  if(!meOk) return
  try {
    const res = await api.get('orders/my_orders/')
    orders.value = await res.json()
  } catch(err) { console.error(err) }
  finally { loading.value=false }
})
</script>

<style scoped>
.bg-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
.page-wrapper { width: 100%; max-width: 480px; margin: 0 auto; }
.header { margin-bottom: 20px; }
.logo { font-size: 48px; margin-bottom: 10px; }
h3 { margin: 0; color: #fff; }
.subtitle { margin: 0; color: #ddd; font-size: 14px; }
.rounded-tabs { border-radius: 12px; }
.order-list { display: flex; flex-direction: column; gap: 12px; }
.order-card { background: rgba(255,255,255,0.1); padding: 16px; border-radius: 16px; cursor: pointer; transition: transform 0.2s; }
.order-card:hover { transform: translateY(-2px); background: rgba(255,255,255,0.15); }
.order-content { display: flex; justify-content: space-between; align-items: center; }
.stat-card { background: rgba(255,255,255,0.15); border-radius: 16px; }
.stats-wrapper { display: flex; flex-direction: column; gap: 12px; }
</style>
