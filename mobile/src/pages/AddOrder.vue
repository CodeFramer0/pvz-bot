<script setup>
import { ref } from 'vue'
import { useOrderStore } from 'src/stores/order-store'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const store = useOrderStore()
const router = useRouter()
const $q = useQuasar()

const form = ref({
  platform: 'Wildberries',
  track: '',
  photo: null,
  comment: ''
})

const loading = ref(false)

const onSubmit = async () => {
  loading.value = true
  try {
    const success = await store.addOrder(form.value)
    
    if (success) {
      $q.notify({ 
        color: 'positive', 
        message: 'Заказ отправлен!',
        position: 'top'
      })
      router.push('/')
    } else {
      $q.notify({ 
        color: 'negative', 
        message: 'Ошибка при отправке',
        position: 'top'
      })
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="q-pa-md">
    <h5>Добавить заказ</h5>
    
    <q-form @submit.prevent="onSubmit" class="q-gutter-md">
      <q-select
        v-model="form.platform"
        label="Платформа"
        :options="['Wildberries', 'Ozon', 'Yandex Market']"
        outlined
        emit-value
        map-options
      />

      <q-input
        v-model="form.track"
        label="Трек-номер"
        outlined
        :rules="[val => val && val.length > 0 || 'Введите трек-номер']"
      />

      <q-file
        v-model="form.photo"
        label="Фото заказа"
        outlined
        accept="image/*"
        max-file-size="5242880"
        @rejected="onFileRejected"
      />

      <q-input
        v-model="form.comment"
        label="Комментарий"
        type="textarea"
        outlined
        rows="4"
      />

      <div class="q-gutter-md row">
        <q-btn
          type="submit"
          label="Отправить"
          color="primary"
          :loading="loading"
        />
        <q-btn
          label="Отмена"
          color="grey-7"
          flat
          @click="router.back()"
        />
      </div>
    </q-form>
  </div>
</template>

<style scoped>
h5 {
  margin-top: 0;
  margin-bottom: 20px;
}
</style>