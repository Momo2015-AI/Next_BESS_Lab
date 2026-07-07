/**
 * Plotly 渲染组合式函数
 *
 * 后端 /api/report/charts/<type> 返回 Plotly 结构化数据（data/layout/config），
 * 前端通过 Plotly.newPlot 直接渲染到容器，避免 v-html 注入任意 HTML（XSS 风险）。
 *
 * Plotly 运行时从 CDN 懒加载（首次使用时注入 <script>），全局复用。
 */

const PLOTLY_CDN = 'https://cdn.plot.ly/plotly-2.35.2.min.js'
let plotlyPromise = null

/**
 * 懒加载 Plotly 全局对象
 * @returns {Promise<object>} window.Plotly
 */
export function loadPlotly() {
  if (typeof window !== 'undefined' && window.Plotly) {
    return Promise.resolve(window.Plotly)
  }
  if (plotlyPromise) {
    return plotlyPromise
  }
  plotlyPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = PLOTLY_CDN
    script.async = true
    script.onload = () => {
      if (window.Plotly) {
        resolve(window.Plotly)
      } else {
        reject(new Error('Plotly 加载异常'))
      }
    }
    script.onerror = () => reject(new Error('Plotly CDN 加载失败'))
    document.head.appendChild(script)
  })
  return plotlyPromise
}

/**
 * 将图表渲染到指定容器
 * @param {HTMLElement} container 目标 DOM 节点
 * @param {object} chart { data, layout, config }
 * @param {string} divId 容器 id（Plotly 要求唯一）
 */
export async function renderPlotly(container, chart, divId) {
  if (!container || !chart) return
  const Plotly = await loadPlotly()
  container.id = divId
  await Plotly.newPlot(container, chart.data, chart.layout, chart.config)
}

/**
 * 清理 Plotly 实例，防止内存泄漏（应在 onUnmounted 调用）
 * @param {HTMLElement} container
 */
export function purgePlotly(container) {
  if (container && typeof window !== 'undefined' && window.Plotly) {
    try {
      window.Plotly.purge(container)
    } catch (e) {
      // 容器尚未初始化时忽略
    }
  }
}
