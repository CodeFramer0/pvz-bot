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
    const url = `${API_BASE_URL}${endpoint}`

    const headers = { ...options.headers }
    if (authStore.accessToken) {
      headers['Authorization'] = `Bearer ${authStore.accessToken}`
    }

    try {
      let response = await fetch(url, { ...options, headers })

      // Обработка 401 + refresh
      if (response.status === 401 && authStore.refreshToken && !endpoint.includes('/auth/') &&  !endpoint.includes('/auth/logout/')) {
        if (!this.isRefreshing) {
          this.isRefreshing = true
          try {
            const newToken = await authStore.refreshAccessToken()
            this.isRefreshing = false
            this.processQueue(null, newToken)

            headers['Authorization'] = `Bearer ${newToken}`
            response = await fetch(url, { ...options, headers })
          } catch (error) {
            this.processQueue(error, null)
            this.isRefreshing = false
            authStore.logout()
            window.location.href = '/login'
            throw error
          }
        } else {
          return new Promise((resolve, reject) => {
            this.failedQueue.push({ resolve, reject })
          }).then(token => {
            headers['Authorization'] = `Bearer ${token}`
            return fetch(url, { ...options, headers })
          })
        }
      }

      if (response.status === 204) return null
      
      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        const error = new Error(data.detail || `HTTP ${response.status}`)
        error.status = response.status
        error.data = data 
        throw error
      }

      return data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
  }

  async patch(endpoint, data) {
    return this.request(endpoint, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
  }

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }

  // ✅ POST для создания (Multipart/FormData)
  async postMultipart(endpoint, formData) {
    return this.request(endpoint, {
      method: 'POST',
      body: formData
    })
  }

  // ✅ PATCH для частичного обновления файлов (Multipart/FormData)
  async patchMultipart(endpoint, formData) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: formData
    })
  }
}

export default new ApiClient()
