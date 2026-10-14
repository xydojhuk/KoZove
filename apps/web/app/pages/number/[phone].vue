
<script setup lang="ts">
import {
  AlertCircle,
  ArrowLeft,
  ArrowRight,
  BadgeCheck,
  Flag,
  MessageSquarePlus,
  RefreshCw,
  ShieldCheck,
  Star
} from '@lucide/vue'

type Review = {
  id: number
  rating: number
  category: string
  text: string
  created_at: string
}

type PhoneData = {
  found: boolean
  number: string
  number_type: string
  business_name: string | null
  source_url: string | null
  rating: number | null
  rating_count: number
  complaints: number
  has_warnings: boolean
  reviews: Review[]
}

const route = useRoute()
const config = useRuntimeConfig()
const { t, locale } = useLocale()

const phone = computed(
  () => String(route.params.phone || '')
)

const {
  data,
  error,
  refresh,
  status
} = await useFetch<PhoneData>(
  '/api/v1/phone/lookup',
  {
    query: { q: phone },
    watch: [phone]
  }
)

useSeoMeta({
  title: computed(
    () => `${data.value?.number || phone.value} — KoZove`
  ),

  description: computed(
    () => `Phone number community reviews: ${
      data.value?.number || phone.value
    }`
  ),

  robots: computed(
    () => data.value?.found
      ? 'index,follow'
      : 'noindex,follow'
  )
})

const mode = ref<'review' | 'report' | 'appeal' | null>(null)
const widgetVersion = ref(0)
const token = ref('')

const rating = ref(5)
const reviewCategory = ref('normal')
const reportCategory = ref('ads')

const comment = ref('')
const contactEmail = ref('')
const reviewId = ref<number | null>(null)

const submitting = ref(false)
const success = ref(false)
const formError = ref('')

const reviewCategories = [
  { value: 'normal', key: 'catNormal' },
  { value: 'delivery', key: 'catDelivery' },
  { value: 'ads', key: 'catAds' },
  { value: 'survey', key: 'catSurvey' },
  { value: 'suspicious', key: 'catSuspicious' },
  { value: 'robot', key: 'catRobot' },
  { value: 'other', key: 'catOther' }
] as const

const reportCategories = [
  { value: 'scam', key: 'catScam' },
  { value: 'ads', key: 'catAds' },
  { value: 'harassment', key: 'catHarassment' },
  { value: 'data', key: 'catData' },
  { value: 'robot', key: 'catRobot' },
  { value: 'other', key: 'catOther' }
] as const

function categoryText(value: string): string {
  const item = [
    ...reviewCategories,
    ...reportCategories
  ].find(x => x.value === value)

  return item ? t(item.key) : value
}

function openForm(
  next: 'review' | 'report' | 'appeal',
  id: number | null = null
) {
  mode.value = next
  reviewId.value = id
  token.value = ''
  comment.value = ''
  contactEmail.value = ''
  formError.value = ''
  success.value = false
  widgetVersion.value++

  if (import.meta.client) {
    window.setTimeout(() => {
      document
        .getElementById('submission-form')
        ?.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
    }, 80)
  }
}

