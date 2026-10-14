
<script setup lang="ts">
import {
  Activity,
  ArrowLeft,
  ArrowRight,
  BookOpenCheck,
  Check,
  CheckCircle2,
  ChevronDown,
  CircleAlert,
  ExternalLink,
  FileWarning,
  Filter,
  Globe2,
  History,
  LayoutDashboard,
  LockKeyhole,
  LogOut,
  Menu,
  MessageSquareText,
  MoreHorizontal,
  Phone,
  Plus,
  RefreshCw,
  Search,
  Settings2,
  ShieldCheck,
  ShieldAlert,
  Trash2,
  X
} from '@lucide/vue'

useSeoMeta({
  title: 'KoZove · Управление',
  robots: 'noindex,nofollow'
})

type Section =
  | 'overview'
  | 'reviews'
  | 'reports'
  | 'phones'
  | 'appeals'
  | 'audit'
  | 'settings'

type Row = Record<string, any>

type PageData = {
  items: Row[]
  total: number
  page: number
  pages: number
  size: number
}

type Overview = {
  phones: number
  reviews: Record<string, number>
  reports: Record<string, number>
  appeals: Record<string, number>
  mode: string

  latest_reviews: {
    id: number
    number: string
    text: string
    rating: number
  }[]
}

const items = [
  {
    id: 'overview',
    name: 'Обзор',
    icon: LayoutDashboard,
    group: 'ОБЩЕЕ'
  },
  {
    id: 'reviews',
    name: 'Отзывы',
    icon: MessageSquareText,
    group: 'МОДЕРАЦИЯ'
  },
  {
    id: 'reports',
    name: 'Жалобы на звонки',
    icon: ShieldAlert,
    group: 'МОДЕРАЦИЯ'
  },
  {
    id: 'appeals',
    name: 'Обращения',
    icon: FileWarning,
    group: 'МОДЕРАЦИЯ'
  },
  {
    id: 'phones',
    name: 'Телефонный справочник',
    icon: Phone,
    group: 'КОНТЕНТ'
  },
  {
    id: 'audit',
    name: 'Журнал действий',
    icon: History,
    group: 'СИСТЕМА'
  },
  {
    id: 'settings',
    name: 'Управление сайтом',
    icon: Settings2,
    group: 'СИСТЕМА'
  }
] as const

const { public: publicConfig } = useRuntimeConfig()

const authed = ref(false)
const checking = ref(true)

const username = ref('admin')
const password = ref('')

const active = ref<Section>('overview')
const mobileNav = ref(false)

const busy = ref(false)
const refreshing = ref(false)

const notice = ref('')
const error = ref('')

const summary = ref<Overview | null>(null)

const pageData = ref<PageData>({
  items: [],
  total: 0,
  page: 1,
  pages: 1,
  size: 12
})

const filter = ref('pending')
const searchText = ref('')
const appliedSearch = ref('')
const page = ref(1)

const selected = ref<Row | null>(null)

const phoneEditor = ref(false)
const phoneEditorId = ref<number | null>(null)

const phoneForm = reactive({
  number: '',
  business_name: '',
  source_url: ''
})

const siteMode = ref('normal')

const isList = computed(() =>
  [
    'reviews',
    'reports',
    'phones',
    'appeals',
    'audit'
  ].includes(active.value)
)

const title = computed(() =>
  items.find(x => x.id === active.value)?.name || 'Обзор'
)

const filters = computed(() => {
  if (active.value === 'phones') {
    return [
      ['all', 'Все номера'],
      ['listed', 'Организации'],
      ['unlisted', 'Без организации']
    ]
  }

  if (active.value === 'appeals') {
    return [
      ['pending', 'Ожидают'],
      ['resolved', 'Решены'],
      ['rejected', 'Отклонены'],
      ['all', 'Все']
    ]
  }

  if (active.value === 'audit') {
    return []
  }

  return [
    ['pending', 'Ожидают'],
    ['approved', 'Одобрены'],
    ['rejected', 'Отклонены'],
    ['hidden', 'Скрыты'],
    ['all', 'Все']
  ]
})

