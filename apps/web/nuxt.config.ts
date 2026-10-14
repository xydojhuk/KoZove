export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',

  modules: [
    '@nuxt/fonts'
  ],

  devtools: {
    enabled: true
  },

  css: [
    '~/assets/css/main.css'
  ],

  fonts: {
    families: [
      {
        name: 'Montserrat',
        provider: 'google',
        global: true,
        weights: [
          '400', '500', '600', '700', '800'
        ]
      }
    ]
  },

  runtimeConfig: {
    proxySharedSecret:
      process.env.NUXT_PROXY_SHARED_SECRET || '',

    apiInternalUrl:
      process.env.NUXT_API_INTERNAL_URL ||
      'http://api:8000',

    public: {
      appVersion:
        process.env.NUXT_PUBLIC_APP_VERSION ||
        'development',

      turnstileSitekey:
        process.env.NUXT_PUBLIC_TURNSTILE_SITEKEY || '',

      githubUrl:
        process.env.NUXT_PUBLIC_GITHUB_URL || '',

      contactEmail:
        process.env.NUXT_PUBLIC_CONTACT_EMAIL || ''
    }
  },

  app: {
    head: {
      title: 'KoZove — Ko te zove?',
      link: [
        {
          rel: 'icon',
          type: 'image/svg+xml',
          href: '/favicon.svg'
        }
      ],
      meta: [
        {
          name: 'description',
          content:
            'Provjeri nepoznate brojeve u Crnoj Gori. '
            + 'Iskustva korisnika, ocjene i prijave poziva.'
        },
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1'
        },
        {
          name: 'theme-color',
          content: '#f8fafc'
        }
      ],
    }
  }
})