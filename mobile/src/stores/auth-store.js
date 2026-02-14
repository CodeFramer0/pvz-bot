import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  // --- Email verification flow ---
  const verificationNeeded = ref(false)
  const verificationEmail = ref('')

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
      const res = await fetch('http://pvz.localhost/api/v1/auth/refresh_token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken.value })
      })
      if (!res.ok) throw new Error('Refresh failed')
      const data = await res.json()
      setTokens(data.access, data.refresh)
      return true
    } catch {
      logout()
      return false
    }
  }

  // --- Login ---
const login = async (email, password) => {
  try {
    const response = await fetch('http://pvz.localhost/api/v1/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    const data = await response.json()
    return data  // возвращаем объект полностью
  } catch (error) {
    console.error(error)
    return { status: 'error', error: 'Ошибка запроса' }
  }
}

  // --- Register ---
  const register = async (username, email, password, telegramUserId = null) => {
    try {
      const res = await fetch('http://pvz.localhost/api/v1/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, telegram_user_id: telegramUserId })
      })
      const data = await res.json()
      if (res.ok) {
        verificationNeeded.value = true
        verificationEmail.value = email
        return data
      } else {
        throw new Error(data.error || 'Ошибка регистрации')
      }
    } catch (err) {
      console.error(err)
      throw err
    }
  }

  // --- Verify Email ---
  const verifyEmail = async (userId, code) => {
    try {
      const res = await fetch('http://pvz.localhost/api/v1/auth/verify_email/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, code })
      })
      if (!res.ok) return false
      const data = await res.json()
      setTokens(data.access, data.refresh)
      user.value = data.user
      verificationNeeded.value = false
      verificationEmail.value = ''
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  }

  // --- Resend code ---
  const resendCode = async () => {
    if (!verificationEmail.value) return false
    try {
      const res = await fetch('http://pvz.localhost/api/v1/auth/resend_code/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: verificationEmail.value })
      })
      return res.ok
    } catch (err) {
      console.error(err)
      return false
    }
  }

  // --- Telegram login ---
  const telegramLogin = async (telegramUserId) => {
    try {
      const res = await fetch('http://pvz.localhost/api/v1/auth/telegram_login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ telegram_user_id: telegramUserId })
      })
      if (!res.ok) return false
      const data = await res.json()
      setTokens(data.access, data.refresh)
      user.value = data.user
      verificationNeeded.value = false
      verificationEmail.value = ''
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  }

  // --- Link Telegram ---
  const linkTelegram = async (telegramUserId) => {
    try {
      const res = await fetch('http://pvz.localhost/api/v1/auth/link_telegram/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: JSON.stringify({ telegram_user_id: telegramUserId })
      })
      if (!res.ok) return false
      const data = await res.json()
      user.value.telegram_user = data.telegram_user
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    verificationNeeded.value = false
    verificationEmail.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const getMe = async () => {
    if (!accessToken.value) return false
    try {
      const res = await fetch('http://pvz.localhost/api/v1/auth/me/', {
        headers: { 'Authorization': `Bearer ${accessToken.value}` }
      })
      if (res.ok) {
        user.value = await res.json()
        return true
      } else if (res.status === 401) {
        return await refreshAccessToken()
      } else {
        logout()
        return false
      }
    } catch (err) {
      console.error(err)
      logout()
      return false
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    isTelegramLinked,
    verificationNeeded,
    verificationEmail,
    setTokens,
    refreshAccessToken,
    login,
    register,
    verifyEmail,
    resendCode,
    telegramLogin,
    linkTelegram,
    logout,
    getMe
  }
})
