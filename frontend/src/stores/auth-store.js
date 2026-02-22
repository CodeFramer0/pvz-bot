import { defineStore } from 'pinia'
import api from 'src/api/client' // Убедись, что путь верный

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    // === ЛОГИН ===
    async login(email, password) {
      try {
        // Наш Backend ждет email в поле username
        const data = await api.post('/auth/login/', {
          username: email,
          password: password
        })

        // Если бэкенд сразу вернул токены (success)
        if (data.access) {
          this.setTokens(data.access, data.refresh)
          // После логина сразу тянем инфо о юзере
          await this.getMe()
          return { status: 'success' }
        }

        // Если твой бэкенд настроен на 2FA/подтверждение
        if (data.verification_needed) {
          return {
            status: 'verification_needed',
            user_id: data.user_id,
            email: data.email,
            message: data.detail
          }
        }
      } catch (error) {
        console.warn(error)
        throw error // ApiClient уже распарсил ошибку в error.data
      }
    },

    // === ОБНОВЛЕНИЕ ТОКЕНА (вызывается из ApiClient) ===
    async refreshAccessToken() {
      try {
        if (!this.refreshToken) throw new Error('No refresh token')

        const data = await api.post('/auth/refresh/', {
          refresh: this.refreshToken
        })

        this.accessToken = data.access
        localStorage.setItem('access_token', data.access)
        
        // Если бэкенд при рефреше выдает и новый refresh (ROTATE_REFRESH_TOKENS = True)
        if (data.refresh) {
          this.refreshToken = data.refresh
          localStorage.setItem('refresh_token', data.refresh)
        }

        return data.access
      } catch (error) {
        this.logout()
        throw error
      }
    },

    // === ПОЛУЧЕНИЕ ПРОФИЛЯ ===
    async getMe() {
      if (this.user) return this.user
      try {
        const userData = await api.get('/users/me/')
        this.user = userData
        localStorage.setItem('user', JSON.stringify(userData))
      } catch (error) {
        console.error('Failed to fetch profile', error)
      }
    },

    // === УСТАНОВКА ТОКЕНОВ ===
    setTokens(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
    },

    // === ВЫХОД ===
    async logout() {
      // 1. МГНОВЕННО очищаем локальные данные (чтобы юзер сразу увидел страницу логина)
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')

      // 2. Уведомляем бэкенд БЕЗ использования ApiClient.request (чтобы избежать перехватчиков 401)
  
    }
  }
})
