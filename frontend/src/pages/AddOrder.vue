<template>
  <q-page class="pvz-page">

    <!-- Header -->
    <div class="pvz-page-header">
      <q-btn
        flat round dense
        icon="arrow_back"
        color="white"
        size="md"
        class="back-btn"
        @click="$router.back()"
      />
      <h4 class="header-title">Создать заказ</h4>
      <div class="header-spacer"></div>
    </div>

    <!-- Form Container -->
    <div class="form-container">
      <div class="pvz-card">

        <!-- Progress Steps -->
        <div class="pvz-steps q-mb-lg">
          <div :class="['pvz-step', { active: currentStep === 1, completed: currentStep > 1 }]">
            <div class="pvz-step__circle">1</div>
            <span class="pvz-step__label">Данные</span>
          </div>
          <div class="pvz-step-line" :class="{ active: currentStep > 1 }"></div>
          <div :class="['pvz-step', { active: currentStep === 2, completed: currentStep > 2 }]">
            <div class="pvz-step__circle">2</div>
            <span class="pvz-step__label">Штрих-код</span>
          </div>
          <div class="pvz-step-line" :class="{ active: currentStep > 2 }"></div>
          <div :class="['pvz-step', { active: currentStep === 3 }]">
            <div class="pvz-step__circle">3</div>
            <span class="pvz-step__label">Готово</span>
          </div>
        </div>

        <!-- Step 1: Order Details -->
        <div v-if="currentStep === 1" class="anim-slide-in">
          <q-form @submit.prevent="nextStep">

            <div class="pvz-form-group">
              <label class="pvz-form-label">Пункт выдачи *</label>
              <q-select
                v-model="form.pickupPoint"
                :options="pickupPoints"
                outlined dense
                option-label="display"
                option-value="id"
                placeholder="Выберите пункт выдачи"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[val => val || 'Выберите пункт выдачи']"
              >
                <template v-slot:prepend>
                  <q-icon name="place" color="primary" />
                </template>
                <template v-slot:option="scope">
                  <q-item v-bind="scope.itemProps">
                    <q-item-section avatar>
                      <span class="mp-emoji">{{ getMarketplaceIcon(scope.opt.marketplace) }}</span>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ scope.opt.display }}</q-item-label>
                      <q-item-label caption>{{ scope.opt.address }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </template>
                <template v-slot:selected-item="scope">
                  <div class="selected-item">
                    <span class="mp-emoji">{{ getMarketplaceIcon(scope.opt.marketplace) }}</span>
                    <span>{{ scope.opt.display }}</span>
                  </div>
                </template>
              </q-select>
            </div>

            <div class="pvz-form-group">
              <label class="pvz-form-label">ФИО получателя *</label>
              <q-input
                v-model="form.fullName"
                outlined dense
                placeholder="Иванов Иван Иванович"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[val => val && val.length > 0 || 'Введите ФИО']"
              >
                <template v-slot:prepend>
                  <q-icon name="person" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="pvz-form-group">
              <label class="pvz-form-label">Сумма заказа *</label>
              <q-input
                v-model="form.amount"
                outlined dense
                type="number" min="0"
                placeholder="1000"
                suffix="₽"
                bg-color="grey-1"
                class="pvz-form-input"
                :rules="[
                  val => val && val > 0 || 'Введите сумму',
                  val => val <= 1000000 || 'Слишком большая сумма'
                ]"
              >
                <template v-slot:prepend>
                  <q-icon name="payments" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="pvz-form-group">
              <label class="pvz-form-label">Комментарий (опционально)</label>
              <q-input
                v-model="form.comment"
                outlined dense
                type="textarea"
                rows="3"
                placeholder="Дополнительная информация..."
                bg-color="grey-1"
                class="pvz-form-input pvz-form-input--textarea"
                maxlength="500"
                counter
              >
                <template v-slot:prepend>
                  <q-icon name="comment" color="primary" />
                </template>
              </q-input>
            </div>

            <q-btn
              type="submit"
              label="Продолжить"
              color="primary"
              unelevated rounded
              class="pvz-btn-primary q-mt-xs"
              size="lg"
              icon-right="arrow_forward"
            />
          </q-form>
        </div>

        <!-- Step 2: Barcode Upload -->
        <div v-if="currentStep === 2" class="anim-slide-in">
          <div class="upload-header">
            <h5 class="upload-title">Загрузите штрих-код</h5>
            <p class="upload-subtitle">Сфотографируйте или выберите изображение штрих-кода</p>
          </div>

          <div
            :class="['pvz-upload', {
              'pvz-upload--has-image': form.barcodeImage,
              'pvz-upload--drag-over': isDragging
            }]"
            @click="triggerFileInput"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="onDrop"
          >
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              capture="environment"
              style="display: none"
              @change="onFileSelect"
            />

            <div v-if="!form.barcodeImage" class="pvz-upload__placeholder">
              <q-icon name="qr_code_scanner" size="64px" color="grey-6" />
              <p class="pvz-upload__text">Нажмите или перетащите изображение</p>
              <p class="pvz-upload__hint">JPG, PNG до 10MB</p>
            </div>

            <div v-else class="pvz-upload__preview">
              <img :src="imagePreview" alt="Barcode" class="pvz-upload__image" />
              <q-btn
                flat round dense
                icon="close"
                color="negative"
                class="pvz-upload__remove"
                @click.stop="removeImage"
              />
            </div>
          </div>

          <div class="pvz-btn-group">
            <q-btn
              label="Назад"
              outline color="primary"
              class="pvz-btn-back"
              @click="prevStep"
            />
            <q-btn
              label="Создать заказ"
              color="primary"
              unelevated rounded
              class="pvz-btn-primary"
              icon-right="check"
              :loading="loading"
              :disable="!form.barcodeImage"
              @click="submitOrder"
            />
          </div>
        </div>

        <!-- Step 3: Success -->
        <div v-if="currentStep === 3" class="anim-slide-in">
          <div class="pvz-success">
            <div class="pvz-success__icon">
              <q-icon name="check_circle" size="80px" color="positive" />
            </div>
            <h4 class="pvz-success__title">Заказ создан!</h4>
            <p class="pvz-success__text">
              Ваш заказ <strong>#{{ createdOrderId }}</strong> успешно создан и отправлен в обработку
            </p>

            <div class="pvz-success__summary">
              <div class="summary-item">
                <span class="summary-label">Пункт выдачи:</span>
                <span class="summary-value">{{ form.pickupPoint?.display }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">ФИО:</span>
                <span class="summary-value">{{ form.fullName }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Сумма:</span>
                <span class="summary-value">{{ form.amount }} ₽</span>
              </div>
            </div>

            <div class="pvz-btn-group pvz-btn-group--reverse">
              <q-btn
                label="Создать ещё"
                outline color="primary"
                class="pvz-btn-back"
                icon="add"
                @click="resetForm"
              />
              <q-btn
                label="К заказам"
                color="primary"
                unelevated rounded
                class="pvz-btn-primary"
                icon="inventory_2"
                @click="goToOrders"
              />
            </div>
          </div>
        </div>

      </div>
    </div>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import api from 'src/api/client'
import { useAuthStore } from 'src/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const auth = useAuthStore()

const currentStep = ref(1)
const loading = ref(false)
const isDragging = ref(false)
const pickupPoints = ref([])
const fileInput = ref(null)
const createdOrderId = ref(null)

const form = ref({
  pickupPoint: null,
  fullName: '',
  amount: '',
  comment: '',
  barcodeImage: null,
})

const imagePreview = computed(() =>
  form.value.barcodeImage ? URL.createObjectURL(form.value.barcodeImage) : null
)

const marketplaceMap = {
  ozon: 'Ozon',
  wb: 'Wildberries',
  yandex: 'Яндекс.Маркет',
  cdek: 'СДЭК',
  mail: 'Почта России',
}

const getMarketplaceIcon = (mp) =>
  ({ wb: '🟣', ozon: '🔵', yandex: '🟡', cdek: '🟢', mail: '📮' }[mp] || '📦')

const fetchPickupPoints = async () => {
  try {
    const res = await api.get('/pickup-points/')
    if (res.ok) {
      const data = await res.json()
      pickupPoints.value = data.map(pp => ({
        ...pp,
        display: `${marketplaceMap[pp.marketplace] || pp.marketplace} - ${pp.address.substring(0, 30)}${pp.address.length > 30 ? '...' : ''}`,
      }))
    }
  } catch (err) {
    console.error(err)
    $q.notify({ color: 'negative', message: 'Не удалось загрузить пункты выдачи', position: 'top', icon: 'error' })
  }
}

const nextStep = () => currentStep.value++
const prevStep = () => currentStep.value--

const triggerFileInput = () => fileInput.value.click()

const onFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) validateAndSetImage(file)
}

const onDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) validateAndSetImage(file)
}

const validateAndSetImage = (file) => {
  if (!file.type.startsWith('image/')) {
    $q.notify({ color: 'negative', message: 'Пожалуйста, выберите изображение', position: 'top', icon: 'error' })
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    $q.notify({ color: 'negative', message: 'Файл слишком большой (макс. 10MB)', position: 'top', icon: 'error' })
    return
  }
  form.value.barcodeImage = file
}

const removeImage = () => {
  form.value.barcodeImage = null
  if (fileInput.value) fileInput.value.value = ''
}

const submitOrder = async () => {
  if (!form.value.barcodeImage) {
    $q.notify({ color: 'negative', message: 'Загрузите штрих-код', position: 'top', icon: 'error' })
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('pickup_point_id', form.value.pickupPoint.id)
    formData.append('full_name', form.value.fullName)
    formData.append('amount', form.value.amount)
    if (form.value.comment) formData.append('comment', form.value.comment)
    formData.append('barcode_image', form.value.barcodeImage)

    const res = await api.postMultipart('/orders/', formData)

    if (res.ok) {
      const data = await res.json()
      createdOrderId.value = data.id
      currentStep.value = 3
      $q.notify({ color: 'positive', message: 'Заказ успешно создан! 🎉', position: 'top', icon: 'check_circle' })
    } else {
      const err = await res.json()
      throw new Error(err.detail || 'Ошибка при создании заказа')
    }
  } catch (err) {
    console.error(err)
    $q.notify({ color: 'negative', message: err.message || 'Не удалось создать заказ', position: 'top', icon: 'error' })
  } finally {
    loading.value = false
  }
}

