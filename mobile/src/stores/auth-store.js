import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isTelegramLinked = computed(() => !!user.value?.telegram_user)

  const setTokens = (access, refresh) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value) return false

    try {
      const response = await fetch('/api/v1/auth/refresh_token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken.value })
      })

      if (response.ok) {
        const data = await response.json()
        setTokens(data.access, data.refresh)
        return true
      } else {
        logout()
        return false
      }
    } catch (error) {
      console.error('Refresh token error:', error)
      logout()
      return false
    }
  }

  const register = async (username, email, password, telegramUserId = null) => {
    try {
      const response = await fetch('/api/v1/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          email,
          password,
          telegram_user_id: telegramUserId
        })
      })

      if (response.ok) {
        return await response.json()
      }
      const error = await response.json()
      throw new Error(error.error || 'Ошибка регистрации')
    } catch (error) {
      console.error(error)
      throw error
    }
  }

  const verifyEmail = async (userId, code) => {
    try {
      const response = await fetch('/api/v1/auth/verify_email/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          code
        })
      })

      if (response.ok) {
        const data = await response.json()
        setTokens(data.access, data.refresh)
        user.value = data.user
        return true
      }
      return false
    } catch (error) {
      console.error(error)
      return false
    }
  }

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/v1/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        const data = await response.json()
        setTokens(data.access, data.refresh)
        user.value = data.user
        return true
      }
      return false
    } catch (error) {
      console.error(error)
      return false
    }
  }

  const telegramLogin = async (telegramUserId) => {
    try {
      const response = await fetch('/api/v1/auth/telegram_login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ telegram_user_id: telegramUserId })
      })

      if (response.ok) {
        const data = await response.json()
        setTokens(data.access, data.refresh)
        user.value = data.user
        return true
      }
      return false
    } catch (error) {
      console.error(error)
      return false
    }
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const getMe = async () => {
    if (!accessToken.value) return false

    try {
      const response = await fetch('/api/v1/auth/me/', {
        headers: { 'Authorization': `Bearer ${accessToken.value}` }
      })

      if (response.ok) {
        const data = await response.json()
        user.value = data
        return true
      } else if (response.status === 401) {
        // Токен истек, пытаемся обновить
        return await refreshAccessToken()
      } else {
        logout()
        return false
      }
    } catch (error) {
      console.error(error)
      logout()
      return false
    }
  }

  const linkTelegram = async (telegramUserId) => {
    try {
      const response = await fetch('/api/v1/auth/link_telegram/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: JSON.stringify({ telegram_user_id: telegramUserId })
      })

      if (response.ok) {
        const data = await response.json()
        user.value.telegram_user = data.telegram_user
        return true
      }
      return false
    } catch (error) {
      console.error(error)
      return false
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    isTelegramLinked,
    setTokens,
    refreshAccessToken,
    register,
    verifyEmail,
    login,
    telegramLogin,
    logout,
    getMe,
    linkTelegram
  }
})