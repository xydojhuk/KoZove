
<script setup lang="ts">
import {
  ArrowUpRight,
  ChevronRight,
  Heart,
  Menu,
  X,
  ShieldCheck
} from '@lucide/vue'

const { locale } = useLocale()
const { c } = useSiteCopy()
const route = useRoute()
const { public: publicConfig } = useRuntimeConfig()

const isAdmin = computed(
  () =>
    route.path === '/admin' ||
    route.path.startsWith('/admin/')
)

const dialogOpen = ref(false)
const mobileMenuOpen = ref(false)

function openProjectDialog() {
  mobileMenuOpen.value = false
  dialogOpen.value = true
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

useHead({
  htmlAttrs: {
    lang: computed(
      () => locale.value === 'sr'
        ? 'sr-Latn'
        : locale.value
    )
  }
})
</script>

<template>
  <div
    class="app-shell"
    :class="{ 'admin-app-shell': isAdmin }"
  >
    <template v-if="!isAdmin">
      <button
        class="announcement"
        type="button"
        @click="openProjectDialog"
      >
        <ShieldCheck :size="15" />
        <span>{{ c.topText }}</span>

        <strong>
          {{ c.topAction }}
          <ChevronRight :size="14" />
        </strong>
      </button>

      <header class="site-header">
        <div class="container nav-shell">
          <NuxtLink
            to="/"
            class="brand brand-new"
            @click="closeMobileMenu"
          >
            <span class="brand-symbol">
              <span class="brand-symbol-ring"></span>
              <span class="brand-symbol-dot"></span>
            </span>

            <span class="brand-word">
              KoZove<span>.</span>
            </span>
          </NuxtLink>

          <nav class="nav-links">
            <NuxtLink to="/" @click="closeMobileMenu">
              {{ c.navHome }}
            </NuxtLink>

            <NuxtLink
              to="/#how-it-works"
              @click="closeMobileMenu"
            >
              {{ c.navHow }}
            </NuxtLink>

            <button
              type="button"
              @click="openProjectDialog"
            >
              {{ c.navAbout }}
            </button>
          </nav>

          <div class="nav-actions">
            <select
              v-model="locale"
              class="locale-switch"
              aria-label="Language"
            >
              <option value="sr">SR</option>
              <option value="ru">RU</option>
              <option value="en">EN</option>
            </select>

            <button
              class="header-support"
              type="button"
              @click="openProjectDialog"
            >
              <Heart :size="16" />
              <span>{{ c.navSupport }}</span>
              <ArrowUpRight :size="14" />
            </button>

            <button
              class="mobile-menu-button"
              type="button"
              :aria-expanded="mobileMenuOpen"
              aria-label="Toggle navigation"
              @click="mobileMenuOpen = !mobileMenuOpen"
            >
              <X v-if="mobileMenuOpen" :size="22" />
              <Menu v-else :size="22" />
            </button>
          </div>
        </div>

        <Transition name="mobile-nav">
          <nav
            v-if="mobileMenuOpen"
            class="mobile-nav-links"
          >
            <NuxtLink to="/" @click="closeMobileMenu">
              {{ c.navHome }}
            </NuxtLink>

            <NuxtLink
              to="/#how-it-works"
              @click="closeMobileMenu"
            >
              {{ c.navHow }}
            </NuxtLink>

            <button @click="openProjectDialog">
              {{ c.navAbout }}
            </button>

            <button @click="openProjectDialog">
              {{ c.navSupport }}
            </button>
          </nav>
        </Transition>
      </header>
    </template>

    <main class="main-content">
      <NuxtPage />
    </main>

    <footer
      v-if="!isAdmin"
      class="site-footer site-footer-new"
    >
      <div class="container">
        <div class="footer-main">
          <div>
            <div class="footer-brand">
              KoZove<span>.</span>
            </div>

            <p class="footer-tagline">
              {{ c.footerTagline }}
            </p>
          </div>

          <div class="footer-links">
            <button
              type="button"
              @click="openProjectDialog"
            >
              {{ c.navAbout }}
            </button>

            <button
              type="button"
              @click="openProjectDialog"
            >
              {{ c.navSupport }}
            </button>

            <NuxtLink to="/privacy">
              {{ c.footerPrivacy }}
            </NuxtLink>

            <NuxtLink to="/terms">
              {{ c.footerTerms }}
            </NuxtLink>
          </div>
        </div>

        <div class="footer-bottom">
          <span>© 2026 KoZove · Open Source · v{{ publicConfig.appVersion }}</span>
        </div>
      </div>
    </footer>

    <ProjectDialog
      v-if="!isAdmin"
      :open="dialogOpen"
      @close="dialogOpen = false"
    />
  </div>
</template>
