<template>
  <q-page class="pvz-page detail-page">

    <!-- Header -->
    <div class="detail-hero">
      <q-btn
        flat round dense
        icon="arrow_back"
        color="white"
        class="detail-back"
        @click="$router.back()"
      />

      <div v-if="!loading && order" class="detail-hero__body">
        <div class="detail-hero__mp-icon">
          {{ getMarketplaceIcon(order.pickup_point?.marketplace) }}
        </div>
        <p class="detail-hero__mp-name">{{ order.pickup_point?.marketplace }}</p>
        <h2 class="detail-hero__order-id">Заказ #{{ order.id }}</h2>
        <span :class="['status-chip', getStatusClass(order.status)]">
          <span class="status-chip__dot"></span>
          {{ order.status_display }}
        </span>
      </div>

      <div v-else-if="loading" class="detail-hero__body">
        <div class="detail-hero__order-id">Загружаем...</div>
      </div>

      <!-- Decorative wave -->
      <svg class="detail-hero__wave" viewBox="0 0 375 40" preserveAspectRatio="none">
        <path d="M0,20 C60,40 120,0 180,20 C240,40 300,0 375,20 L375,40 L0,40 Z" fill="white"/>
      </svg>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="orders-loading">
      <q-spinner-dots color="primary" size="50px" />
      <p>Загружаем заказ...</p>
    </div>

    <!-- Not found -->
    <div v-else-if="!order" class="pvz-empty">
      <div class="empty-icon anim-float-y">📦</div>
      <h5 class="empty-title">Заказ не найден</h5>
      <p class="empty-text">Попробуйте обновить страницу</p>
    </div>

    <!-- Content -->
    <div v-else class="detail-content">

      <!-- Основная информация -->
      <div class="detail-card anim-slide-in" style="animation-delay: 0.05s">
        <div class="detail-card__row">
          <div class="detail-card__icon-wrap detail-card__icon-wrap--blue">
            <q-icon name="person" size="20px" />
          </div>
          <div class="detail-card__info">
            <span class="detail-card__label">Получатель</span>
            <span class="detail-card__value">{{ order.full_name }}</span>
          </div>
        </div>

        <div class="detail-card__divider"></div>

        <div class="detail-card__row">
          <div class="detail-card__icon-wrap detail-card__icon-wrap--purple">
            <q-icon name="payments" size="20px" />
          </div>
          <div class="detail-card__info">
            <span class="detail-card__label">Сумма заказа</span>
            <span class="detail-card__value detail-card__value--amount">{{ order.amount }} ₽</span>
          </div>
        </div>

        <div class="detail-card__divider"></div>

        <div class="detail-card__row">
          <div class="detail-card__icon-wrap detail-card__icon-wrap--green">
            <q-icon name="place" size="20px" />
          </div>
          <div class="detail-card__info">
            <span class="detail-card__label">Пункт выдачи</span>
            <span class="detail-card__value">{{ order.pickup_point.marketplace_display }}</span>
            <span class="detail-card__sub">{{ order.pickup_point.address }}</span>
          </div>
        </div>
      </div>

      <!-- Комментарий -->
      <div v-if="order.comment" class="detail-card anim-slide-in" style="animation-delay: 0.1s">
        <div class="detail-card__row">
          <div class="detail-card__icon-wrap detail-card__icon-wrap--orange">
            <q-icon name="comment" size="20px" />
          </div>
          <div class="detail-card__info">
            <span class="detail-card__label">Комментарий</span>
            <span class="detail-card__value detail-card__value--comment">{{ order.comment }}</span>
          </div>
        </div>
      </div>

      <!-- Штрих-код -->
      <div v-if="order.barcode_image" class="detail-card detail-card--barcode anim-slide-in" style="animation-delay: 0.15s">
        <div class="barcode-header">
          <div class="detail-card__icon-wrap detail-card__icon-wrap--grey">
            <q-icon name="qr_code" size="20px" />
          </div>
          <span class="detail-card__label">Штрих-код</span>
        </div>
        <div class="barcode-frame">
          <div class="barcode-corner barcode-corner--tl"></div>
          <div class="barcode-corner barcode-corner--tr"></div>
          <div class="barcode-corner barcode-corner--bl"></div>
          <div class="barcode-corner barcode-corner--br"></div>
          <img :src="order.barcode_image" alt="Barcode" class="barcode-img" />
        </div>
      </div>

    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from 'src/api/client'

const route = useRoute()
const order = ref(null)
const loading = ref(true)

const getMarketplaceIcon = (mp) =>
  ({ Wildberries: '🟣', Ozon: '🔵', 'Яндекс.Маркет': '🟡', СДЭК: '🟢' }[mp] || '📦')

