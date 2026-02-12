import { defineStore } from 'pinia'

export const useOrderStore = defineStore('orders', {
  state: () => ({
    orders: [],
    loading: false
  }),

  actions: {
    // Получение списка заказов
    async fetchOrders() {
      this.loading = true
      try {
        // Когда будет бэк: const response = await api.get('/orders')
        // Пока делаем заглушку (имитация запроса):
        await new Promise(resolve => setTimeout(resolve, 1000))
        // Если данных нет, оставляем примеры
        if (this.orders.length === 0) {
          this.orders = [
            { id: 1, platform: 'Wildberries', track: '99214450', status: 'В пути', archive: false }
          ]
        }
      } catch (error) {
        console.error('Ошибка загрузки:', error)
      } finally {
        this.loading = false
      }
    },

    // Создание нового заказа
    async addOrder(orderData) {
      this.loading = true
      try {
        // В будущем: const response = await api.post('/orders', orderData)
        // Сейчас просто пушим в массив
        const newOrder = {
          ...orderData,
          id: Date.now(),
          status: 'Принято',
          archive: false
        }
        this.orders.push(newOrder)
        return true
      } catch {
        return false
      } finally {
        this.loading = false
      }
    }
  }
})