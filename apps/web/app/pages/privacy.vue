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
    "title": "Политика конфиденциальности",
    "updated": "Обновлено: 14 октября 2026 года",
    "intro": "KoZove помогает находить отзывы о телефонных номерах Черногории (+382). Ниже объясняем, какие данные нужны для работы сайта, что становится публичным и как обратиться по поводу опубликованной информации.",
    "contactTitle": "Связаться с нами",
    "contactLine": "По вопросам персональных данных, исправления и удаления информации можно написать на контактный адрес или воспользоваться формой оспаривания на странице номера.",
    "contactMissing": "Контактный адрес указан владельцем сайта при настройке сервиса.",
    "sections": [
      {
        "heading": "1. Какие данные мы обрабатываем",
        "paragraphs": [
          "При поиске используется введённый номер телефона. Создавать аккаунт для просмотра карточек и отправки материалов не требуется.",
          "В отзыве сохраняются номер, оценка, категория, текст, время отправки и результат модерации. В жалобе — номер, категория, текст (если указан), время и статус проверки.",
          "В обращении об исправлении или удалении сохраняются номер, текст обращения, при наличии — идентификатор отзыва и указанный вами email. Email не публикуется.",
          "Для борьбы со спамом создаётся технический отпечаток на основе IP-адреса и User-Agent с использованием серверного секретного ключа. Отпечаток привязывается к отзывам и жалобам, а отдельные события ограничений хранятся непродолжительное время.",
          "Действия администратора, журнал модерации и сессии администратора также обрабатываются для управления сервисом. Хостинг может обрабатывать сетевые данные и журналы доступа."
        ],
        "bullets": []
      },
      {
        "heading": "2. Зачем нужны данные",
        "paragraphs": [
          "Чтобы показывать результаты поиска, принимать отзывы и жалобы, проверять публикации, рассматривать обращения, предотвращать массовые отправки и обеспечивать безопасность сайта.",
          "Мы не создаём публичную базу личностей частных абонентов и не импортируем чужие телефонные книги."
        ],
        "bullets": []
      },
      {
        "heading": "3. Что видят другие посетители",
        "paragraphs": [
          "После одобрения модератором могут отображаться телефонный номер, категория и текст отзыва, оценка и дата публикации, а также количество одобренных жалоб.",
          "Для организаций могут показываться название и ссылка на публичный проверяемый источник. Контактный email из обращения, технический отпечаток и административный журнал посетителям не показываются.",
          "Отзывы описывают личный опыт пользователей. Они не подтверждают личность владельца номера и не доказывают нарушение закона."
        ],
        "bullets": []
      },
      {
        "heading": "4. Cookies и внешние сервисы",
        "paragraphs": [
          "Cookie kozove_locale сохраняет выбранный язык. Cookie kozove_admin используется только после входа администратора и позволяет поддерживать защищённую сессию.",
          "Для защиты публичных форм используется Cloudflare Turnstile. При проверке Cloudflare может обрабатывать необходимые технические данные согласно собственным правилам.",
          "В исходной версии проекта нет собственной рекламной сети или подключённой системы аналитики посещений. Оператор хостинга и поставщики сетевой инфраструктуры могут вести технические журналы."
        ],
        "bullets": []
      },
      {
        "heading": "5. Как долго хранятся данные",
        "paragraphs": [
          "Отдельные антиспам-события удаляются командой обслуживания через 48 часов; эту команду необходимо запускать регулярно. Сессии администратора действуют до 24 часов и удаляются после истечения срока при обслуживании.",
          "Отпечатки, прикреплённые к отзывам и жалобам, хранятся вместе с соответствующими материалами до их удаления. Публичные материалы, обращения и журнал административных действий сейчас не имеют автоматического срока удаления: их удаление выполняется вручную по результатам проверки.",
          "Фактический срок хранения сетевых журналов зависит от используемого хостинга."
        ],
        "bullets": []
      },
      {
        "heading": "6. Исправление, удаление и защита прав",
        "paragraphs": [
          "Если публикация содержит ошибку, личные данные или иной проблемный материал, используйте форму оспаривания на странице номера либо контактный email. По возможности укажите номер, ссылку на материал и причину обращения.",
          "Мы рассматриваем обращения и можем исправить, скрыть или удалить информацию после проверки. Для предотвращения удаления чужих материалов может потребоваться дополнительное подтверждение обстоятельств.",
          "Права на доступ, исправление, удаление и обращение в компетентный орган реализуются в пределах применимого законодательства."
        ],
        "bullets": []
      },
      {
        "heading": "7. Изменения политики",
        "paragraphs": [
          "При изменении работы сервиса, поставщиков или правил хранения мы обновим эту страницу и укажем дату последнего изменения."
        ],
        "bullets": []
      }
    ]
  },
  "en": {
    "title": "Privacy Policy",
    "updated": "Last updated: 14 October 2026",
    "intro": "KoZove helps people check community reviews of Montenegro (+382) phone numbers. This policy explains what information the service processes, what becomes public and how to request a correction or removal.",
    "contactTitle": "Contact us",
    "contactLine": "For privacy questions and correction or removal requests, contact the address below or use the dispute form on the relevant number page.",
    "contactMissing": "The contact address is supplied by the site operator when configuring the service.",
    "sections": [
      {
        "heading": "1. Information we handle",
        "paragraphs": [
          "A phone number entered in search is used to retrieve a result. Visitors do not need an account to search or submit content.",
          "For reviews, we store the phone number, rating, category, text, submission time and moderation status. For call reports, we store the number, category, optional text, time and moderation status.",
          "A correction or removal request contains the number, request text, any referenced review ID and any email address you choose to provide. That email address is not published.",
          "To reduce spam, the service derives a technical fingerprint from the IP address and User-Agent using a secret server key. The fingerprint is attached to reviews and reports; separate rate-limit events are stored for a shorter period.",
          "Administrative sessions and moderation activity are processed to manage the service. Hosting providers may also process network information and access logs."
        ],
        "bullets": []
      },
      {
        "heading": "2. Why we use it",
        "paragraphs": [
          "We use this information to return search results, accept and moderate submissions, respond to disputes, prevent abusive traffic and maintain site security.",
          "KoZove does not run a public directory of private subscribers’ identities and does not import private contact books."
        ],
        "bullets": []
      },
      {
        "heading": "3. What other visitors can see",
        "paragraphs": [
          "Once approved, a review may display the phone number, review category and text, rating and publication date. The number page may also show the count of approved call reports.",
          "A business name and a link to a verifiable public source may appear for an organization. Dispute email addresses, technical fingerprints and administrative logs are not shown publicly.",
          "Reviews describe individual experiences. They do not verify who owns a number or establish that any person committed an offence."
        ],
        "bullets": []
      },
      {
        "heading": "4. Cookies and third parties",
        "paragraphs": [
          "The kozove_locale cookie remembers your language choice. The kozove_admin cookie is used only for an administrator session after sign-in.",
          "Public submission forms use Cloudflare Turnstile for bot protection. Cloudflare may process technical information needed to perform its verification, under its own terms and policies.",
          "This version of KoZove does not contain a first-party advertising network or a configured visitor analytics system. Hosting and network providers may maintain technical logs."
        ],
        "bullets": []
      },
      {
        "heading": "5. Retention",
        "paragraphs": [
          "Separate anti-abuse events are deleted after 48 hours when the maintenance command runs; the operator must schedule that command. Administrator sessions expire after 24 hours and are removed by cleanup once expired.",
          "Fingerprints attached to reviews and reports remain with those records until removal. Public submissions, disputes and administrative audit records currently have no automatic deletion deadline and are removed manually after review.",
          "The retention period for network logs depends on the hosting provider."
        ],
        "bullets": []
      },
      {
        "heading": "6. Corrections, removal and your rights",
        "paragraphs": [
          "If a page includes inaccurate information, personal details or otherwise problematic content, use the dispute form on that number’s page or email us. Please include the number, a link to the material and your reason.",
          "We review requests and may correct, hide or remove material after checking the circumstances. Additional evidence may be needed to protect against wrongful removal.",
          "Requests for access, rectification, erasure and complaints to a relevant supervisory authority are handled in accordance with applicable law."
        ],
        "bullets": []
      },
      {
        "heading": "7. Updates to this policy",
        "paragraphs": [
          "We update this page if the service, its providers or retention practices change, and we show the date of the latest revision."
        ],
        "bullets": []
      }
    ]
  },
  "sr": {
    "title": "Politika privatnosti",
    "updated": "Posljednja izmjena: 14. oktobar 2026.",
    "intro": "KoZove omogućava pretragu korisničkih iskustava o telefonskim brojevima u Crnoj Gori (+382). Ovdje objašnjavamo koje podatke obrađujemo, šta je javno dostupno i kako možete zatražiti ispravku ili uklanjanje sadržaja.",
    "contactTitle": "Kontakt",
    "contactLine": "Za pitanja o privatnosti i zahtjeve za ispravku ili uklanjanje podataka pišite na navedenu adresu ili koristite obrazac za osporavanje na stranici broja.",
    "contactMissing": "Kontakt adresu određuje rukovalac prilikom podešavanja sajta.",
    "sections": [
      {
        "heading": "1. Koje podatke obrađujemo",
        "paragraphs": [
          "Broj koji unesete u pretragu koristi se za prikaz rezultata. Registracija nije potrebna za pretragu ili slanje sadržaja.",
          "Uz komentar čuvamo broj telefona, ocjenu, kategoriju, tekst, vrijeme slanja i status moderacije. Uz prijavu poziva čuvamo broj, kategoriju, tekst ako je unesen, vrijeme slanja i status.",
          "Zahtjev za ispravku ili uklanjanje sadrži broj, tekst zahtjeva, eventualni ID komentara i email adresu ako je sami navedete. Email se ne objavljuje.",
          "Radi ograničavanja zloupotreba kreiramo tehnički otisak na osnovu IP adrese i User-Agent podatka, uz tajni ključ servera. Otisak se vezuje za komentare i prijave; posebni događaji ograničavanja zahtjeva čuvaju se kraće.",
          "Administratorske sesije i aktivnosti moderacije obrađuju se radi upravljanja servisom. Pružalac hostinga može obrađivati mrežne podatke i pristupne zapise."
        ],
        "bullets": []
      },
      {
        "heading": "2. Zašto koristimo podatke",
        "paragraphs": [
          "Podaci su potrebni za rezultate pretrage, prijem i moderaciju sadržaja, obradu zahtjeva, sprečavanje masovnih prijava i zaštitu sajta.",
          "KoZove ne vodi javni imenik identiteta privatnih pretplatnika i ne uvozi privatne imenike kontakata."
        ],
        "bullets": []
      },
      {
        "heading": "3. Šta je javno vidljivo",
        "paragraphs": [
          "Nakon odobrenja mogu biti prikazani broj telefona, kategorija i tekst komentara, ocjena, datum objave i broj odobrenih prijava poziva.",
          "Za organizacije se mogu prikazati naziv i veza ka provjerljivom javnom izvoru. Email iz zahtjeva, tehnički otisak i administratorski zapisi nijesu javni.",
          "Komentari su lična iskustva korisnika. Oni ne potvrđuju identitet vlasnika broja niti dokazuju protivpravno postupanje."
        ],
        "bullets": []
      },
      {
        "heading": "4. Kolačići i spoljne usluge",
        "paragraphs": [
          "Kolačić kozove_locale pamti izabrani jezik. Kolačić kozove_admin koristi se samo za administratorsku sesiju nakon prijave.",
          "Za zaštitu obrazaca koristimo Cloudflare Turnstile. Cloudflare može obrađivati tehničke podatke potrebne za provjeru, prema sopstvenim pravilima.",
          "Ova verzija nema sopstvenu oglasnu mrežu niti podešen sistem analitike posjeta. Hosting i mrežni pružaoci usluga mogu voditi tehničke zapise."
        ],
        "bullets": []
      },
      {
        "heading": "5. Koliko dugo čuvamo podatke",
        "paragraphs": [
          "Posebni događaji zaštite od zloupotrebe brišu se nakon 48 sati kada se izvrši komanda za održavanje; rukovalac treba da obezbijedi njeno redovno pokretanje. Administratorske sesije ističu nakon 24 sata i uklanjaju se tokom čišćenja.",
          "Otisci vezani za komentare i prijave čuvaju se dok se ti zapisi ne uklone. Javni sadržaj, zahtjevi i zapisnik administratorskih radnji trenutno nemaju automatski rok brisanja; uklanjaju se ručno nakon provjere.",
          "Rok čuvanja mrežnih zapisa zavisi od pružaoca hostinga."
        ],
        "bullets": []
      },
      {
        "heading": "6. Ispravka, uklanjanje i vaša prava",
        "paragraphs": [
          "Ako je podatak netačan, sadrži lične informacije ili je sadržaj sporan, koristite obrazac za osporavanje na stranici broja ili nam pišite. Navedite broj, vezu ka objavi i razlog zahtjeva.",
          "Zahtjeve razmatramo i možemo ispraviti, sakriti ili ukloniti sadržaj nakon provjere. Radi zaštite od neosnovanih zahtjeva može biti potrebno dodatno obrazloženje.",
          "Zahtjevi za pristup, ispravku, brisanje i obraćanje nadležnom organu rješavaju se u skladu sa primjenjivim propisima."
        ],
        "bullets": []
      },
      {
        "heading": "7. Izmjene politike",
        "paragraphs": [
          "Ako se promijene način rada, pružaoci usluga ili rokovi čuvanja, ažuriraćemo ovu stranicu i datum posljednje izmjene."
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