function statusName(value: string) {
  return ({
    pending: 'Ожидает решения',
    approved: 'Одобрено',
    rejected: 'Отклонено',
    hidden: 'Скрыто',
    resolved: 'Решено'
  } as Record<string, string>)[value] || value
}

function kindName(value: string) {
  return ({
    normal: 'Обычный звонок',
    delivery: 'Доставка',
    ads: 'Реклама',
    survey: 'Опрос',
    suspicious: 'Подозрительный',
    robot: 'Автообзвон',
    other: 'Другое',
    scam: 'Подозрение на мошенничество',
    harassment: 'Навязчивый звонок',
    data: 'Получение данных'
  } as Record<string, string>)[value] || value
}

function displayDate(value?: string) {
  if (!value) return '—'

  const date = new Date(value)

  if (Number.isNaN(date.valueOf())) {
    return '—'
  }

  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function apiStatus(e: any) {
  return Number(
    e?.statusCode ??
    e?.response?.status ??
    0
  )
}

function apiError(e: any) {
  const detail = e?.data?.detail

  return typeof detail === 'string'
    ? detail
    : `Ошибка запроса (HTTP ${apiStatus(e) || '?'})`
}

async function loadOverview() {
  summary.value = await $fetch<Overview>(
    '/api/v1/admin/manage/overview'
  )

  siteMode.value = summary.value.mode
}

async function loadTable() {
  if (!isList.value) return

  refreshing.value = true

  try {
    pageData.value = await $fetch<PageData>(
      `/api/v1/admin/manage/${active.value}`,
      {
        query: {
          page: page.value,
          size: 12,

          ...(active.value !== 'audit'
            ? { status: filter.value }
            : {}),

          ...(appliedSearch.value
            ? { q: appliedSearch.value }
            : {})
        }
      }
    )
  } finally {
    refreshing.value = false
  }
}

async function reload() {
  try {
    error.value = ''

    await loadOverview()
    await loadTable()

  } catch (e: any) {
    error.value = apiError(e)

    if (apiStatus(e) === 401) {
      authed.value = false
    }
  }
}

onMounted(async () => {
  try {
    await $fetch('/api/v1/admin/me')

    authed.value = true
    await reload()

  } catch (e: any) {
    if (apiStatus(e) !== 401) {
      error.value = apiError(e)
    }

  } finally {
    checking.value = false
  }
})

async function login() {
  if (busy.value) return

  busy.value = true
  error.value = ''

  try {
    await $fetch('/api/v1/admin/login', {
      method: 'POST',
      body: {
        username: username.value,
        password: password.value
      }
    })

    password.value = ''
    authed.value = true

    await reload()

  } catch (e: any) {
    error.value =
      apiStatus(e) === 401
        ? 'Неверный логин или пароль'
        : apiError(e)

  } finally {
    busy.value = false
  }
}

async function logout() {
  try {
    await $fetch('/api/v1/admin/logout', {
      method: 'POST',
      headers: {
        'x-kozove-admin': '1'
      }
    })
  } finally {
    authed.value = false
    selected.value = null
    summary.value = null
  }
}

async function section(next: Section) {
  active.value = next
  mobileNav.value = false
  selected.value = null

  page.value = 1
  searchText.value = ''
  appliedSearch.value = ''

  filter.value =
    next === 'phones' || next === 'audit'
      ? 'all'
      : 'pending'

  await reload()
}

async function changeFilter() {
  page.value = 1
  await loadSafe()
}

async function doSearch() {
  appliedSearch.value = searchText.value.trim()
  page.value = 1

  await loadSafe()
}

async function move(to: number) {
  page.value = to
  await loadSafe()
}

async function loadSafe() {
  try {
    error.value = ''
    await loadTable()
  } catch (e: any) {
    error.value = apiError(e)
  }
}

async function mutate(
  path: string,
  method: 'POST' | 'PATCH' | 'PUT' | 'DELETE',
  body?: any
): Promise<boolean> {
  if (busy.value) return false

  busy.value = true
  notice.value = ''
  error.value = ''

  try {
    await $fetch(path, {
      method,
      body,
      headers: {
        'x-kozove-admin': '1'
      }
    })

    notice.value = 'Изменения сохранены'
    selected.value = null

    await reload()

    return true

  } catch (e: any) {
    error.value = apiError(e)

    if (apiStatus(e) === 401) {
      authed.value = false
    }

    return false

  } finally {
    busy.value = false
  }
}

function endpoint(row: Row) {
  if (active.value === 'reviews') {
    return `/api/v1/admin/reviews/${row.id}`
  }

  if (active.value === 'reports') {
    return `/api/v1/admin/reports/${row.id}`
  }

  if (active.value === 'appeals') {
    return `/api/v1/admin/appeals/${row.id}`
  }

  return `/api/v1/admin/phones/${row.id}`
}

async function decide(row: Row, value: string) {
  if (row.status !== 'pending') return

  await mutate(
    endpoint(row),
    'PATCH',
    { status: value }
  )
}

async function removeSelected() {
  if (!selected.value || active.value === 'audit') {
    return
  }

  if (!window.confirm(
    'Удалить запись? Действие нельзя отменить.'
  )) {
    return
  }

  await mutate(
    endpoint(selected.value),
    'DELETE'
  )
}

function createPhone() {
  phoneEditorId.value = null

  Object.assign(phoneForm, {
    number: '',
    business_name: '',
    source_url: ''
  })

  phoneEditor.value = true
}

function editPhone(row: Row) {
  phoneEditorId.value = row.id

  Object.assign(phoneForm, {
    number: row.number,
    business_name: row.business_name || '',
    source_url: row.source_url || ''
  })

  selected.value = null
  phoneEditor.value = true
}

async function savePhone() {
  const body = {
    business_name:
      phoneForm.business_name.trim() || null,

    source_url:
      phoneForm.source_url.trim() || null
  }

  const successful = phoneEditorId.value
    ? await mutate(
        `/api/v1/admin/phones/${phoneEditorId.value}`,
        'PATCH',
        body
      )
    : await mutate(
        '/api/v1/admin/phones',
        'POST',
        {
          number: phoneForm.number.trim(),
          ...body
        }
      )

  if (successful) {
    phoneEditor.value = false
  }
}

async function saveMode() {
  await mutate(
    '/api/v1/admin/maintenance',
    'PUT',
    { mode: siteMode.value }
  )
}
</script>

<template>
  <div class="admin-page">
    <!-- Session check -->
    <div v-if="checking" class="admin-center">
      <RefreshCw class="admin-spin" :size="24" />
      Проверка сеанса...
    </div>

    <!-- Login -->
    <div v-else-if="!authed" class="admin-login-wrap">
      <div class="admin-login-card">
        <div class="admin-login-icon">
          <ShieldCheck :size="26" />
        </div>

        <div class="admin-kicker">
          ПАНЕЛЬ УПРАВЛЕНИЯ
        </div>

        <h1>Добро пожаловать</h1>

        <p>
          Закрытый кабинет администратора KoZove.
          Регистрация недоступна.
        </p>

        <form @submit.prevent="login">
          <label>
            Логин
            <input
              v-model="username"
              class="admin-input"
              autocomplete="username"
              required
            />
          </label>

          <label>
            Пароль
            <input
              v-model="password"
              class="admin-input"
              type="password"
              autocomplete="current-password"
              required
            />
          </label>

          <p
            v-if="error"
            class="admin-error"
            role="alert"
          >
            {{ error }}
          </p>

          <button
            class="admin-primary admin-wide"
            :disabled="busy"
            type="submit"
          >
            <LockKeyhole :size="17" />
            Войти
          </button>
        </form>

        <NuxtLink to="/" class="admin-back">
          <ArrowLeft :size="15" />
          Вернуться на сайт
        </NuxtLink>
      </div>
    </div>

    <!-- Authenticated administration -->
    <div v-else class="admin-shell">
      <div
        v-if="mobileNav"
        class="admin-nav-shade"
        @click="mobileNav = false"
      ></div>

      <aside
        class="admin-sidebar"
        :class="{ 'admin-sidebar-open': mobileNav }"
      >
        <div class="admin-brand">
          <span class="admin-brand-mark">
            <Activity :size="21" />
          </span>

          <div>
            <strong>KoZove<span>.</span></strong>
            <small>ADMIN CONSOLE</small>
          </div>

          <button
            class="admin-nav-close"
            aria-label="Закрыть меню"
            @click="mobileNav = false"
          >
            <X :size="19" />
          </button>
        </div>

        <div class="admin-sidebar-scroll">
          <template
            v-for="(item, i) in items"
            :key="item.id"
          >
            <div
              v-if="
                i === 0 ||
                items[i - 1]?.group !== item.group
              "
              class="admin-nav-group"
            >
              {{ item.group }}
            </div>

            <button
              type="button"
              class="admin-nav-link"
              :class="{ active: active === item.id }"
              @click="section(item.id)"
            >
              <component
                :is="item.icon"
                :size="18"
              />

              <span>{{ item.name }}</span>

              <em
                v-if="
                  item.id === 'reviews' &&
                  summary?.reviews.pending
                "
              >
                {{ summary.reviews.pending }}
              </em>

              <em
                v-if="
                  item.id === 'reports' &&
                  summary?.reports.pending
                "
              >
                {{ summary.reports.pending }}
              </em>

              <em
                v-if="
                  item.id === 'appeals' &&
                  summary?.appeals.pending
                "
              >
                {{ summary.appeals.pending }}
              </em>
            </button>
          </template>
        </div>

        <div class="admin-sidebar-bottom">
          <div class="admin-account">
            <span>A</span>

            <div>
              <strong>Администратор</strong>
              <small>Единственный аккаунт</small>
            </div>
          </div>

          <button
            class="admin-logout"
            @click="logout"
          >
            <LogOut :size="17" />
            Выйти из панели
          </button>
        </div>
      </aside>

      <div class="admin-workspace">
        <!-- Top bar -->
        <header class="admin-topbar">
          <div class="admin-topbar-left">
            <button
              class="admin-mobile-toggle"
              aria-label="Открыть меню"
              @click="mobileNav = true"
            >
              <Menu :size="21" />
            </button>

            <span class="admin-breadcrumb">
              KoZove <span>/</span> {{ title }}
            </span>
          </div>

          <div class="admin-topbar-right">
            <span class="admin-live">
              <span></span>
              Администратор
            </span>

            <NuxtLink
              to="/"
              target="_blank"
              title="Открыть сайт"
            >
              <ExternalLink :size="18" />
            </NuxtLink>
          </div>
        </header>

        <main class="admin-main">
          <!-- Page heading -->
          <div class="admin-heading">
            <div>
              <p class="admin-kicker">
                УПРАВЛЕНИЕ СЕРВИСОМ
              </p>

              <h1>{{ title }}</h1>

              <p class="admin-lead">
                {{
                  active === 'overview'
                    ? 'Все важные события и состояние сервиса в одном месте.'
                    : active === 'settings'
                      ? 'Основные параметры работы и режима обслуживания.'
                      : 'Управляй записями, проверяй материалы и отслеживай изменения.'
                }}
              </p>
            </div>

            <div class="admin-heading-actions">
              <button
                class="admin-ghost"
                :disabled="refreshing"
                @click="reload"
              >
                <RefreshCw
                  :size="16"
                  :class="{
                    'admin-spin': refreshing
                  }"
                />
                Обновить
              </button>

              <button
                v-if="active === 'phones'"
                class="admin-primary"
                @click="createPhone"
              >
                <Plus :size="16" />
                Добавить номер
              </button>
            </div>
          </div>

          <!-- Notifications -->
          <div
            v-if="error"
            class="admin-alert admin-alert-error"
            role="alert"
          >
            <CircleAlert :size="18" />
            {{ error }}
          </div>

          <div
            v-if="notice"
            class="admin-alert admin-alert-success"
            role="status"
          >
            <CheckCircle2 :size="18" />
            {{ notice }}

            <button
              aria-label="Закрыть"
              @click="notice = ''"
            >
              <X :size="15" />
            </button>
          </div>

          <!-- Dashboard -->
          <template
            v-if="active === 'overview' && summary"
          >
            <div class="admin-stats">
              <button
                class="admin-stat"
                @click="section('phones')"
              >
                <span class="admin-stat-icon teal">
                  <Phone :size="21" />
                </span>

                <small>Номеров в базе</small>
                <strong>{{ summary.phones }}</strong>
                <span>
                  Справочник и пользовательские записи
                </span>
              </button>

              <button
                class="admin-stat"
                @click="section('reviews')"
              >
                <span class="admin-stat-icon amber">
                  <MessageSquareText :size="21" />
                </span>

                <small>Отзывы на проверке</small>

                <strong>
                  {{ summary.reviews.pending }}
                </strong>

                <span>
                  {{ summary.reviews.approved }}
                  опубликовано
                </span>
              </button>

              <button
                class="admin-stat"
                @click="section('reports')"
              >
                <span class="admin-stat-icon purple">
                  <ShieldAlert :size="21" />
                </span>

                <small>Жалобы на проверке</small>

                <strong>
                  {{ summary.reports.pending }}
                </strong>

                <span>
                  {{ summary.reports.approved }}
                  одобрено
                </span>
              </button>

              <button
                class="admin-stat"
                @click="section('appeals')"
              >
                <span class="admin-stat-icon blue">
                  <FileWarning :size="21" />
                </span>

                <small>Обращения</small>

                <strong>
                  {{ summary.appeals.pending }}
                </strong>

                <span>Требуют ответа</span>
              </button>
            </div>

            <div class="admin-overview-grid">
              <section class="admin-panel">
                <div class="admin-panel-head">
                  <div>
                    <h2>Очередь модерации</h2>
                    <p>
                      Последние отзывы, ожидающие решения
                    </p>
                  </div>

                  <button
                    class="admin-text-link"
                    @click="section('reviews')"
                  >
                    Все отзывы
                    <ArrowRight :size="16" />
                  </button>
                </div>

                <div
                  v-if="!summary.latest_reviews.length"
                  class="admin-empty"
                >
                  <CheckCircle2 :size="28" />
                  <strong>Очередь пуста</strong>
                  <span>
                    Новые отзывы появятся здесь.
                  </span>
                </div>

                <div
                  v-for="r in summary.latest_reviews"
                  :key="r.id"
                  class="admin-queue-row"
                >
                  <div>
                    <strong>{{ r.number }}</strong>
                    <p>{{ r.text }}</p>
                  </div>

                  <span class="admin-status pending">
                    На проверке
                  </span>
                </div>
              </section>

              <section class="admin-panel">
                <div class="admin-panel-head">
                  <div>
                    <h2>Состояние проекта</h2>
                    <p>Текущие рабочие параметры</p>
                  </div>
                </div>

                <div class="admin-system-line">
                  <span>
                    <Activity :size="17" />
                    Режим сайта
                  </span>

                  <span
                    class="admin-status"
                    :class="
                      summary.mode === 'normal'
                        ? 'approved'
                        : 'pending'
                    "
                  >
                    {{
                      summary.mode === 'normal'
                        ? 'Обычная работа'
                        : summary.mode === 'read_only'
                          ? 'Только чтение'
                          : 'Обслуживание'
                    }}
                  </span>
                </div>

                <div class="admin-system-line">
                  <span>
                    <ShieldCheck :size="17" />
                    Модерация
                  </span>
                  <strong>Ручная</strong>
                </div>

                <div class="admin-system-line">
                  <span>
                    <Globe2 :size="17" />
                    Страна
                  </span>
                  <strong>Черногория (+382)</strong>
                </div>

                <div class="admin-system-line">
                  <span>
                    <LockKeyhole :size="17" />
                    Доступ
                  </span>
                  <strong>Один администратор</strong>
                </div>

                <button
                  class="admin-ghost admin-wide"
                  @click="section('settings')"
                >
                  <Settings2 :size="17" />
                  Управление сайтом
                </button>
              </section>
            </div>
          </template>

          <!-- Paginated lists -->
          <template v-else-if="isList">
            <div class="admin-panel admin-list-panel">
              <div class="admin-filters">
                <form
                  class="admin-search"
                  @submit.prevent="doSearch"
                >
                  <Search :size="18" />

                  <input
                    v-model="searchText"
                    :placeholder="
                      active === 'audit'
                        ? 'Найти действие или объект...'
                        : 'Поиск по номеру или содержимому...'
                    "
                  />

                  <button type="submit">
                    Найти
                  </button>
                </form>

                <label
                  v-if="filters.length"
                  class="admin-filter-select"
                >
                  <Filter :size="17" />

                  <select
                    v-model="filter"
                    @change="changeFilter"
                  >
                    <option
                      v-for="opt in filters"
                      :key="opt[0]"
                      :value="opt[0]"
                    >
                      {{ opt[1] }}
                    </option>
                  </select>

                  <ChevronDown :size="15" />
                </label>
              </div>

              <div class="admin-list-meta">
                <span>
                  Найдено:
                  <strong>{{ pageData.total }}</strong>
                </span>

                <span>
                  Страница {{ pageData.page }}
                  из {{ pageData.pages }}
                </span>
              </div>

              <div
                v-if="!pageData.items.length"
                class="admin-empty"
              >
                <BookOpenCheck :size="29" />
                <strong>Ничего не найдено</strong>

                <span>
                  Попробуй изменить фильтр
                  или поисковый запрос.
                </span>
              </div>

              <div
                v-for="row in pageData.items"
                :key="row.id"
                class="admin-record"
              >
                <div class="admin-record-main">
                  <div class="admin-record-title">
                    <strong>
                      {{
                        active === 'audit'
                          ? `${row.action} · ${row.target_type}`
                          : row.number
                      }}
                    </strong>

                    <span
                      v-if="row.status"
                      class="admin-status"
                      :class="row.status"
                    >
                      {{ statusName(row.status) }}
                    </span>

                    <span
                      v-if="active === 'phones'"
                      class="admin-status"
                      :class="
                        row.is_listed
                          ? 'approved'
                          : 'neutral'
                      "
                    >
                      {{
                        row.is_listed
                          ? 'Организация'
                          : 'Без названия'
                      }}
                    </span>
                  </div>

                  <p
                    v-if="
                      active === 'reviews' ||
                      active === 'reports' ||
                      active === 'appeals'
                    "
                    class="admin-record-text"
                  >
                    {{
                      row.text ||
                      'Комментарий отсутствует'
                    }}
                  </p>

                  <p
                    v-else-if="active === 'phones'"
                    class="admin-record-text"
                  >
                    {{
                      row.business_name ||
                      'Название не установлено'
                    }}
                  </p>

                  <div class="admin-record-meta">
                    <span>#{{ row.id }}</span>

                    <span v-if="row.category">
                      {{ kindName(row.category) }}
                    </span>

                    <span v-if="row.rating">
                      ★ {{ row.rating }}/5
                    </span>

                    <span
                      v-if="row.risk_flags?.length"
                      class="admin-risk"
                    >
                      <ShieldAlert :size="13" />

                      {{
                        row.risk_flags.join(', ')
                      }}
                    </span>

                    <span v-if="row.created_at">
                      {{ displayDate(row.created_at) }}
                    </span>

                    <span v-if="row.target_id">
                      ID объекта:
                      {{ row.target_id }}
                    </span>
                  </div>
                </div>

                <div class="admin-record-actions">
                  <!-- Only pending reviews and reports -->
                  <template
                    v-if="
                      row.status === 'pending' &&
                      (
                        active === 'reviews' ||
                        active === 'reports'
                      )
                    "
                  >
                    <button
                      class="admin-approve"
                      :disabled="busy"
                      @click="decide(row, 'approved')"
                    >
                      <Check :size="16" />
                      Одобрить
                    </button>

                    <button
                      class="admin-reject"
                      :disabled="busy"
                      @click="decide(row, 'rejected')"
                    >
                      <X :size="16" />
                      Отклонить
                    </button>
                  </template>

                  <!-- Only pending appeals -->
                  <template
                    v-if="
                      row.status === 'pending' &&
                      active === 'appeals'
                    "
                  >
                    <button
                      class="admin-approve"
                      :disabled="busy"
                      @click="decide(row, 'resolved')"
                    >
                      <Check :size="16" />
                      Решено
                    </button>

                    <button
                      class="admin-reject"
                      :disabled="busy"
                      @click="decide(row, 'rejected')"
                    >
                      Отклонить
                    </button>
                  </template>

                  <button
                    v-if="active !== 'audit'"
                    class="admin-more"
                    :aria-label="
                      `Подробности записи ${row.id}`
                    "
                    @click="selected = { ...row }"
                  >
                    <MoreHorizontal :size="20" />
                  </button>
                </div>
              </div>

              <div
                v-if="pageData.total"
                class="admin-pagination"
              >
                <button
                  :disabled="page <= 1 || refreshing"
                  @click="move(page - 1)"
                >
                  <ArrowLeft :size="16" />
                  Назад
                </button>

                <span>
                  {{ page }} / {{ pageData.pages }}
                </span>

                <button
                  :disabled="
                    page >= pageData.pages ||
                    refreshing
                  "
                  @click="move(page + 1)"
                >
                  Дальше
                  <ArrowRight :size="16" />
                </button>
              </div>
            </div>
          </template>

          <!-- Website settings -->
          <template v-else-if="active === 'settings'">
            <div class="admin-settings-grid">
              <section class="admin-panel">
                <h2>Режим работы сайта</h2>

                <p class="admin-lead">
                  Выбирай режим с учётом доступности
                  новых публикаций.
                </p>

                <label class="admin-setting-choice">
                  <input
                    v-model="siteMode"
                    type="radio"
                    value="normal"
                  />

                  <span>
                    <strong>Обычная работа</strong>
                    <small>
                      Публичный поиск, отзывы
                      и жалобы доступны.
                    </small>
                  </span>
                </label>

                <label class="admin-setting-choice">
                  <input
                    v-model="siteMode"
                    type="radio"
                    value="read_only"
                  />

                  <span>
                    <strong>Только чтение</strong>
                    <small>
                      Публичные записи видны,
                      новые отзывы заблокированы.
                    </small>
                  </span>
                </label>

                <label class="admin-setting-choice">
                  <input
                    v-model="siteMode"
                    type="radio"
                    value="maintenance"
                  />

                  <span>
                    <strong>Техобслуживание</strong>
                    <small>
                      Поиск временно недоступен,
                      админка продолжает работать.
                    </small>
                  </span>
                </label>

                <button
                  class="admin-primary"
                  :disabled="busy"
                  @click="saveMode"
                >
                  <Check :size="17" />
                  Сохранить режим
                </button>
              </section>

              <section class="admin-panel">
                <h2>Конфигурация проекта</h2>

                <p class="admin-lead">
                  Эти значения заданы в конфигурации
                  и не изменяются из браузера.
                </p>

                <div class="admin-system-line">
                  <span>Версия приложения</span>
                  <strong>v{{ publicConfig.appVersion }}</strong>
                </div>

                <div class="admin-system-line">
                  <span>Регион поиска</span>
                  <strong>Черногория (+382)</strong>
                </div>

                <div class="admin-system-line">
                  <span>Модерация</span>
                  <strong>Ручная</strong>
                </div>

                <div class="admin-system-line">
                  <span>Публичная регистрация</span>
                  <strong>Выключена</strong>
                </div>

                <div class="admin-system-line">
                  <span>Администраторы</span>
                  <strong>1</strong>
                </div>

                <div class="admin-alert admin-alert-info">
                  <CircleAlert :size="17" />
                  Пароли, домен, ключи и лимиты
                  меняются в .env и backend,
                  не через публичные настройки.
                </div>
              </section>
            </div>
          </template>
        </main>
      </div>
    </div>

    <!-- Record details -->
    <div
      v-if="selected"
      class="admin-modal-layer"
      @click.self="selected = null"
    >
      <div
        class="admin-drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Детали записи"
      >
        <div class="admin-drawer-head">
          <div>
            <p class="admin-kicker">
              ПОДРОБНОСТИ
            </p>

            <h2>Запись #{{ selected.id }}</h2>
          </div>

          <button
            class="admin-more"
            aria-label="Закрыть"
            @click="selected = null"
          >
            <X :size="19" />
          </button>
        </div>

        <div class="admin-drawer-body">
          <div
            v-if="selected.number"
            class="admin-detail-line"
          >
            <small>Номер</small>
            <strong>{{ selected.number }}</strong>
          </div>

          <div
            v-if="selected.status"
            class="admin-detail-line"
          >
            <small>Статус</small>

            <span
              class="admin-status"
              :class="selected.status"
            >
              {{ statusName(selected.status) }}
            </span>
          </div>

          <div
            v-if="selected.category"
            class="admin-detail-line"
          >
            <small>Категория</small>
            <strong>
              {{ kindName(selected.category) }}
            </strong>
          </div>

          <div
            v-if="selected.rating"
            class="admin-detail-line"
          >
            <small>Оценка</small>
            <strong>
              ★ {{ selected.rating }}/5
            </strong>
          </div>

          <div
            v-if="selected.risk_flags?.length"
            class="admin-alert admin-alert-warn"
          >
            Проверить:
            {{ selected.risk_flags.join(', ') }}
          </div>

          <div
            v-if="selected.text"
            class="admin-detail-line"
          >
            <small>Содержимое</small>
            <p>{{ selected.text }}</p>
          </div>

          <div
            v-if="active === 'phones'"
            class="admin-detail-line"
          >
            <small>Организация</small>
            <p>
              {{
                selected.business_name ||
                'Не указана'
              }}
            </p>

            <small>Источник</small>
            <p>
              {{
                selected.source_url ||
                'Не указан'
              }}
            </p>
          </div>

          <div
            v-if="selected.contact_email"
            class="admin-detail-line"
          >
            <small>
              Контакт заявителя (не публикуется)
            </small>

            <strong>
              {{ selected.contact_email }}
            </strong>
          </div>

          <div
            v-if="selected.created_at"
            class="admin-detail-line"
          >
            <small>Создано</small>
            <strong>
              {{ displayDate(selected.created_at) }}
            </strong>
          </div>
        </div>

        <div class="admin-drawer-footer">
          <button
            v-if="active === 'phones'"
            class="admin-primary"
            @click="editPhone(selected)"
          >
            <Settings2 :size="16" />
            Редактировать
          </button>

          <button
            class="admin-danger"
            :disabled="busy"
            @click="removeSelected"
          >
            <Trash2 :size="16" />
            Удалить запись
          </button>
        </div>
      </div>
    </div>

    <!-- Phone editor -->
    <div
      v-if="phoneEditor"
      class="admin-modal-layer"
      @click.self="phoneEditor = false"
    >
      <form
        class="admin-drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Редактор номера"
        @submit.prevent="savePhone"
      >
        <div class="admin-drawer-head">
          <div>
            <p class="admin-kicker">
              СПРАВОЧНИК
            </p>

            <h2>
              {{
                phoneEditorId
                  ? 'Редактирование'
                  : 'Новый номер'
              }}
            </h2>
          </div>

          <button
            type="button"
            class="admin-more"
            aria-label="Закрыть"
            @click="phoneEditor = false"
          >
            <X :size="19" />
          </button>
        </div>

        <div class="admin-drawer-body">
          <label class="admin-field">
            Номер +382

            <input
              v-model="phoneForm.number"
              class="admin-input"
              placeholder="+382 6X XXX XXX"
              :readonly="!!phoneEditorId"
              required
            />
          </label>

          <label class="admin-field">
            Название организации

            <input
              v-model="phoneForm.business_name"
              class="admin-input"
              maxlength="120"
              placeholder="Только подтверждённая организация"
            />
          </label>

          <label class="admin-field">
            Официальный источник HTTPS

            <input
              v-model="phoneForm.source_url"
              class="admin-input"
              type="url"
              maxlength="500"
              placeholder="https://example.org/contact"
            />
          </label>

          <p class="admin-muted">
            Название и официальный источник
            должны быть указаны вместе.
            Без них номер сохраняется как неизвестный.
          </p>
        </div>

        <div class="admin-drawer-footer">
          <button
            type="button"
            class="admin-ghost"
            @click="phoneEditor = false"
          >
            Отмена
          </button>

          <button
            type="submit"
            class="admin-primary"
            :disabled="busy"
          >
            <Check :size="16" />
            Сохранить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style src="../assets/css/admin.css"></style>
