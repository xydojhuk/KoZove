
<script setup lang="ts">
import {
  X,
  ArrowUpRight,
  ShieldCheck,
  HeartHandshake,
  Code2,
  Globe2
} from '@lucide/vue'

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{ (e: 'close'): void }>()

const { c } = useSiteCopy()
const config = useRuntimeConfig()

const closeButton = ref<HTMLButtonElement | null>(null)
const dialog = ref<HTMLElement | null>(null)

let previousOverflow = ''
let previouslyFocused: HTMLElement | null = null

function close() {
  emit('close')
}

function onKeydown(event: KeyboardEvent) {
  if (!props.open) return

  if (event.key === 'Escape') {
    event.preventDefault()
    close()
    return
  }

  if (event.key !== 'Tab' || !dialog.value) return

  const focusable = Array.from(
    dialog.value.querySelectorAll<HTMLElement>(
      'a[href], button:not([disabled]), select:not([disabled]), ' +
      'input:not([disabled]), textarea:not([disabled]), ' +
      '[tabindex]:not([tabindex="-1"])'
    )
  )

  if (focusable.length === 0) {
    event.preventDefault()
    dialog.value.focus()
    return
  }

  const first = focusable[0]!
  const last = focusable[focusable.length - 1]!

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last.focus()
  } else if (
    !event.shiftKey &&
    document.activeElement === last
  ) {
    event.preventDefault()
    first.focus()
  }
}

watch(
  () => props.open,
  async (isOpen) => {
    if (!import.meta.client) return

    if (isOpen) {
      previousOverflow = document.body.style.overflow
      previouslyFocused =
        document.activeElement as HTMLElement | null

      document.body.style.overflow = 'hidden'

      await nextTick()
      closeButton.value?.focus()
    } else {
      document.body.style.overflow = previousOverflow
      previouslyFocused?.focus()
      previouslyFocused = null
    }
  }
)

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = previousOverflow
})
</script>

<template>
  <Transition name="project-modal">
    <div
      v-if="open"
      class="project-overlay"
      @click.self="close"
    >
      <section
        ref="dialog"
        class="project-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="project-dialog-title"
        tabindex="-1"
      >
        <button
          ref="closeButton"
          class="project-dialog-close"
          type="button"
          :aria-label="c.modalClose"
          @click="close"
        >
          <X :size="20" />
        </button>

        <div class="dialog-emblem">
          <Code2 :size="27" :stroke-width="1.7" />
        </div>

        <span class="dialog-eyebrow">
          {{ c.modalEyebrow }}
        </span>

        <h2 id="project-dialog-title">
          {{ c.modalTitle }}
        </h2>

        <p class="dialog-description">
          {{ c.modalDescription }}
        </p>

        <p class="dialog-open-source">
          {{ c.modalWhy }}
        </p>

        <div class="dialog-support">
          <div class="dialog-support-heading">
            <HeartHandshake :size="22" />
            <h3>{{ c.modalSupportTitle }}</h3>
          </div>

          <p>{{ c.modalSupportText }}</p>

          <div class="dialog-actions">
            <a
              v-if="config.public.githubUrl"
              :href="config.public.githubUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="button button-primary"
            >
              <Code2 :size="18" />
              {{ c.modalGithub }}
              <ArrowUpRight :size="16" />
            </a>

            <button
              class="button button-soft"
              disabled
              type="button"
            >
              <HeartHandshake :size="18" />
              {{ c.modalDonate }}
            </button>
          </div>
        </div>
      </section>
    </div>
  </Transition>
</template>