const getStatusClass = (status) => ({
  'Выдан':         'status-chip--success',
  'В пути':        'status-chip--warning',
  'На складе РФ':  'status-chip--info',
}[status] || 'status-chip--default')

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get(`/orders/${route.params.id}/`)
    order.value = await res.json()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
@use 'src/css/variables' as *;

// ─── Hero ────────────────────────────────────────────────────

.detail-hero {
  position: relative;
  background: $gradient-brand;
  padding: 16px 20px 52px; // 52px запас под волну
  min-height: 220px;
  display: flex;
  flex-direction: column;

  &__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 12px 0 24px;
    text-align: center;
  }

  &__mp-icon {
    font-size: 48px;
    margin-bottom: 8px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    animation: bounce 0.7s ease-in-out;
  }

  &__mp-name {
    margin: 0 0 4px;
    color: rgba(255,255,255,0.8);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  &__order-id {
    margin: 0 0 16px;
    color: white;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }

  &__wave {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 40px;
  }
}

.detail-back {
  color: white;
  align-self: flex-start;
}

// ─── Status Chip ─────────────────────────────────────────────

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.3px;
  backdrop-filter: blur(10px);

  &__dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
  }

  &--success {
    background: rgba(16, 185, 129, 0.2);
    color: #ecfdf5;
    border: 1px solid rgba(16, 185, 129, 0.4);
    .status-chip__dot { background: #10b981; }
  }
  &--warning {
    background: rgba(234, 88, 12, 0.2);
    color: #fff7ed;
    border: 1px solid rgba(234, 88, 12, 0.4);
    .status-chip__dot { background: #ea580c; }
  }
  &--info {
    background: rgba(37, 99, 235, 0.2);
    color: #eff6ff;
    border: 1px solid rgba(37, 99, 235, 0.4);
    .status-chip__dot { background: #3b82f6; }
  }
  &--default {
    background: rgba(255,255,255,0.15);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
    .status-chip__dot { background: rgba(255,255,255,0.7); }
  }
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.7); }
}

// ─── Content ─────────────────────────────────────────────────

.detail-content {
  padding: 16px 16px 32px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

// ─── Detail Cards ─────────────────────────────────────────────

.detail-card {
  background: white;
  border-radius: 20px;
  padding: 6px 0;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  overflow: hidden;

  &__row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 18px;
  }

  &__divider {
    height: 1px;
    background: #f3f4f6;
    margin: 0 18px;
  }

  &__icon-wrap {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-top: 2px;

    &--blue   { background: linear-gradient(135deg, #60a5fa, #3b82f6); }
    &--purple { background: linear-gradient(135deg, $primary-start, $primary-end); }
    &--green  { background: linear-gradient(135deg, #34d399, #10b981); }
    &--orange { background: linear-gradient(135deg, #fb923c, #ea580c); }
    &--grey   { background: linear-gradient(135deg, #9ca3af, #6b7280); }
  }

  &__info {
    display: flex;
    flex-direction: column;
    gap: 3px;
    flex: 1;
  }

  &__label {
    font-size: 11px;
    font-weight: 600;
    color: $color-text-hint;
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  &__value {
    font-size: 15px;
    font-weight: 600;
    color: $color-text-dark;
    line-height: 1.4;

    &--amount {
      font-size: 22px;
      font-weight: 700;
      background: $gradient-brand;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    &--comment {
      font-weight: 500;
      color: $color-text-body;
      line-height: 1.5;
    }
  }

  &__sub {
    font-size: 13px;
    color: $color-text-muted;
    line-height: 1.4;
    margin-top: 1px;
  }

  // Barcode card variant
  &--barcode {
    padding: 18px;
  }
}

// ─── Barcode ─────────────────────────────────────────────────

.barcode-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;

  .detail-card__label {
    font-size: 13px;
  }
}

.barcode-frame {
  position: relative;
  background: #f9fafb;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}

// Угловые декоративные скобки
.barcode-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border-color: $primary-start;
  border-style: solid;

  &--tl { top: 8px; left: 8px;  border-width: 2px 0 0 2px; border-radius: 4px 0 0 0; }
  &--tr { top: 8px; right: 8px; border-width: 2px 2px 0 0; border-radius: 0 4px 0 0; }
  &--bl { bottom: 8px; left: 8px;  border-width: 0 0 2px 2px; border-radius: 0 0 0 4px; }
  &--br { bottom: 8px; right: 8px; border-width: 0 2px 2px 0; border-radius: 0 0 4px 0; }
}

.barcode-img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}

// ─── Loading ─────────────────────────────────────────────────

.orders-loading {
  text-align: center;
  padding: 60px 20px;
  color: white;
  p { margin-top: 16px; font-size: 14px; }
}
</style>