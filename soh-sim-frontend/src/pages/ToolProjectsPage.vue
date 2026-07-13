<template>
  <AppPage :title-key="'versionManager.title'" :desc-key="'versionManager.desc'">

    <!-- 视图切换 -->
    <div class="view-tabs">
      <button
        :class="['tab-btn', { active: view === 'projects' }]"
        @click="view = 'projects'"
      >
        📁 {{ $t('versionManager.projects') }}
      </button>
      <button
        :class="['tab-btn', { active: view === 'versions' }]"
        :disabled="!selectedProject"
        @click="view = 'versions'"
      >
        📋 {{ $t('versionManager.versions') }}
      </button>
      <button
        :class="['tab-btn', { active: view === 'compare' }]"
        :disabled="compareIds.length < 2"
        @click="view = 'compare'"
      >
        🔄 {{ $t('versionManager.compare') }}
      </button>
    </div>

    <!-- 项目列表视图 -->
    <div v-if="view === 'projects'" class="view-content">
      <div v-if="loading" class="loading">{{ $t('common.loading') }}</div>
      <div v-else-if="projects.length === 0" class="empty-state">
        <span class="empty-icon">📁</span>
        <p>{{ $t('versionManager.noProjects') }}</p>
      </div>
      <div v-else class="project-cards">
        <div
          v-for="p in projects"
          :key="p.id"
          :class="['project-card', { selected: selectedProject?.id === p.id }]"
          @click="selectProject(p)"
        >
          <div class="card-header">
            <span class="project-name">{{ p.name || p.code || p.id }}</span>
            <span class="project-status" :class="'status-' + (p.status || 'draft')">
              {{ p.status || 'draft' }}
            </span>
          </div>
          <div class="card-body">
            <div class="card-row">
              <span class="label">{{ $t('versionManager.stage') }}</span>
              <span class="value">{{ p.stage || '—' }}</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('versionManager.updated') }}</span>
              <span class="value">{{ fmtDate(p.updated_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 版本列表视图 -->
    <div v-if="view === 'versions' && selectedProject" class="view-content">
      <div class="version-toolbar">
        <span class="project-label">
          {{ $t('versionManager.project') }}: <strong>{{ selectedProject.name || selectedProject.id }}</strong>
        </span>
      </div>

      <div v-if="loadingVersions" class="loading">{{ $t('common.loading') }}</div>
      <div v-else-if="versions.length === 0" class="empty-state">
        <span class="empty-icon">📋</span>
        <p>{{ $t('versionManager.noVersions') }}</p>
      </div>
      <div v-else class="version-list">
        <div
          v-for="v in versions"
          :key="v.id"
          class="version-row"
        >
          <div class="version-info">
            <span class="version-num">v{{ v.version_num }}</span>
            <span class="version-name">{{ v.name }}</span>
            <span v-if="v.is_active" class="active-badge">{{ $t('versionManager.active') }}</span>
          </div>
          <div class="version-desc">{{ v.description }}</div>
          <div class="version-meta">
            <span>{{ fmtDate(v.created_at) }}</span>
            <span class="status-tag" :class="'status-' + (v.status || 'draft')">{{ v.status }}</span>
          </div>
          <div class="version-actions">
            <label class="compare-check">
              <input
                type="checkbox"
                :value="v.id"
                :checked="compareIds.includes(v.id)"
                @change="toggleCompare(v.id)"
              />
              {{ $t('versionManager.selectCompare') }}
            </label>
            <button class="btn btn-sm" @click="restoreVersion(v.id)">
              {{ $t('versionManager.restore') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 版本对比视图 -->
    <div v-if="view === 'compare'" class="view-content">
      <VersionCompare :compare-result="compareResult" />
    </div>
  </AppPage>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppPage from '../components/AppPage.vue'
import { get, post } from '../services/api.js'
import { useBessStore } from '../stores/bess.js'
import VersionCompare from '../components/VersionCompare.vue'

const router = useRouter()
const store = useBessStore()

const view = ref('projects')
const projects = ref([])
const versions = ref([])
const selectedProject = ref(null)
const loading = ref(false)
const loadingVersions = ref(false)
const compareIds = ref([])
const compareResult = ref(null)

function fmtDate(d) {
  if (!d) return '—'
  try { return new Date(d).toLocaleDateString('zh-CN') } catch { return d }
}

onMounted(async () => {
  loading.value = true
  try {
    const resp = await get('/api/projects')
    if (resp.success) {
      projects.value = resp.data || []
    }
  } catch (e) {
    console.error('加载项目列表失败:', e)
  } finally {
    loading.value = false
  }
})

async function selectProject(project) {
  selectedProject.value = project
  compareIds.value = []
  compareResult.value = null
  view.value = 'versions'

  loadingVersions.value = true
  try {
    const resp = await get(`/api/projects/${project.id}`)
    if (resp.success) {
      versions.value = resp.data?.versions || []
    }
  } catch (e) {
    console.error('加载版本列表失败:', e)
  } finally {
    loadingVersions.value = false
  }
}

function toggleCompare(id) {
  const idx = compareIds.value.indexOf(id)
  if (idx >= 0) {
    compareIds.value.splice(idx, 1)
  } else if (compareIds.value.length < 2) {
    compareIds.value.push(id)
  } else {
    // 替换最早的选择
    compareIds.value.shift()
    compareIds.value.push(id)
  }
}

async function restoreVersion(versionId) {
  try {
    const resp = await post(`/api/versions/${versionId}/restore`)
    if (resp.success) {
      // 恢复到 Pinia store
      const data = resp.data
      if (data.design) {
        store.selectedProducts = {
          cell: data.design.container?.cellModel || null,
          container: data.design.container?.model || null,
          pcs: data.design.pcs?.model || null
        }
        store.systemParams = {
          ...store.systemParams,
          ratedEnergy: data.design.container?.ratedEnergyMwh || store.systemParams.ratedEnergy,
          initContainerQty: data.design.containerQty || store.systemParams.initContainerQty,
          initPcsQty: data.design.pcsQty || store.systemParams.initPcsQty,
          pcsPower: data.design.pcs?.ratedPowerMW || store.systemParams.pcsPower,
        }
      }
      if (data.simulation) {
        store.results = {
          initGross: data.simulation.initGross || [],
          initAux: data.simulation.initAux || [],
          initAcUsable: data.simulation.initAcUsable || [],
          augGross: data.simulation.augGross || [],
          augAux: data.simulation.augAux || [],
          augAcUsable: data.simulation.augAcUsable || [],
          augAccumQty: data.simulation.augAccumQty || [],
          totalAcUsable: data.simulation.totalAcUsable || [],
          meetsReq: data.simulation.meetsReq || []
        }
        store.degradation.soh = data.simulation.soh || []
        store.degradation.rte = data.simulation.rte || []
        store.degradation.dod = data.simulation.dod || []
      }
      if (data.financial?.metrics) {
        const m = data.financial.metrics
        store.financial.metrics = {
          projectIrr: m.projectIrr || m.irr || 0,
          equityIrr: m.equityIrr || 0,
          npv: m.npv || 0,
          lcos: m.lcos || m.lcoe || 0,
          dscr: m.dscr || { min: 0, avg: 0 },
          payback: m.payback || -1,
          roi: m.roi || 0
        }
      }
      // 跳转到一键方案页面
      router.push('/orchestrator')
    }
  } catch (e) {
    console.error('版本回溯失败:', e)
  }
}

// 监听 compareIds 变化，自动执行对比
import { watch } from 'vue'
watch(compareIds, async (ids) => {
  if (ids.length >= 2) {
    try {
      const resp = await post('/api/versions/compare', { version_ids: ids })
      if (resp.success) {
        compareResult.value = resp.data
      }
    } catch (e) {
      console.error('版本对比失败:', e)
    }
  } else {
    compareResult.value = null
  }
})
</script>

<style scoped>
.view-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 6px;
  background: var(--input-bg, #f9f9f9);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.tab-btn.active {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border-color: var(--color-accent);
}

.tab-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.view-content {
  background: var(--card-bg, #fff);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary, #888);
}

.empty-icon { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }

.project-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 0.75rem;
}

.project-card {
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 8px;
  padding: 0.75rem;
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.project-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.project-card.selected { border-color: var(--primary, #3b82f6); }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.project-name { font-weight: 600; font-size: 0.95rem; }
.project-status {
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  text-transform: uppercase;
}

.status-active { background: var(--color-success-glow); color: var(--color-success); }
.status-draft { background: var(--color-card-dark); color: var(--color-text-secondary); }
.status-archived { background: var(--color-warning-glow); color: var(--color-warning); }

.card-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  padding: 0.15rem 0;
}

.card-row .label { color: var(--text-secondary, #888); }
.card-row .value { font-weight: 500; }

/* Version List */
.version-toolbar {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-light, #f3f4f6);
}

.version-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.version-row {
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 8px;
  padding: 0.75rem;
}

.version-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.version-num {
  font-weight: 700;
  color: var(--primary, #3b82f6);
  font-size: 0.9rem;
}

.version-name { font-weight: 500; }

.active-badge {
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  background: var(--color-success-glow);
  color: var(--color-success);
  border-radius: 4px;
}

.version-desc {
  font-size: 0.8rem;
  color: var(--text-secondary, #888);
  margin-bottom: 0.35rem;
}

.version-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: var(--text-secondary, #888);
  margin-bottom: 0.5rem;
}

.status-tag {
  padding: 0.05rem 0.3rem;
  border-radius: 3px;
}

.version-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.compare-check {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
}

.btn {
  padding: 0.4rem 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
}

.btn-sm {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}

.btn-sm:hover { background: var(--primary-dark, #2563eb); }
</style>