const goToOrders = () => router.push('/')

const resetForm = () => {
  form.value = { pickupPoint: null, fullName: '', amount: '', comment: '', barcodeImage: null }
  currentStep.value = 1
  createdOrderId.value = null
}

onMounted(async () => {
  const meOk = await auth.getMe()
  if (!meOk) { router.push('/login'); return }
  await fetchPickupPoints()
})
</script>

<style lang="scss" scoped>
// Только уникальное для этой страницы

.form-container {
  padding: 20px 16px;
  max-width: 600px;
  margin: 0 auto;
}

// Шаг загрузки — заголовок
.upload-header {
  text-align: center;
  margin-bottom: 24px;

  .upload-title {
    margin: 0 0 8px;
    font-size: 20px;
    font-weight: 700;
    color: #2c3e50;
  }
  .upload-subtitle {
    margin: 0;
    font-size: 14px;
    color: #6b7280;
  }
}

// Emoji в селекте — маленький нюанс
.mp-emoji      { font-size: 20px; }
.selected-item { display: flex; align-items: center; gap: 8px; }

// Реверс кнопок на шаге успеха (сначала "Создать ещё", потом "К заказам")
.pvz-btn-group--reverse {
  .pvz-btn-back { order: 1; }
  .pvz-btn-primary { order: 2; }
}
</style>