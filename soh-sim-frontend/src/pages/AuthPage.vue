<template>
  <div class="auth-landing">
    <!-- 左侧：功能亮点 -->
    <aside class="auth-aside">
      <div class="auth-aside-inner">
        <h2 class="auth-aside-title">{{ $t('home.heroBadge') }}</h2>
        <p class="auth-aside-lead">{{ $t('home.heroLeadText') }}</p>
        <ul class="auth-aside-list">
          <li v-for="feat in features" :key="feat.key">
            <span class="auth-aside-dot" :class="feat.iconClass" />
            <div>
              <strong>{{ $t(feat.titleKey) }}</strong>
              <p>{{ $t(feat.descKey) }}</p>
            </div>
          </li>
        </ul>
      </div>
    </aside>

    <!-- 右侧：登录/注册表单 -->
    <main class="auth-main">
      <AuthPanel :default-mode="defaultMode" @auth-success="onAuthSuccess" @error="onError" />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthPanel from '../components/AuthPanel.vue'

const route = useRoute()
const router = useRouter()

const defaultMode = computed(() => (route.query.mode === 'register' ? 'register' : 'login'))

const features = [
  {
    key: 'config',
    iconClass: 'dot-blue',
    titleKey: 'home.feature1Title',
    descKey: 'home.feature1Desc'
  },
  {
    key: 'soh',
    iconClass: 'dot-green',
    titleKey: 'home.feature2Title',
    descKey: 'home.feature2Desc'
  },
  {
    key: 'finance',
    iconClass: 'dot-amber',
    titleKey: 'home.feature3Title',
    descKey: 'home.feature3Desc'
  },
  {
    key: 'compliance',
    iconClass: 'dot-purple',
    titleKey: 'home.feature4Title',
    descKey: 'home.feature4Desc'
  }
]

function onAuthSuccess() {
  router.push('/')
}

function onError() {
  // AuthPanel 自带错误提示
}
</script>

<style scoped>
.auth-landing {
  display: flex;
  min-height: 100%;
}

.auth-aside {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: radial-gradient(
    ellipse 80% 60% at 30% 50%,
    var(--color-accent-glow, rgba(0, 102, 204, 0.08)) 0%,
    transparent 70%
  );
  border-right: 1px solid var(--color-border);
}

.auth-aside-inner {
  max-width: 440px;
}

.auth-aside-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-accent);
  margin: 0 0 16px;
  letter-spacing: -0.02em;
}

.auth-aside-lead {
  font-size: 15px;
  color: var(--color-text-secondary, var(--text-secondary));
  line-height: 1.6;
  margin: 0 0 32px;
}

.auth-aside-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.auth-aside-list li {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.auth-aside-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.dot-blue {
  background: #0066cc;
}
.dot-green {
  background: #10b981;
}
.dot-amber {
  background: #f59e0b;
}
.dot-purple {
  background: #8b5cf6;
}

.auth-aside-list strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text, var(--text-primary));
  display: block;
  margin-bottom: 2px;
}

.auth-aside-list p {
  font-size: 13px;
  color: var(--color-text-secondary, var(--text-secondary));
  line-height: 1.4;
  margin: 0;
}

.auth-main {
  flex: 0 0 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

@media (max-width: 900px) {
  .auth-aside {
    display: none;
  }
  .auth-main {
    flex: 1;
  }
}
</style>
