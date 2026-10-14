<script setup lang="ts">
const { locale } = useLocale()
const config = useRuntimeConfig()

interface LegalSection {
  heading: string
  paragraphs: string[]
  bullets: string[]
}
interface LegalPage {
  title: string
  updated: string
  intro: string
  contactTitle: string
  contactLine: string
  contactMissing: string
  sections: LegalSection[]
}
type Language = 'sr' | 'ru' | 'en'

const pages: Record<Language, LegalPage> = {
  "ru": {
    "title": "Правила использования",
    "updated": "Обновлено: 14 октября 2026 года",
    "intro": "KoZove — открытый сервис отзывов о телефонных номерах Черногории. Пользуйтесь поиском бесплатно, делитесь только собственным опытом и уважайте частную жизнь других людей.",
    "contactTitle": "Обратная связь",
    "contactLine": "Если заметили ошибку, незаконный материал или публикацию о себе, воспользуйтесь формой оспаривания на странице номера либо напишите нам.",
    "contactMissing": "Контактный адрес указывается при настройке сервиса.",
    "sections": [
      {
        "heading": "1. Назначение сервиса",
        "paragraphs": [
          "На сайте можно искать номера с кодом +382, читать отзывы, оставлять оценки и сообщения о нежелательных звонках. Регистрация публичного аккаунта не требуется.",
          "Материалы пользователей выражают их личное мнение и опыт. Мы не подтверждаем личность частного абонента и не утверждаем, что номер связан с мошенничеством или иным правонарушением."
        ],
        "bullets": []
      },
      {
        "heading": "2. Правила публикации",
        "paragraphs": [
          "Отправляйте сведения добросовестно и только если имеете право ими делиться. Описывайте произошедшее спокойно и конкретно.",
          "Не публикуйте следующие материалы:"
        ],
        "bullets": [
          "ФИО, домашние адреса, чужие email, личные контакты и другие данные, раскрывающие частную личность.",
          "Угрозы, оскорбления, травлю, дискриминацию и призывы к насилию.",
          "Заведомо ложные обвинения, вымогательство, рекламу, спам и автоматические массовые публикации.",
          "Пароли, коды подтверждения, токены и другую конфиденциальную информацию."
        ]
      },
      {
        "heading": "3. Модерация",
        "paragraphs": [
          "Отзывы и жалобы поступают на предварительную модерацию. Мы можем отклонить, скрыть, исправить технические ошибки либо удалить материал, если он нарушает правила, права других людей или требования закона.",
          "Одобрение публикации не означает подтверждения её достоверности. Администрация может ограничивать отправку материалов для предотвращения злоупотреблений."
        ],
        "bullets": []
      },
      {
        "heading": "4. Права на материалы",
        "paragraphs": [
          "Вы сохраняете права на свой текст. Отправляя его, разрешаете KoZove хранить, проверять и показывать материал на сайте в пределах, необходимых для работы сервиса и модерации.",
          "Не отправляйте текст или изображения, на публикацию которых у вас нет необходимых прав."
        ],
        "bullets": []
      },
      {
        "heading": "5. Исправления и жалобы",
        "paragraphs": [
          "Если информация о номере неточна, раскрывает персональные данные или затрагивает ваши права, используйте форму оспаривания либо контактный email. Укажите материал и основание обращения.",
          "Мы проверяем такие запросы и можем попросить сведения, подтверждающие обоснованность исправления или удаления."
        ],
        "bullets": []
      },
      {
        "heading": "6. Работа сервиса",
        "paragraphs": [
          "Мы стараемся обеспечивать доступность и аккуратную модерацию, но не гарантируем непрерывную работу сайта, полноту или достоверность каждого пользовательского сообщения.",
          "Не используйте информацию с сайта как единственное основание для обвинений, платежей или решений, затрагивающих права других людей. Ответственность и права сторон определяются применимым законодательством."
        ],
        "bullets": []
      },
      {
        "heading": "7. Изменения правил",
        "paragraphs": [
          "Мы можем обновлять эти правила по мере развития сервиса. Дата последней редакции указана вверху страницы."
        ],
        "bullets": []
      }
    ]
  },
  "en": {
    "title": "Terms of Use",
    "updated": "Last updated: 14 October 2026",
    "intro": "KoZove is a community-powered resource for Montenegro phone numbers. Search for free, share your own experiences and respect other people’s privacy.",
    "contactTitle": "Questions or concerns",
    "contactLine": "If you see an error, unlawful content or information about yourself, use the dispute form on that number page or contact us.",
    "contactMissing": "The contact address is set by the site operator.",
    "sections": [
      {
        "heading": "1. What KoZove provides",
        "paragraphs": [
          "Visitors can search +382 numbers, read reviews, leave ratings and report unwanted calls. No public account is required.",
          "Submissions are users’ opinions and experiences. KoZove does not verify the identity of private subscribers or certify that a number is connected to fraud or other wrongdoing."
        ],
        "bullets": []
      },
      {
        "heading": "2. Posting responsibly",
        "paragraphs": [
          "Share information in good faith and only when you are entitled to share it. Describe your experience clearly and fairly.",
          "Do not submit:"
        ],
        "bullets": [
          "Private individuals’ names, home addresses, third-party email addresses or other identifying personal information.",
          "Threats, harassment, discriminatory attacks or calls for violence.",
          "Knowingly false accusations, extortion, advertising, spam or automated bulk submissions.",
          "Passwords, verification codes, access tokens or other confidential information."
        ]
      },
      {
        "heading": "3. Moderation",
        "paragraphs": [
          "Reviews and call reports are screened before publication. We may reject, hide, correct technical errors in or remove content that breaches these rules, the rights of others or applicable law.",
          "Approval does not mean that a statement has been independently verified. We may restrict submissions to prevent misuse."
        ],
        "bullets": []
      },
      {
        "heading": "4. Rights to your content",
        "paragraphs": [
          "You retain rights to your own words. By submitting content, you allow KoZove to store, review and display it as needed to operate the service and moderate contributions.",
          "Do not submit material you lack permission to publish."
        ],
        "bullets": []
      },
      {
        "heading": "5. Corrections and complaints",
        "paragraphs": [
          "If a number page is inaccurate, exposes personal data or otherwise affects your rights, use its dispute form or contact email. Identify the content and explain your concern.",
          "We review requests and may ask for information supporting a correction or removal."
        ],
        "bullets": []
      },
      {
        "heading": "6. Service availability and reliance",
        "paragraphs": [
          "We aim to keep the website useful and available, but cannot guarantee uninterrupted access, complete coverage or the accuracy of every user submission.",
          "Do not rely on a KoZove report alone to accuse someone, make payments or take actions that affect another person’s rights. Any responsibility is subject to applicable law."
        ],
        "bullets": []
      },
      {
        "heading": "7. Updates",
        "paragraphs": [
          "These terms may change as KoZove evolves. The latest revision date is shown at the top of this page."
        ],
        "bullets": []
      }
    ]
  },
  "sr": {
    "title": "Uslovi korišćenja",
    "updated": "Posljednja izmjena: 14. oktobar 2026.",
    "intro": "KoZove je servis za razmjenu iskustava o telefonskim brojevima u Crnoj Gori. Pretražujte besplatno, dijelite sopstvena iskustva i poštujte privatnost drugih.",
    "contactTitle": "Pitanja i primjedbe",
    "contactLine": "Ako primijetite grešku, nezakonit sadržaj ili podatak o sebi, koristite obrazac za osporavanje na stranici broja ili nam pišite.",
    "contactMissing": "Kontakt adresu određuje rukovalac prilikom podešavanja sajta.",
    "sections": [
      {
        "heading": "1. Čemu služi KoZove",
        "paragraphs": [
          "Možete pretraživati brojeve sa pozivnim brojem +382, čitati komentare, ostavljati ocjene i prijavljivati neželjene pozive. Javni korisnički nalog nije potreban.",
          "Objave predstavljaju mišljenja i iskustva korisnika. KoZove ne potvrđuje identitet privatnih pretplatnika niti utvrđuje da je određeni broj povezan s prevarom ili drugim nezakonitim radnjama."
        ],
        "bullets": []
      },
      {
        "heading": "2. Pravila objavljivanja",
        "paragraphs": [
          "Dijelite informacije savjesno i samo ako imate pravo da ih objavite. Iskustvo opišite jasno i odmjereno.",
          "Zabranjeno je objavljivati:"
        ],
        "bullets": [
          "Imena i prezimena privatnih lica, kućne adrese, tuđe email adrese i druge podatke koji otkrivaju identitet.",
          "Prijetnje, uznemiravanje, diskriminatorne napade i pozive na nasilje.",
          "Svjesno neistinite optužbe, ucjene, reklame, spam i automatsko masovno slanje sadržaja.",
          "Lozinke, kodove za potvrdu, pristupne tokene i druge povjerljive informacije."
        ]
      },
      {
        "heading": "3. Moderacija",
        "paragraphs": [
          "Komentari i prijave prolaze provjeru prije objavljivanja. Možemo odbiti, sakriti, ispraviti tehničke greške ili ukloniti sadržaj koji krši pravila, prava drugih ili zakon.",
          "Odobrenje ne znači da je navod nezavisno potvrđen. Možemo ograničiti slanje sadržaja radi sprečavanja zloupotreba."
        ],
        "bullets": []
      },
      {
        "heading": "4. Prava na sadržaj",
        "paragraphs": [
          "Zadržavate prava na sopstveni tekst. Slanjem sadržaja dozvoljavate KoZove da ga čuva, provjerava i prikazuje u mjeri potrebnoj za rad sajta i moderaciju.",
          "Nemojte slati materijal za koji nemate pravo objavljivanja."
        ],
        "bullets": []
      },
      {
        "heading": "5. Ispravke i prigovori",
        "paragraphs": [
          "Ako su podaci netačni, otkrivaju privatne informacije ili utiču na vaša prava, koristite obrazac za osporavanje ili kontakt email. Navedite sadržaj i razlog zahtjeva.",
          "Zahtjev ćemo razmotriti i po potrebi zatražiti dodatne podatke koji potvrđuju osnov za ispravku ili uklanjanje."
        ],
        "bullets": []
      },
      {
        "heading": "6. Dostupnost i pouzdanost",
        "paragraphs": [
          "Nastojimo da sajt bude dostupan i koristan, ali ne možemo garantovati neprekidan rad, potpunost baze ili tačnost svakog korisničkog navoda.",
          "Nemojte se oslanjati samo na prijavu sa KoZove prilikom optuživanja drugih, plaćanja ili donošenja odluka koje utiču na njihova prava. Odgovornost se određuje prema primjenjivom zakonu."
        ],
        "bullets": []
      },
      {
        "heading": "7. Izmjene",
        "paragraphs": [
          "Ove uslove možemo ažurirati kako se servis razvija. Datum posljednje izmjene naveden je na početku stranice."
        ],
        "bullets": []
      }
    ]
  }
}
const content = computed(() => pages[locale.value as Language] ?? pages.sr)

