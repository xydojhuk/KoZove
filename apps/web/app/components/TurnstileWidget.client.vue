<script setup lang="ts">
const props = defineProps<{
  sitekey: string
}>()

const emit = defineEmits<{
  (e: 'token', token: string): void
}>()

const target = ref<HTMLElement | null>(null)

let widgetId: string | undefined

function renderWidget() {
  const turnstile = (window as any).turnstile

  if (!turnstile || !target.value || widgetId) return

  widgetId = turnstile.render(target.value, {
    sitekey: props.sitekey,

    callback: (token: string) => {
      emit('token', token)
    },

    'expired-callback': () => {
      emit('token', '')
    },

    'error-callback': () => {
      emit('token', '')
    }
  })
}

onMounted(() => {
  if ((window as any).turnstile) {
    renderWidget()
    return
  }

  let script = document.querySelector<HTMLScriptElement>(
    'script[data-kozove-turnstile]'
  )

  if (!script) {
    script = document.createElement('script')
    script.src =
      'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'

    script.async = true
    script.dataset.kozoveTurnstile = '1'
    document.head.appendChild(script)
  }

  script.addEventListener('load', renderWidget, {
    once: true
  })
})

onBeforeUnmount(() => {
  const turnstile = (window as any).turnstile

  if (turnstile && widgetId) {
    turnstile.remove(widgetId)
  }

  emit('token', '')
})
</script>

<template>
  <div ref="target"></div>
</template>