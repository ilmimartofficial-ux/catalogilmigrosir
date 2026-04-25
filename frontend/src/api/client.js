import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
})

// Products
export const getProducts = (params) => api.get('/api/products', { params })
export const getCategories = () => api.get('/api/products/categories')
export const getStats = () => api.get('/api/products/stats')

// Chat
export const sendChat = (message, history) =>
  api.post('/api/chat', { message, history })

// Admin
export const adminLogin = (password) =>
  api.post('/api/admin/login', { password })

export const uploadExcel = (file, token) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/api/admin/upload', form, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`
    }
  })
}

export const getHistory = (token) =>
  api.get('/api/admin/history', {
    headers: { Authorization: `Bearer ${token}` }
  })

export default api
