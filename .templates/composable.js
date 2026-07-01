import { ref, onMounted, onUnmounted } from 'vue'

export function useComposable() {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchData() {
    loading.value = true
    error.value = null
    try {
      const resp = await fetch('/api/endpoint')
      const result = await resp.json()
      if (result.success) {
        data.value = result.data
      } else {
        error.value = result.error
      }
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    fetchData()
  })

  return {
    data,
    loading,
    error,
    fetchData,
  }
}