useSeoMeta({
  title: () => `KoZove · ${content.value.title}`,
  description: () => content.value.intro,
  robots: 'noindex,follow'
})
</script>

<template>
  <main class="content-page">
    <article class="container legal-container">
      <h1 class="page-title">{{ content.title }}</h1>
      <p class="legal-updated">{{ content.updated }}</p>

      <div class="page-card legal-card">
        <p class="legal-intro">{{ content.intro }}</p>

        <section
          v-for="section in content.sections"
          :key="section.heading"
          class="legal-section"
        >
          <h2>{{ section.heading }}</h2>
          <p v-for="paragraph in section.paragraphs" :key="paragraph">
            {{ paragraph }}
          </p>
          <ul v-if="section.bullets.length">
            <li v-for="bullet in section.bullets" :key="bullet">
              {{ bullet }}
            </li>
          </ul>
        </section>

        <section class="legal-section legal-contact">
          <h2>{{ content.contactTitle }}</h2>
          <p>{{ content.contactLine }}</p>
          <p v-if="config.public.contactEmail">
            <a
              class="source-link"
              :href="`mailto:${config.public.contactEmail}`"
            >{{ config.public.contactEmail }}</a>
          </p>
          <p v-else>{{ content.contactMissing }}</p>
        </section>
      </div>
    </article>
  </main>
</template>

<style scoped>
.legal-container { max-width: 860px; }
.legal-updated { color: #64748b; margin: 4px 0 22px; font-size: 0.9rem; }
.legal-card { display: grid; gap: 25px; padding: clamp(22px, 4vw, 42px); }
.legal-intro { font-size: 1.05rem; line-height: 1.8; color: #334155; margin: 0; }
.legal-section { display: grid; gap: 10px; }
.legal-section h2 { color: #0f172a; font-size: 1.14rem; line-height: 1.4; margin: 0 0 4px; }
.legal-section p, .legal-section li { line-height: 1.78; color: #475569; margin: 0; }
.legal-section ul { margin: 0; padding-left: 23px; display: grid; gap: 6px; }
.legal-contact { padding-top: 22px; border-top: 1px solid #e2e8f0; }
.source-link { overflow-wrap: anywhere; }
</style>
