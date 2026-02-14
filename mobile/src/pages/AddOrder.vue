<template>
  <q-page class="bg-gradient">
    <div class="q-pa-md page-container">
      <div class="form-card q-pa-xl q-mb-lg">
        <div class="form-header text-center">
          <div class="form-logo">🛒</div>
          <h4>Создать заказ</h4>
          <p class="subtitle">Добавьте новый заказ для отслеживания</p>
        </div>

        <q-form @submit.prevent="onSubmit" class="q-gutter-md">
          <q-select
            v-model="form.pickup_point"
            label="Пункт выдачи"
            :options="pickupOptions"
            option-label="label"
            option-value="value"
            outlined
            dense
            required
          />

          <q-input
            v-model="form.full_name"
            label="ФИО"
            outlined
            dense
            :rules="[val => !!val || 'Введите ФИО']"
            required
          />

          <q-input
            v-model="form.amount"
            label="Сумма заказа"
            outlined
            dense
            type="number"
            :rules="[val => !!val || 'Введите сумму']"
            required
          />

          <q-file
            v-model="form.barcode_image"
            label="Фото штрих-кода"
            outlined
            dense
            accept="image/*"
            max-file-size="5242880"
            @rejected="onFileRejected"
            required
          />

          <q-input
            v-model="form.comment"
            label="Комментарий (не обязательно)"
            type="textarea"
            outlined
            dense
            rows="4"
          />

          <div class="row q-gutter-md justify-end q-mt-md">
            <q-btn type="submit" label="Создать заказ" color="primary" :loading="loading" unelevated rounded />
            <q-btn label="Отмена" color="grey-7" flat rounded @click="router.back()" />
          </div>
        </q-form>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import api from 'src/api/client'

const router = useRouter()
const $q = useQuasar()
const loading = ref(false)
const form = ref({
  pickup_point: null,
  full_name: '',
  amount: '',
  barcode_image: null,
  comment: ''
})
const pickupPoints = ref([])
const pickupOptions = ref([])

onMounted(async () => {
  try {
    const res = await api.get('pickup-points/')
    const data = await res.json()
    pickupPoints.value = data
    pickupOptions.value = data.map(p => ({ label: `${p.marketplace} - ${p.address}`, value: p.id }))
  } catch {
    $q.notify({ color: 'negative', message: 'Не удалось загрузить пункты выдачи', position: 'top' })
  }
})

const onFileRejected = () => $q.notify({ color: 'negative', message: 'Файл не подходит', position: 'top' })

const onSubmit = async () => {
  if (!form.value.pickup_point || !form.value.full_name || !form.value.amount || !form.value.barcode_image) {
    $q.notify({ color: 'negative', message: 'Заполните все обязательные поля', position: 'top' })
    return
  }
  loading.value = true
  try {
    const data = new FormData()
    Object.entries(form.value).forEach(([k, v]) => v && data.append(k, v))
    const res = await api.postMultipart('orders/', data)
    if (res.ok) {
      $q.notify({ color: 'positive', message: 'Заказ создан!', position: 'top' })
      router.push('/orders')
    } else {
      const err = await res.json()
      $q.notify({ color: 'negative', message: err.detail || 'Ошибка при создании заказа', position: 'top' })
    }
  } finally { loading.value = false }
}
</script>

<style scoped>
.bg-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; }
.page-container { width: 100%; max-width: 500px; }
.form-card { background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.form-header { margin-bottom: 20px; }
.form-logo { font-size: 48px; margin-bottom: 10px; }
h4 { margin: 0 0 5px 0; color: #333; font-weight: 600; }
.subtitle { margin: 0; color: #999; font-size: 14px; }
</style>
