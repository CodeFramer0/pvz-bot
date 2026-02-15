import { useAuthStore } from 'src/stores/auth-store'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

class ApiClient {
  constructor() {
    this.isRefreshing = false
    this.failedQueue = []
  }

  processQueue(error, token = null) {
    this.failedQueue.forEach(prom => {
      if (error) prom.reject(error)
      else prom.resolve(token)
    })
    this.failedQueue = []
  }

  async request(endpoint, options = {}) {
    const authStore = useAuthStore()

    const headers = {
      ...options.headers
    }

    // Добавляем токен, если есть
    if (authStore.accessToken) {
      headers['Authorization'] = `Bearer ${authStore.accessToken}`
    }

    try {
      let response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
      })

      // Обработка 401 + refresh
      if (response.status === 401 && authStore.refreshToken) {
        if (!this.isRefreshing) {
          this.isRefreshing = true
          try {
            await authStore.refreshAccessToken()
            this.isRefreshing = false
            this.processQueue(null, authStore.accessToken)

            headers['Authorization'] = `Bearer ${authStore.accessToken}`
            response = await fetch(`${API_BASE_URL}${endpoint}`, {
              ...options,
              headers
            })
          } catch (error) {
            this.processQueue(error, null)
            authStore.logout()
            window.location.href = '/login'
            throw error
          }
        } else {
          return new Promise((resolve, reject) => {
            this.failedQueue.push({ resolve, reject })
          }).then(token => {
            headers['Authorization'] = `Bearer ${token}`
            return fetch(`${API_BASE_URL}${endpoint}`, {
              ...options,
              headers
            })
          })
        }
      }

      if (!response.ok && response.status !== 401) {
        throw new Error(`HTTP ${response.status}`)
      }

      return response
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'GET' })
  }

  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...options.headers },
      body: JSON.stringify(data)
    })
  }

  async put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...options.headers },
      body: JSON.stringify(data)
    })
  }

  async delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'DELETE' })
  }

  // ✅ Новый postMultipart
  async postMultipart(endpoint, formData, options = {}) {
    const authStore = useAuthStore()
    const headers = { ...options.headers } // не ставим Content-Type!
    if (authStore.accessToken) headers['Authorization'] = `Bearer ${authStore.accessToken}`

    return this.request(endpoint, {
      ...options,
      method: 'POST',
      body: formData,
      headers
    })
  }
}

export default new ApiClient()
