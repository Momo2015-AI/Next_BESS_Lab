<template>
  <div class="admin-panel">
    <!-- Tab 切换 -->
    <div class="admin-tabs">
      <button
        :class="['admin-tab', { active: activeTab === 'roles' }]"
        @click="activeTab = 'roles'"
      >
        {{ $t('admin.tabRoles') }}
      </button>
      <button
        :class="['admin-tab', { active: activeTab === 'users' }]"
        @click="activeTab = 'users'"
      >
        {{ $t('admin.tabUsers') }}
      </button>
    </div>

    <!-- ==================== 角色权限配置 ==================== -->
    <div v-if="activeTab === 'roles'" class="admin-section">
      <div class="admin-section-header">
        <h2>{{ $t('admin.rolePermissions') }}</h2>
        <p class="admin-section-desc">{{ $t('admin.rolePermissionsDesc') }}</p>
      </div>

      <div v-if="loading" class="admin-loading">{{ $t('admin.loading') }}</div>

      <template v-else>
        <!-- 角色选择器 -->
        <div class="role-selector">
          <label>{{ $t('admin.selectRole') }}</label>
          <select v-model="selectedRole" class="role-select">
            <option v-for="role in roles" :key="role.code" :value="role.code">
              {{ role.label }} ({{ role.label_en }})
            </option>
          </select>
          <span v-if="selectedRoleData" class="role-desc">{{ selectedRoleData.description }}</span>
        </div>

        <!-- 权限矩阵编辑 -->
        <div v-if="selectedRole" class="perm-matrix">
          <table class="perm-table">
            <thead>
              <tr>
                <th>{{ $t('admin.moduleName') }}</th>
                <th>{{ $t('admin.permissionFull') }}</th>
                <th>{{ $t('admin.permissionReadonly') }}</th>
                <th>{{ $t('admin.permissionHidden') }}</th>
                <th>{{ $t('admin.defaultPerm') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="key in permissionKeys" :key="key">
                <td class="perm-label">{{ $t(`admin.modules.${key}`) }}</td>
                <td class="perm-cell">
                  <input
                    type="radio"
                    :name="`perm-${key}`"
                    :value="'full'"
                    v-model="editingPerms[key]"
                  />
                </td>
                <td class="perm-cell">
                  <input
                    type="radio"
                    :name="`perm-${key}`"
                    :value="'readonly'"
                    v-model="editingPerms[key]"
                  />
                </td>
                <td class="perm-cell">
                  <input
                    type="radio"
                    :name="`perm-${key}`"
                    :value="'hidden'"
                    v-model="editingPerms[key]"
                  />
                </td>
                <td class="perm-default">{{ getDefaultPerm(key) }}</td>
              </tr>
            </tbody>
          </table>

          <!-- 失效时间 + 备注 -->
          <div class="override-controls">
            <div class="control-group">
              <label>{{ $t('admin.expiresAt') }}</label>
              <input
                type="datetime-local"
                v-model="expiresAtInput"
                class="control-input"
              />
              <button class="control-clear-btn" @click="expiresAtInput = ''">
                {{ $t('common.clear') }}
              </button>
              <span class="control-hint">{{ $t('admin.expiresHint') }}</span>
            </div>
            <div class="control-group">
              <label>{{ $t('admin.note') }}</label>
              <input
                type="text"
                v-model="noteInput"
                class="control-input"
                :placeholder="$t('admin.notePlaceholder')"
              />
            </div>
            <div class="control-actions">
              <button class="admin-btn primary" @click="saveRolePermissions">
                {{ $t('common.save') }}
              </button>
              <button class="admin-btn danger" @click="resetRolePermissions">
                {{ $t('admin.resetToDefault') }}
              </button>
            </div>
            <div v-if="currentOverride && currentOverride.expires_at" class="override-info">
              <span :class="['override-status', { expired: currentOverride.is_expired }]">
                {{ currentOverride.is_expired ? $t('admin.expired') : $t('admin.expiresAt') }}:
                {{ formatDateTime(currentOverride.expires_at) }}
              </span>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- ==================== 用户权限配置 ==================== -->
    <div v-if="activeTab === 'users'" class="admin-section">
      <div class="admin-section-header">
        <h2>{{ $t('admin.userPermissions') }}</h2>
        <p class="admin-section-desc">{{ $t('admin.userPermissionsDesc') }}</p>
      </div>

      <div v-if="usersLoading" class="admin-loading">{{ $t('admin.loading') }}</div>

      <template v-else>
        <!-- 用户列表 -->
        <div class="user-list">
          <table class="user-table">
            <thead>
              <tr>
                <th>{{ $t('admin.username') }}</th>
                <th>{{ $t('admin.email') }}</th>
                <th>{{ $t('admin.role') }}</th>
                <th>{{ $t('admin.effectiveRole') }}</th>
                <th>{{ $t('admin.overrideStatus') }}</th>
                <th>{{ $t('admin.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ getRoleLabel(user.role) }}</td>
                <td>
                  <span :class="['role-badge', user.effective_role]">
                    {{ getRoleLabel(user.effective_role) }}
                  </span>
                </td>
                <td>
                  <span v-if="user.override && !user.override.is_expired" class="override-active">
                    {{ $t('admin.hasOverride') }}
                    <span v-if="user.override.expires_at">
                      ({{ formatDateTime(user.override.expires_at) }})
                    </span>
                  </span>
                  <span v-else-if="user.override && user.override.is_expired" class="override-expired">
                    {{ $t('admin.expired') }}
                  </span>
                  <span v-else class="override-none">{{ $t('admin.noOverride') }}</span>
                </td>
                <td>
                  <button
                    class="admin-btn small"
                    @click="openUserEditor(user)"
                    :disabled="user.role === 'admin'"
                  >
                    {{ $t('admin.editPermissions') }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 用户权限编辑弹窗 -->
        <div v-if="editingUser" class="modal-overlay" @click.self="closeUserEditor">
          <div class="modal-content">
            <div class="modal-header">
              <h3>{{ $t('admin.editUserPermissions') }} - {{ editingUser.username }}</h3>
              <button class="modal-close" @click="closeUserEditor">&times;</button>
            </div>

            <div class="modal-body">
              <!-- 永久角色更改 -->
              <div class="modal-section">
                <h4>{{ $t('admin.permanentRole') }}</h4>
                <select v-model="editingUserRole" class="role-select">
                  <option v-for="role in roles" :key="role.code" :value="role.code">
                    {{ role.label }} ({{ role.label_en }})
                  </option>
                </select>
                <button class="admin-btn small" @click="saveUserRole">
                  {{ $t('admin.changeRole') }}
                </button>
              </div>

              <div class="modal-divider"></div>

              <!-- 临时角色覆盖 -->
              <div class="modal-section">
                <h4>{{ $t('admin.temporaryOverride') }}</h4>
                <p class="modal-hint">{{ $t('admin.temporaryOverrideDesc') }}</p>
                <div class="control-group">
                  <label>{{ $t('admin.temporaryRole') }}</label>
                  <select v-model="userOverride.temporaryRole" class="role-select">
                    <option :value="null">{{ $t('admin.none') }}</option>
                    <option v-for="role in roles" :key="role.code" :value="role.code">
                      {{ role.label }} ({{ role.label_en }})
                    </option>
                  </select>
                </div>

                <!-- 精确权限覆盖 -->
                <div class="control-group">
                  <label>{{ $t('admin.customPermissions') }}</label>
                  <p class="modal-hint">{{ $t('admin.customPermissionsDesc') }}</p>
                  <div class="perm-matrix compact">
                    <div v-for="key in permissionKeys" :key="key" class="perm-row">
                      <span class="perm-label">{{ $t(`admin.modules.${key}`) }}</span>
                      <select v-model="userOverride.permissions[key]" class="perm-select">
                        <option value="">{{ $t('admin.inherit') }}</option>
                        <option value="full">{{ $t('admin.permissionFull') }}</option>
                        <option value="readonly">{{ $t('admin.permissionReadonly') }}</option>
                        <option value="hidden">{{ $t('admin.permissionHidden') }}</option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- 失效时间 -->
                <div class="control-group">
                  <label>{{ $t('admin.expiresAt') }}</label>
                  <input
                    type="datetime-local"
                    v-model="userOverride.expiresAt"
                    class="control-input"
                  />
                  <button class="control-clear-btn" @click="userOverride.expiresAt = ''">
                    {{ $t('common.clear') }}
                  </button>
                  <span class="control-hint">{{ $t('admin.expiresHint') }}</span>
                </div>

                <!-- 备注 -->
                <div class="control-group">
                  <label>{{ $t('admin.note') }}</label>
                  <input
                    type="text"
                    v-model="userOverride.note"
                    class="control-input"
                    :placeholder="$t('admin.notePlaceholder')"
                  />
                </div>

                <div class="control-actions">
                  <button class="admin-btn primary" @click="saveUserOverride">
                    {{ $t('common.save') }}
                  </button>
                  <button class="admin-btn danger" @click="resetUserOverride">
                    {{ $t('admin.resetOverride') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Toast -->
    <div v-if="toast.show" :class="['admin-toast', `toast-${toast.type}`]">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../services/api.js'

const { t } = useI18n()

const props = defineProps({
  initialTab: { type: String, default: '' }
})

const activeTab = ref(props.initialTab || 'roles')
const loading = ref(false)
const usersLoading = ref(false)

// 角色列表
const roles = ref([])
// 权限模块 key 列表
const permissionKeys = ref([])
// 默认权限映射
const defaultPermissions = ref({})
// 角色权限配置（含覆盖）
const rolePermissions = ref({})

// 当前选中的角色
const selectedRole = ref('')
const selectedRoleData = computed(() => roles.value.find(r => r.code === selectedRole.value))

// 编辑中的权限
const editingPerms = reactive({})
const expiresAtInput = ref('')
const noteInput = ref('')
const currentOverride = ref(null)

// 用户列表
const users = ref([])
const editingUser = ref(null)
const editingUserRole = ref('')
const userOverride = reactive({
  temporaryRole: null,
  permissions: {},
  expiresAt: '',
  note: ''
})

// Toast
const toast = reactive({ show: false, message: '', type: 'info' })
function showToast(message, type = 'info') {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// 加载角色和权限定义
async function loadRolesAndPermissions() {
  loading.value = true
  try {
    const [rolesResp, permsResp, rolePermsResp] = await Promise.all([
      api.get('/api/rbac/roles'),
      api.get('/api/rbac/permissions'),
      api.get('/api/rbac/role-permissions')
    ])
    roles.value = rolesResp.data
    permissionKeys.value = permsResp.data.permission_keys
    defaultPermissions.value = permsResp.data.default_permissions
    rolePermissions.value = rolePermsResp.data

    if (roles.value.length > 0) {
      selectedRole.value = roles.value[0].code
      loadRoleToEditor()
    }
  } catch (err) {
    showToast(err.message || t('admin.loadFailed'), 'error')
  } finally {
    loading.value = false
  }
}

// 加载选中角色的权限到编辑器
function loadRoleToEditor() {
  if (!selectedRole.value) return
  const roleData = rolePermissions.value[selectedRole.value]
  if (!roleData) return

  // 使用有效权限（合并了覆盖后的）
  const effPerms = roleData.effective_permissions || roleData.default_permissions || {}
  Object.keys(editingPerms).forEach(k => delete editingPerms[k])
  permissionKeys.value.forEach(key => {
    editingPerms[key] = effPerms[key] || 'hidden'
  })

  // 加载覆盖信息
  currentOverride.value = roleData.override || null
  if (currentOverride.value) {
    noteInput.value = currentOverride.value.note || ''
    if (currentOverride.value.expires_at && !currentOverride.value.is_expired) {
      expiresAtInput.value = toLocalDatetimeInput(currentOverride.value.expires_at)
    } else {
      expiresAtInput.value = ''
    }
  } else {
    expiresAtInput.value = ''
    noteInput.value = ''
  }
}

// 监听角色切换
watch(selectedRole, () => loadRoleToEditor())

function getDefaultPerm(key) {
  const dp = defaultPermissions.value[selectedRole.value]
  return dp ? dp[key] || 'hidden' : 'hidden'
}

// 保存角色权限覆盖
async function saveRolePermissions() {
  if (!selectedRole.value) return
  try {
    const perms = { ...editingPerms }
    const expiresAt = expiresAtInput.value ? toISOString(expiresAtInput.value) : null
    await api.put(`/api/rbac/role-permissions/${selectedRole.value}`, {
      permissions: perms,
      expires_at: expiresAt,
      note: noteInput.value
    })
    showToast(t('admin.saveSuccess'), 'success')
    await loadRolesAndPermissions()
  } catch (err) {
    showToast(err.message || t('admin.saveFailed'), 'error')
  }
}

// 重置角色权限到默认
async function resetRolePermissions() {
  if (!selectedRole.value) return
  try {
    await api.del(`/api/rbac/role-permissions/${selectedRole.value}`)
    showToast(t('admin.resetSuccess'), 'success')
    await loadRolesAndPermissions()
  } catch (err) {
    showToast(err.message || t('admin.resetFailed'), 'error')
  }
}

// 加载用户列表
async function loadUsers() {
  usersLoading.value = true
  try {
    const resp = await api.get('/api/rbac/users')
    users.value = resp.data
  } catch (err) {
    showToast(err.message || t('admin.loadFailed'), 'error')
  } finally {
    usersLoading.value = false
  }
}

// 打开用户编辑弹窗
function openUserEditor(user) {
  editingUser.value = user
  editingUserRole.value = user.role

  // 初始化覆盖编辑器
  userOverride.temporaryRole = user.override?.temporary_role || null
  userOverride.note = user.override?.note || ''
  userOverride.expiresAt = user.override?.expires_at && !user.override.is_expired
    ? toLocalDatetimeInput(user.override.expires_at)
    : ''

  // 初始化权限覆盖
  Object.keys(userOverride.permissions).forEach(k => delete userOverride.permissions[k])
  permissionKeys.value.forEach(key => {
    userOverride.permissions[key] = user.override?.permissions?.[key] || ''
  })
}

function closeUserEditor() {
  editingUser.value = null
}

// 永久更改用户角色
async function saveUserRole() {
  if (!editingUser.value) return
  try {
    await api.put(`/api/rbac/users/${editingUser.value.id}/role`, {
      role: editingUserRole.value
    })
    showToast(t('admin.roleChanged'), 'success')
    await loadUsers()
  } catch (err) {
    showToast(err.message || t('admin.saveFailed'), 'error')
  }
}

// 保存用户权限覆盖
async function saveUserOverride() {
  if (!editingUser.value) return
  try {
    // 过滤空值
    const perms = {}
    Object.entries(userOverride.permissions).forEach(([k, v]) => {
      if (v) perms[k] = v
    })

    const expiresAt = userOverride.expiresAt ? toISOString(userOverride.expiresAt) : null
    await api.put(`/api/rbac/users/${editingUser.value.id}/override`, {
      temporary_role: userOverride.temporaryRole,
      permissions: perms,
      expires_at: expiresAt,
      note: userOverride.note
    })
    showToast(t('admin.saveSuccess'), 'success')
    await loadUsers()
  } catch (err) {
    showToast(err.message || t('admin.saveFailed'), 'error')
  }
}

// 重置用户权限覆盖
async function resetUserOverride() {
  if (!editingUser.value) return
  try {
    await api.del(`/api/rbac/users/${editingUser.value.id}/override`)
    showToast(t('admin.resetSuccess'), 'success')
    await loadUsers()
    closeUserEditor()
  } catch (err) {
    showToast(err.message || t('admin.resetFailed'), 'error')
  }
}

// 工具函数
function getRoleLabel(code) {
  const role = roles.value.find(r => r.code === code)
  return role ? role.label : code
}

function formatDateTime(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return d.toLocaleString()
}

function toLocalDatetimeInput(isoStr) {
  const d = new Date(isoStr)
  const tzOffset = d.getTimezoneOffset() * 60000
  return new Date(d.getTime() - tzOffset).toISOString().slice(0, 16)
}

function toISOString(localInput) {
  if (!localInput) return null
  const d = new Date(localInput)
  return d.toISOString()
}

onMounted(() => {
  loadRolesAndPermissions()
  loadUsers()
})
</script>

