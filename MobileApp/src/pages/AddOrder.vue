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

const onSubmit = async () => {
  const success = await store.addOrder(form.value)
  
  if (success) {
    $q.notify({ color: 'positive', message: 'Заказ отправлен!' })
    router.push('/')
  } else {
    $q.notify({ color: 'negative', message: 'Ошибка при отправке' })
  }
}
</script>
