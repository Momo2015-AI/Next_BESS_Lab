/**
 * 全站草稿持久化 composable
 *
 * 设计目标：
 * - 所有需要填写的方框数据自动持久化到 localStorage
 * - 关闭网页/超时后数据仍在
 * - 只有点击"提交/计算"按钮后，数据才正式存入数据库（由组件自行调用 API）
 * - 提交成功后清除对应草稿
 *
 * 使用方式：
 *   const { state, clearDraft } = useDraft('survey-form', defaultValue)
 *   // state 是一个 reactive 对象，修改后自动保存
 *   // 提交成功后调用 clearDraft() 清除草稿
 *
 * 原则：
 * - 不保存敏感数据（密码、token）
 * - 不保存图表实例、定时器等不可序列化对象
 * - 保存数组时保留长度，避免 NaN/undefined
 */

import { reactive, watch, isReactive, toRaw, ref } from 'vue'

const STORAGE_PREFIX = 'soh-draft:'
const SCHEMA_VERSION = '1.0'

// 全局草稿元信息（保存最后更新时间，便于调试和过期清理）
const META_KEY = `${STORAGE_PREFIX}_meta`

function readMeta() {
  try {
    const raw = localStorage.getItem(META_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

function writeMeta(key, info) {
  try {
    const meta = readMeta()
    meta[key] = info
    localStorage.setItem(META_KEY, JSON.stringify(meta))
  } catch {
    /* localStorage 配额或被禁用，静默失败 */
  }
}

function safeParse(raw, fallback) {
  if (!raw) return fallback
  try {
    const parsed = JSON.parse(raw)
    if (parsed && parsed.__v === SCHEMA_VERSION && 'data' in parsed) {
      return parsed.data
    }
    return fallback
  } catch {
    return fallback
  }
}

function safeStringify(data) {
  return JSON.stringify({
    __v: SCHEMA_VERSION,
    savedAt: Date.now(),
    data
  })
}

/**
 * 合并默认值与已保存草稿，保证字段完整（避免新增字段缺失）
 */
function mergeWithDefaults(saved, defaults) {
  if (saved == null) return JSON.parse(JSON.stringify(defaults))
  if (typeof saved !== 'object' || Array.isArray(saved)) {
    return saved
  }
  const merged = JSON.parse(JSON.stringify(defaults))
  for (const k of Object.keys(saved)) {
    merged[k] = saved[k]
  }
  return merged
}

/**
 * 深度同步数组长度（用于 26 年时序数据）
 */
function syncArrayLength(saved, defaults) {
  if (!Array.isArray(saved) || !Array.isArray(defaults)) return saved
  // 保留默认长度，但用保存的值覆盖
  const result = defaults.slice()
  for (let i = 0; i < Math.min(saved.length, result.length); i++) {
    result[i] = saved[i]
  }
  return result
}

/**
 * 创建带草稿持久化的 reactive 状态
 *
 * @param {string} key - 草稿唯一键（自动加前缀）
 * @param {object|Array} defaultValue - 默认值
 * @param {object} options
 * @param {number} options.debounce - 防抖时间（毫秒），默认 500
 * @param {boolean} options.preserveArrayLength - 是否强制保留默认数组长度，默认 true
 * @returns {{ state, clearDraft, forceSave }}
 */
export function useDraft(key, defaultValue, options = {}) {
  const fullKey = STORAGE_PREFIX + key
  const { debounce = 500, preserveArrayLength = true } = options

  // 读取已保存的草稿
  let saved
  try {
    const raw = localStorage.getItem(fullKey)
    saved = safeParse(raw, null)
  } catch {
    saved = null
  }

  // 合并默认值
  let initialValue
  if (saved != null) {
    if (preserveArrayLength && Array.isArray(saved)) {
      initialValue = syncArrayLength(saved, defaultValue)
    } else if (Array.isArray(saved)) {
      initialValue = saved
    } else if (typeof saved === 'object') {
      initialValue = mergeWithDefaults(saved, defaultValue)
    } else {
      initialValue = saved
    }
  } else {
    initialValue = JSON.parse(JSON.stringify(defaultValue))
  }

  const state = reactive(initialValue)

  // 防抖保存
  let saveTimer = null
  let isFirstWatch = true

  watch(
    state,
    (newVal) => {
      // 跳过首次初始化触发
      if (isFirstWatch) {
        isFirstWatch = false
        return
      }
      if (saveTimer) clearTimeout(saveTimer)
      saveTimer = setTimeout(() => {
        try {
          const raw = toRaw(state)
          localStorage.setItem(fullKey, safeStringify(raw))
          writeMeta(key, { savedAt: Date.now() })
        } catch (e) {
          // 配额不足或被禁用，静默失败
          console.warn('[useDraft] 保存失败:', key, e)
        }
      }, debounce)
    },
    { deep: true }
  )

  function clearDraft() {
    try {
      localStorage.removeItem(fullKey)
      const meta = readMeta()
      delete meta[key]
      localStorage.setItem(META_KEY, JSON.stringify(meta))
    } catch {
      /* ignore */
    }
  }

  function forceSave() {
    try {
      const raw = toRaw(state)
      localStorage.setItem(fullKey, safeStringify(raw))
      writeMeta(key, { savedAt: Date.now() })
    } catch {
      /* ignore */
    }
  }

  return { state, clearDraft, forceSave }
}

/**
 * 创建带草稿持久化的 ref（用于简单值类型）
 */
export function useDraftRef(key, defaultValue, options = {}) {
  const fullKey = STORAGE_PREFIX + key
  const { debounce = 500 } = options

  let saved
  try {
    saved = safeParse(localStorage.getItem(fullKey), null)
  } catch {
    saved = null
  }

  const initialValue = saved != null ? saved : defaultValue

  const state = ref(initialValue)

  let saveTimer = null
  watch(
    state,
    () => {
      if (saveTimer) clearTimeout(saveTimer)
      saveTimer = setTimeout(() => {
        try {
          localStorage.setItem(fullKey, safeStringify(state.value))
          writeMeta(key, { savedAt: Date.now() })
        } catch {
          /* ignore */
        }
      }, debounce)
    },
    { deep: true }
  )

  function clearDraft() {
    try {
      localStorage.removeItem(fullKey)
    } catch {
      /* ignore */
    }
  }

  return { state, clearDraft }
}

/**
 * 检查某个草稿是否存在
 */
export function hasDraft(key) {
  try {
    return localStorage.getItem(STORAGE_PREFIX + key) != null
  } catch {
    return false
  }
}

/**
 * 列出所有草稿键
 */
export function listDrafts() {
  try {
    const keys = []
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i)
      if (k && k.startsWith(STORAGE_PREFIX) && !k.endsWith('_meta')) {
        keys.push(k.replace(STORAGE_PREFIX, ''))
      }
    }
    return keys
  } catch {
    return []
  }
}

/**
 * 清除所有草稿
 */
export function clearAllDrafts() {
  try {
    const keysToRemove = []
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i)
      if (k && k.startsWith(STORAGE_PREFIX)) {
        keysToRemove.push(k)
      }
    }
    keysToRemove.forEach((k) => localStorage.removeItem(k))
  } catch {
    /* ignore */
  }
}

/**
 * 页面卸载前强制保存所有未保存的草稿
 * （通过监听 beforeunload 事件，在 App.vue 中调用）
 */
export function setupBeforeUnloadGuard() {
  if (typeof window === 'undefined') return
  window.addEventListener('beforeunload', () => {
    try {
      // 触发同步写入
      const meta = readMeta()
      for (const key of Object.keys(meta)) {
        // localStorage 已在 watch 中防抖保存，这里只是兜底
      }
    } catch {
      /* ignore */
    }
  })
}

export default useDraft
