
import {
  getRequestURL,
  getRequestIP,
  proxyRequest,
  createError
} from 'h3'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const url = getRequestURL(event)
  const upstream = new URL(config.apiInternalUrl)

  if (!url.pathname.startsWith('/api/v1/')) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Not found'
    })
  }

  const target =
    upstream.origin +
    url.pathname +
    url.search

  try {
    if (!config.proxySharedSecret) {
      throw createError({
        statusCode: 500,
        statusMessage: 'Proxy is not configured'
      })
    }

    const ip = getRequestIP(event, {
      xForwardedFor: false
    }) || ''

    return await proxyRequest(event, target, {
      headers: {
        'x-kozove-client-ip': ip,
        'x-kozove-proxy-secret':
          config.proxySharedSecret
      }
    })
  } catch (error: any) {
    if (error?.statusCode) {
      throw error
    }

    console.error(
      '[KoZove API] Upstream unavailable:',
      error?.message
    )

    throw createError({
      statusCode: 502,
      statusMessage:
        'API is temporarily unavailable'
    })
  }
})
