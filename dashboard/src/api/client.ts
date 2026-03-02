import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const fetchStats = async () => {
  const { data } = await api.get('/stats')
  return data
}

export const fetchPipelines = async () => {
  const { data } = await api.get('/pipelines')
  return data
}

export const fetchFailures = async () => {
  const { data } = await api.get('/failures')
  return data
}

export const fetchFixes = async () => {
  const { data } = await api.get('/fixes')
  return data
}
