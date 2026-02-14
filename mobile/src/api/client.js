import { useAuthStore } from 'src/stores/auth-store'

const API_BASE_URL = 'http://pvz.localhost/api/v1/'

class ApiClient {
  constructor() {
    this.isRefreshing = false
    this.failedQueue = []
  }

  processQueue(error, token = null) {
    this.failedQueue.forEach(prom => {
      if (error) {
        prom.reject(error)
      } else {
        prom.resolve(token)
      }
    })
    this.failedQueue = []
  }

  async request(endpoint, options = {}) {
    const authStore = useAuthStore()

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    if (authStore.accessToken) {
      headers['Authorization'] = `Bearer ${authStore.accessToken}`
    }

    try {
      let response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
      })

      // Если 401 и есть refresh token - пытаемся обновить
      if (response.status === 401 && authStore.refreshToken) {
        if (!this.isRefreshing) {
          this.isRefreshing = true

          try {
            await authStore.refreshAccessToken()
            this.isRefreshing = false
            this.processQueue(null, authStore.accessToken)

            // Повторяем запрос с новым токеном
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
          // Ждем пока другой запрос обновит токен
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
      body: JSON.stringify(data)
    })
  }

  async put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'DELETE' })
  }
}

export default new ApiClient()