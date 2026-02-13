<template>
  <q-page class="bg-grey-1">
    <!-- Табы для фильтрации статусов -->
    <q-tabs v-model="tab" dense class="bg-white text-grey" active-color="primary" indicator-color="primary" align="justify" narrow-indicator>
      <q-tab name="active" label="Активные" />
      <q-tab name="history" label="Архив" />
    </q-tabs>

    <q-separator />

    <div class="q-pa-md">
      <!-- Если заказов еще нет -->
      <div v-if="filteredOrders.length === 0" class="text-center q-mt-xl text-grey-6">
        <q-icon name="inventory_2" size="64px" />
        <div class="text-h6">Заказов пока нет</div>
        <q-btn label="Оформить первый" color="primary" flat class="q-mt-sm" @click="$router.push('/add')" />
      </div>

      <!-- Список карточек -->
      <q-list v-else class="q-gutter-y-md">
        <q-card v-for="order in filteredOrders" :key="order.id" flat bordered class="my-card">
          <q-item>
            <q-item-section avatar>
              <q-avatar rounded size="48px" :color="getBrandColor(order.platform)" text-white>
                {{ order.platform.charAt(0) }}
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-weight-bold text-subtitle1">
                {{ order.platform }}
              </q-item-label>
              <q-item-label caption>ID: {{ order.track }}</q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-badge :color="getStatusColor(order.status)" :label="order.status" />
            </q-item-section>
          </q-item>

          <q-separator />

          <q-card-actions align="right" class="bg-grey-1">
            <q-btn flat color="primary" label="Подробнее" icon-right="chevron_right" />
          </q-card-actions>
        </q-card>
      </q-list>
    </div>

    <!-- Кнопка "Плюс" -->
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="$router.push('/add')" />
    </q-page-sticky>
  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'

const tab = ref('active')

// Тестовые данные (потом переедут в Pinia/Backend)
const orders = ref([
  { id: 1, platform: 'Wildberries', track: '99214450', status: 'В пути', archive: false },
  { id: 2, platform: 'Ozon', track: 'OZ-55612', status: 'На складе РФ', archive: false },
  { id: 3, platform: 'СДЭК', track: '1102554', status: 'Выдан', archive: true }
])

const filteredOrders = computed(() => {
  return orders.value.filter(o => tab.value === 'active' ? !o.archive : o.archive)
})

const getBrandColor = (p) => {
  if (p === 'Wildberries') return 'purple-7'
  if (p === 'Ozon') return 'blue-7'
  return 'orange-8'
}

const getStatusColor = (s) => {
  if (s === 'Выдан') return 'grey-7'
  if (s === 'На складе РФ') return 'green'
  return 'orange'
}
</script>