async function submit() {
  if (!mode.value || !token.value || submitting.value) {
    return
  }

  submitting.value = true
  formError.value = ''

  try {
    const shared = {
      number: phone.value,
      turnstile_token: token.value
    }

    if (mode.value === 'review') {
      await $fetch('/api/v1/reviews', {
        method: 'POST',
        body: {
          ...shared,
          rating: rating.value,
          category: reviewCategory.value,
          text: comment.value
        }
      })

    } else if (mode.value === 'report') {
      await $fetch('/api/v1/reports', {
        method: 'POST',
        body: {
          ...shared,
          category: reportCategory.value,
          text: comment.value
        }
      })

    } else {
      await $fetch('/api/v1/appeals', {
        method: 'POST',
        body: {
          ...shared,
          text: comment.value,
          review_id: reviewId.value,
          contact_email: contactEmail.value || null
        }
      })
    }

    success.value = true
    mode.value = null
    await refresh()

  } catch (e: any) {
    const detail = e?.data?.detail

    formError.value =
      typeof detail === 'string'
        ? detail
        : t('errorMessage')

    token.value = ''
    widgetVersion.value++

  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="content-page">
    <div class="container result-container">
      <NuxtLink to="/" class="back-link">
        <ArrowLeft :size="17" />
        {{ t('home') }}
      </NuxtLink>

      <div
        v-if="status === 'pending'"
        class="page-card state-card"
        role="status"
      >
        <div class="loading-spinner"></div>
        <p>Loading...</p>
      </div>

      <div
        v-else-if="error"
        class="page-card state-card"
        role="alert"
      >
        <div class="state-icon warning">
          <AlertCircle :size="28" />
        </div>

        <h2>{{ t('errorMessage') }}</h2>

        <p class="muted">
          HTTP {{ error.statusCode || 502 }}
        </p>

        <button
          class="btn btn-primary"
          @click="refresh()"
        >
          <RefreshCw :size="16" />
          Retry
        </button>
      </div>

      <template v-else-if="data">
        <div class="page-card result-header">
          <div class="result-topline">
            <span class="badge">
              <ShieldCheck :size="15" />
              KoZove · Montenegro
            </span>

            <span
              v-if="data.business_name"
              class="badge verified"
            >
              <BadgeCheck :size="15" />
              {{ t('knownBusiness') }}
            </span>
          </div>

          <p class="result-eyebrow">
            Phone lookup
          </p>

          <h1 class="result-number">
            {{ data.number }}
          </h1>

          <h2 class="result-name">
            {{ data.business_name || t('unknown') }}
          </h2>

          <a
            v-if="data.source_url"
            :href="data.source_url"
            target="_blank"
            rel="noopener noreferrer"
            class="source-link"
          >
            <BadgeCheck :size="15" />
            {{ t('source') }} ↗
          </a>

          <div class="stats-grid">
            <div class="stat">
              <strong>{{ data.rating ?? '—' }}</strong>
              <span>{{ t('rating') }}</span>
            </div>

            <div class="stat">
              <strong>{{ data.rating_count }}</strong>
              <span>{{ t('reviews') }}</span>
            </div>

            <div class="stat">
              <strong>{{ data.complaints }}</strong>
              <span>{{ t('complaints') }}</span>
            </div>
          </div>

          <p
            v-if="data.rating === null"
            class="muted small"
          >
            {{ t('notEnough') }}
          </p>

          <div
            v-if="data.has_warnings"
            class="notice warning"
          >
            <strong>{{ t('reportsWarning') }}</strong>
            <p>{{ t('reportNotice') }}</p>
          </div>

          <div v-if="!data.found" class="notice">
            {{ t('noData') }}
          </div>

          <div class="button-row result-buttons">
            <button
              class="btn btn-primary"
              @click="openForm('review')"
            >
              <MessageSquarePlus :size="17" />
              {{ t('writeReview') }}
            </button>

            <button
              class="btn btn-outline"
              @click="openForm('report')"
            >
              <Flag :size="17" />
              {{ t('writeReport') }}
            </button>

            <button
              class="btn btn-soft"
              @click="openForm('appeal')"
            >
              {{ t('appeal') }}
            </button>
          </div>
        </div>

        <div
          v-if="success"
          class="notice success-notice"
          role="status"
        >
          {{ t('pendingMessage') }}
        </div>

        <form
          v-if="mode"
          id="submission-form"
          class="page-card submission-form"
          @submit.prevent="submit"
        >
          <div class="section-heading">
            <h2>
              {{
                mode === 'review'
                  ? t('writeReview')
                  : mode === 'report'
                    ? t('writeReport')
                    : t('appeal')
              }}
            </h2>

            <button
              type="button"
              class="btn btn-outline btn-small"
              @click="mode = null"
            >
              {{ t('cancel') }}
            </button>
          </div>

          <div
            v-if="mode === 'review'"
            class="field"
          >
            <label>{{ t('stars') }}</label>

            <div class="rating-options">
              <button
                v-for="n in 5"
                :key="n"
                type="button"
                :class="[
                  'rating-button',
                  { selected: rating === n }
                ]"
                :aria-pressed="rating === n"
                @click="rating = n"
              >
                <Star
                  :size="19"
                  :fill="
                    rating === n
                      ? 'currentColor'
                      : 'none'
                  "
                />
                {{ n }}
              </button>
            </div>
          </div>

          <div
            v-if="mode !== 'appeal'"
            class="field"
          >
            <label>{{ t('category') }}</label>

            <select
              v-if="mode === 'review'"
              v-model="reviewCategory"
              class="input"
            >
              <option
                v-for="item in reviewCategories"
                :key="item.value"
                :value="item.value"
              >
                {{ t(item.key) }}
              </option>
            </select>

            <select
              v-else
              v-model="reportCategory"
              class="input"
            >
              <option
                v-for="item in reportCategories"
                :key="item.value"
                :value="item.value"
              >
                {{ t(item.key) }}
              </option>
            </select>
          </div>

          <div class="field">
            <label>{{ t('comment') }}</label>

            <textarea
              v-model="comment"
              class="input"
              :minlength="
                mode === 'report' ? 0 : 10
              "
              :maxlength="
                mode === 'appeal' ? 1500 : 600
              "
              :required="mode !== 'report'"
            />

            <span class="muted small">
              {{ comment.length }} /
              {{ mode === 'appeal' ? 1500 : 600 }}
            </span>
          </div>

          <div
            v-if="mode === 'appeal'"
            class="field"
          >
            <label>{{ t('emailOptional') }}</label>

            <input
              v-model="contactEmail"
              type="email"
              class="input"
              autocomplete="email"
            />
          </div>

          <p class="muted small">
            {{ t('reviewNotice') }}
          </p>

          <ClientOnly>
            <TurnstileWidget
              :key="widgetVersion"
              :sitekey="config.public.turnstileSitekey"
              @token="token = $event"
            />
          </ClientOnly>

          <div
            v-if="formError"
            class="notice error"
            role="alert"
          >
            {{ formError }}
          </div>

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="submitting || !token"
          >
            {{ t('send') }}
            <ArrowRight :size="17" />
          </button>
        </form>

        <section class="reviews-section">
          <div class="section-heading">
            <h2>
              {{ t('reviews') }}
              <span class="muted">
                {{ data.rating_count }}
              </span>
            </h2>
          </div>

          <div
            v-if="!data.reviews.length"
            class="page-card empty-reviews"
          >
            <MessageSquarePlus :size="28" />
            <p>{{ t('noReviews') }}</p>
          </div>

          <div v-else class="review-list">
            <article
              v-for="review in data.reviews"
              :key="review.id"
              class="review-item"
            >
              <div class="review-topline">
                <span class="stars">
                  {{ '★'.repeat(review.rating) }}
                  {{ '☆'.repeat(5 - review.rating) }}
                </span>

                <span class="badge">
                  {{ categoryText(review.category) }}
                </span>
              </div>

              <p>{{ review.text }}</p>

              <div class="review-bottom">
                <span class="muted small">
                  {{
                    new Date(
                      review.created_at
                    ).toLocaleDateString(
                      locale === 'sr'
                        ? 'sr-Latn-ME'
                        : locale === 'ru'
                          ? 'ru-RU'
                          : 'en-GB'
                    )
                  }}
                </span>

                <button
                  class="btn btn-outline btn-small"
                  @click="
                    openForm('appeal', review.id)
                  "
                >
                  {{ t('appeal') }}
                </button>
              </div>
            </article>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>
