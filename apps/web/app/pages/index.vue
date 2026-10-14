
<script setup lang="ts">
import {
  ArrowRight,
  ArrowUpRight,
  BadgeCheck,
  CheckCheck,
  CircleHelp,
  Fingerprint,
  Globe2,
  LockKeyhole,
  MessageCircleMore,
  MessageSquareText,
  Radar,
  Search,
  ShieldCheck,
  Sparkles,
  Star,
  Users,
  WandSparkles
} from '@lucide/vue'

const { c } = useSiteCopy()

const localNumber = ref('')
const searchError = ref('')

function search() {
  const full = toMontenegroE164(localNumber.value)

  if (!full) {
    searchError.value = c.value.searchError
    return
  }

  searchError.value = ''

  return navigateTo(
    `/number/${encodeURIComponent(full)}`
  )
}

const steps = computed(() => [
  {
    title: c.value.step1Title,
    description: c.value.step1Text,
    icon: Search
  },
  {
    title: c.value.step2Title,
    description: c.value.step2Text,
    icon: MessageSquareText
  },
  {
    title: c.value.step3Title,
    description: c.value.step3Text,
    icon: Users
  }
])

const details = computed(() => [
  {
    title: c.value.detail1Title,
    description: c.value.detail1Text,
    icon: MessageCircleMore
  },
  {
    title: c.value.detail2Title,
    description: c.value.detail2Text,
    icon: Star
  },
  {
    title: c.value.detail3Title,
    description: c.value.detail3Text,
    icon: BadgeCheck
  }
])

let observer: IntersectionObserver | null = null

onMounted(() => {
  if (
    !('IntersectionObserver' in window) ||
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  ) {
    return
  }

  const elements = document.querySelectorAll<HTMLElement>(
    '.home-page [data-reveal]'
  )

  observer = new IntersectionObserver(
    entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          observer?.unobserve(entry.target)
        }
      }
    },
    {
      threshold: 0.12,
      rootMargin: '0px 0px -24px 0px'
    }
  )

  elements.forEach(element => {
    element.classList.add('is-pending')
    observer?.observe(element)
  })
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="home-page">
    <section class="home-hero">
      <div
        class="hero-gradient hero-gradient-one"
        aria-hidden="true"
      ></div>

      <div
        class="hero-gradient hero-gradient-two"
        aria-hidden="true"
      ></div>

      <div class="container hero-new-layout">
        <div class="hero-new-content">

          <h1 class="hero-new-heading">
            {{ c.heroTitle1 }}
            <span>{{ c.heroTitle2 }}</span>
          </h1>

          <p class="hero-new-description">
            {{ c.heroDescription }}
          </p>

          <form
            class="hero-search"
            @submit.prevent="search"
          >
            <div
              class="hero-search-prefix"
              aria-label="Country code +382"
            >
              <span class="flag" aria-hidden="true">
                🇲🇪
              </span>

              <span>+382</span>
            </div>

            <input
              v-model="localNumber"
              type="tel"
              inputmode="tel"
              autocomplete="off"
              placeholder="XX XXX XXX"
              aria-label="Phone number without country code"
              maxlength="24"
              required
              @input="searchError = ''"
            />

            <button
              class="hero-search-button"
              type="submit"
            >
              {{ c.searchButton }}
              <ArrowRight :size="18" />
            </button>
          </form>

          <p
            v-if="searchError"
            class="hero-search-error"
            role="alert"
          >
            {{ searchError }}
          </p>

        </div>

        <div class="hero-art" aria-hidden="true">
          <div class="signal-ring ring-one"></div>
          <div class="signal-ring ring-two"></div>
          <div class="signal-ring ring-three"></div>

          <div class="signal-node node-one"></div>
          <div class="signal-node node-two"></div>

          <div class="floating-chip chip-top">
            <span class="chip-icon green">
              <ShieldCheck :size="18" />
            </span>

            <div>
              <strong>{{ c.trustModeration }}</strong>
              <small>{{ c.visualInfo }}</small>
            </div>
          </div>

          <div class="lookup-preview">
            <div class="lookup-preview-top">
              <span class="preview-caption">
                <Radar :size="16" />
                KoZove
              </span>

              <span class="preview-demo-badge">
                {{ c.visualDemo }}
              </span>
            </div>

            <div class="lookup-icon">
              <Fingerprint
                :size="29"
                :stroke-width="1.6"
              />
            </div>

            <div class="lookup-number">
              {{ c.visualNumber }}
            </div>

            <p class="lookup-unknown">
              {{ c.visualUnknown }}
            </p>

            <div class="lookup-divider"></div>

            <div class="lookup-status">
              <div>
                <strong>{{ c.visualStatus }}</strong>
                <p>{{ c.visualNote }}</p>
              </div>

              <CircleHelp :size="19" />
            </div>

            <div class="lookup-mini-grid">
              <div>
                <Star :size="17" />
                {{ c.visualRating }}
              </div>

              <div>
                <MessageCircleMore :size="17" />
                {{ c.visualReports }}
              </div>
            </div>
          </div>

          <div class="floating-chip chip-bottom">
            <span class="chip-icon violet">
              <Globe2 :size="17" />
            </span>

            {{ c.trustNoAccount }}
            <ArrowUpRight :size="14" />
          </div>
        </div>
      </div>
    </section>

    <section
      id="how-it-works"
      class="landing-section how-section"
    >
      <div class="container">
        <div class="section-intro" data-reveal>
          <div class="section-kicker">
            <Sparkles :size="16" />
            {{ c.howEyebrow }}
          </div>

          <h2>{{ c.howTitle }}</h2>
          <p>{{ c.howSubtitle }}</p>
        </div>

        <div class="how-grid" data-reveal>
          <article
            v-for="(step, index) in steps"
            :key="index"
            class="how-card"
          >
            <div class="how-card-top">
              <div class="how-icon">
                <component
                  :is="step.icon"
                  :size="25"
                />
              </div>

              <span>0{{ index + 1 }}</span>
            </div>

            <h3>{{ step.title }}</h3>
            <p>{{ step.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="landing-section details-section">
      <div class="container details-layout">
        <div class="details-intro" data-reveal>
          <div class="section-kicker">
            <WandSparkles :size="15" />
            {{ c.detailEyebrow }}
          </div>

          <h2>{{ c.detailTitle }}</h2>
          <p>{{ c.detailDescription }}</p>
        </div>

        <div class="details-cards" data-reveal>
          <article
            v-for="item in details"
            :key="item.title"
            class="detail-card"
          >
            <div class="detail-icon">
              <component
                :is="item.icon"
                :size="21"
              />
            </div>

            <div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>

            <ArrowUpRight
              class="detail-arrow"
              :size="17"
            />
          </article>
        </div>
      </div>
    </section>

    <section class="safety-section">
      <div class="container">
        <div class="safety-panel" data-reveal>
          <div class="safety-icon">
            <ShieldCheck :size="29" />
          </div>

          <div class="safety-content">
            <h2>{{ c.safetyTitle }}</h2>
            <p>{{ c.safetyText }}</p>
          </div>

          <NuxtLink
            to="/privacy"
            class="safety-button"
          >
            {{ c.safetyLink }}
            <ArrowRight :size="17" />
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
[data-reveal] {
  transition:
    opacity .7s ease,
    transform .7s cubic-bezier(.2, .7, .2, 1);
}

[data-reveal].is-pending {
  opacity: 0;
  transform: translateY(28px);
}

[data-reveal].is-pending.is-visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
</style>
