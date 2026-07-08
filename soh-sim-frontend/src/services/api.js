/**
 * 统一 API 请求层
 *
 * 封装 fetch，提供：
 * - 自动注入 Authorization token
 * - 统一错误处理（401 跳登录、500 提示）
 * - 统一响应解析（success/data/error/message 契约）
 * - 请求超时控制
 */

const DEFAULT_TIMEOUT = 30000
const BASE_URL = import.meta.env.VITE_API_BASE || ''

/**
 * 获取认证 token
 * @returns {string|null}
 */
// token 统一从 sessionStorage 读取（与 AuthPanel 写入处一致），
// 并缓存到内存，避免每次请求访问存储。
// 注意：sessionStorage 在标签页关闭后即清除，相比 localStorage 降低 XSS 长期窃取风险。
let _memoryToken = null

function getAuthToken() {
  if (_memoryToken) return _memoryToken
  try {
    _memoryToken = sessionStorage.getItem('auth_token')
  } catch (e) {
    _memoryToken = null
  }
  return _memoryToken
}

/**
 * 统一请求方法
 * @param {string} url - 请求地址
 * @param {object} options - fetch options
 * @param {object} config - 额外配置 { timeout, skipAuth, skipErrorToast }
 * @returns {Promise<object>} 解析后的响应数据
 */
async function request(url, options = {}, config = {}) {
  const { timeout = DEFAULT_TIMEOUT, skipAuth = false, skipErrorToast = false } = config

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }

  if (!skipAuth) {
    const token = getAuthToken()
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }
  }

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeout)

  try {
    const resp = await fetch(`${BASE_URL}${url}`, {
      ...options,
      headers,
      signal: controller.signal
    })
    clearTimeout(timer)

    // 非 JSON 响应（如文件下载 blob）
    const contentType = resp.headers.get('content-type') || ''
    if (!contentType.includes('application/json')) {
      if (!resp.ok) {
        throw new ApiError(resp.statusText || '请求失败', resp.status)
      }
      return resp
    }

    const data = await resp.json()

    // 401 未认证 — 清除 token 并跳登录
    if (resp.status === 401) {
      _memoryToken = null
      try {
        sessionStorage.removeItem('auth_token')
        sessionStorage.removeItem('user_info')
      } catch (e) {
        // 忽略存储清理异常
      }
      window.dispatchEvent(new StorageEvent('storage', { key: 'auth_token', newValue: null }))
      if (window.location.pathname !== '/auth' && !skipErrorToast) {
        window.location.href = '/auth'
      }
      throw new ApiError(data.error || data.message || '登录已过期', 401)
    }

    if (!resp.ok || data.success === false) {
      const errMsg = data.error || data.message || `请求失败 (${resp.status})`
      if (!skipErrorToast) {
        console.error('[API Error]', url, errMsg)
      }
      throw new ApiError(errMsg, resp.status, data)
    }

    return data
  } catch (err) {
    clearTimeout(timer)
    if (err.name === 'AbortError') {
      throw new ApiError('请求超时', 408)
    }
    if (err instanceof ApiError) {
      throw err
    }
    // 网络错误
    throw new ApiError(err.message || '网络连接失败', 0)
  }
}

class ApiError extends Error {
  constructor(message, status, raw) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.raw = raw
  }
}

/** GET 请求 */
function get(url, config) {
  return request(url, { method: 'GET' }, config)
}

/** POST 请求 */
function post(url, body, config) {
  return request(url, { method: 'POST', body: JSON.stringify(body) }, config)
}

/** PUT 请求 */
function put(url, body, config) {
  return request(url, { method: 'PUT', body: JSON.stringify(body) }, config)
}

/** DELETE 请求 */
function del(url, config) {
  return request(url, { method: 'DELETE' }, config)
}

/** 文件下载（blob 响应） */
async function download(url, body, config) {
  const resp = await request(url, { method: 'POST', body: JSON.stringify(body || {}) }, { ...config })
  const blob = await resp.blob()
  return blob
}

export { request, get, post, put, del, download, ApiError }
export default { request, get, post, put, del, download, ApiError }
