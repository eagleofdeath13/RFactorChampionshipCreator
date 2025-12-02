import axios from 'axios'

// API base URL - uses Vite proxy in development
const API_BASE_URL = import.meta.env.PROD ? '/api' : '/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    throw new Error(message)
  }
)

// API endpoints
export const apiEndpoints = {
  // Talents
  talents: {
    list: () => api.get('/talents/'),
    get: (name) => api.get(`/talents/${encodeURIComponent(name)}`),
    create: (data) => api.post('/talents/', data),
    update: (name, data) => api.put(`/talents/${encodeURIComponent(name)}`, data),
    delete: (name) => api.delete(`/talents/${encodeURIComponent(name)}`),
  },

  // Championships
  championships: {
    list: () => api.get('/championships/'),
    get: (name) => api.get(`/championships/${encodeURIComponent(name)}`),
    getRfm: (name) => api.get(`/championships/rfm/${encodeURIComponent(name)}`),
    listCustom: () => api.get('/championships/custom'),
    createCustom: (data) => api.post('/championships/custom', data),
    deleteCustom: (name) => api.delete(`/championships/custom/${encodeURIComponent(name)}`),
  },

  // Vehicles
  vehicles: {
    list: () => api.get('/vehicles/'),
    get: (path) => api.get(`/vehicles/${encodeURIComponent(path)}`),
    update: (path, data) => api.put(`/vehicles/${encodeURIComponent(path)}`, data),
  },

  // Tracks
  tracks: {
    list: () => api.get('/tracks/'),
    get: (path) => api.get(`/tracks/${encodeURIComponent(path)}`),
  },

  // Config
  config: {
    get: () => api.get('/config/'),
    update: (data) => api.post('/config/', data),
  },

  // Import/Export
  import: {
    talents: (file) => {
      const formData = new FormData()
      formData.append('file', file)
      return api.post('/import/talents', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    },
    template: () => api.get('/template/talents', { responseType: 'blob' }),
  },
}

export default api
