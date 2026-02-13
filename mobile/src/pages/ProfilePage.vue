<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()


onMounted(async () => {
  await authStore.getMe()
})

const onLogout = () => {
  $q.dialog({
    title: 'Выход',
    message: 'Вы уверены, что хотите выйти?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    authStore.logout()
    router.push('/login')
  })
}
const onLinkTelegram = () => {
  $q.notify({
    color: 'info',
    message: 'Откройте бота для привязки Telegram',
    position: 'top'
  })
}

const onUnlinkTelegram = () => {
  $q.dialog({
    title: 'Отвязать Telegram',
    message: 'Вы уверены, что хотите отвязать Telegram аккаунт?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    $q.notify({
      color: 'positive',
      message: 'Telegram отвязан',
      position: 'top'
    })
  })
}
</script>

<template>
  <div class="profile-page q-pa-md">
    <div class="profile-container">
      <!-- Header -->
      <div class="profile-header">
        <q-btn
          flat
          dense
          round
          icon="arrow_back"
          color="primary"
          @click="$router.back()"
          class="q-mr-md"
        />
        <h4 class="q-my-none">Мой профиль</h4>
      </div>

      <!-- Profile Card -->
      <div class="profile-card q-mt-lg">
        <div class="avatar-section">
          <div class="avatar">
            {{ authStore.user?.username?.charAt(0).toUpperCase() }}
          </div>
        </div>

        <div class="profile-info q-mt-lg q-gutter-md">
          <div class="info-item">
            <span class="label">👤 Имя пользователя</span>
            <span class="value">{{ authStore.user?.username }}</span>
          </div>

          <div class="info-item">
            <span class="label">📧 Email</span>
            <span class="value">{{ authStore.user?.email }}</span>
            <q-icon
              v-if="authStore.user?.email"
              name="verified"
              color="positive"
              size="xs"
              class="q-ml-sm"
            />
          </div>

          <div class="divider q-my-md"></div>

          <!-- Telegram Section -->
          <div class="section-title q-mt-lg">
            <q-icon name="send" color="info" class="q-mr-sm" />
            <span>Telegram</span>
          </div>

          <div class="telegram-section">
            <div
              v-if="authStore.isTelegramLinked"
              class="linked-telegram q-pa-md"
            >
              <div class="q-d-flex q-align-center q-gutter-md">
                <div class="telegram-avatar">✈️</div>
                <div class="flex-grow">
                  <p class="q-my-none text-weight-bold">
                    {{ authStore.user?.telegram_user?.nick_name }}
                  </p>
                  <p class="q-my-none text-caption text-grey-7">
                    @{{ authStore.user?.telegram_user?.nick_name }}
                  </p>
                </div>
                <q-btn
                  flat
                  dense
                  icon="delete_outline"
                  color="negative"
                  size="sm"
                  @click="onUnlinkTelegram"
                />
              </div>
            </div>

            <div v-else class="not-linked q-pa-md">
              <p class="q-my-none text-grey-7 text-center">
                Telegram не привязан
              </p>
              <q-btn
                label="Привязать Telegram"
                color="info"
                class="full-width q-mt-md"
                unelevated
                rounded
                icon="send"
                @click="onLinkTelegram"
              />
            </div>
          </div>

          <div class="divider q-my-md"></div>

          <!-- Statistics -->
          <div class="section-title q-mt-lg">
            <q-icon name="bar_chart" color="primary" class="q-mr-sm" />
            <span>Статистика</span>
          </div>

          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-value">12</div>
              <div class="stat-label">Заказов</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">8</div>
              <div class="stat-label">Выполнено</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">4</div>
              <div class="stat-label">В процессе</div>
            </div>
          </div>

          <div class="divider q-my-md"></div>

          <!-- Actions -->
          <div class="actions q-gutter-md q-mt-lg">
            <q-btn
              label="Изменить пароль"
              outline
              color="primary"
              class="full-width"
              rounded
              icon="security"
            />
            <q-btn
              label="Выход"
              outline
              color="negative"
              class="full-width"
              rounded
              icon="logout"
              @click="onLogout"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  min-height: 100vh;
}

.profile-container {
  max-width: 500px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-header h4 {
  margin: 0;
  color: #333;
  font-weight: 600;
}

.profile-card {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.avatar-section {
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: white;
  font-weight: bold;
  margin: 0 auto;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.profile-info {
  margin-top: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item .label {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.info-item .value {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.divider {
  height: 1px;
  background: #eee;
}

.section-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #333;
  font-size: 16px;
}

.telegram-section {
  margin-top: 15px;
}

.linked-telegram {
  background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
  border: 1px solid #667eea30;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.telegram-avatar {
  font-size: 32px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
}

.not-linked {
  background: #f5f5f5;
  border-radius: 12px;
  border: 1px dashed #ddd;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 15px;
  margin-top: 15px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
  border: 1px solid #667eea30;
  border-radius: 12px;
  padding: 15px;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  text-transform: uppercase;
}

.actions {
  margin-top: 20px;
}

@media (max-width: 600px) {
  .profile-card {
    padding: 20px;
  }

  .avatar {
    width: 80px;
    height: 80px;
    font-size: 32px;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>