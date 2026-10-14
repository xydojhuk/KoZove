import { watch } from 'vue'

type Locale = 'sr' | 'ru' | 'en'

const translations = {
  ru: {
    search: 'Найти номер',
    searchPlaceholder: '+382 20 417 412',
    heroBadge: 'Бесплатный сервис Черногории',
    heroTitle: 'Узнай, кто тебе звонил',
    heroDescription:
      'Проверяй неизвестные номера, читай отзывы и делись собственным опытом.',
    heroHint: 'Без регистрации. Бесплатно. Для номеров +382.',

    home: 'Главная',
    about: 'О проекте',
    support: 'Поддержать',
    privacy: 'Конфиденциальность',
    terms: 'Правила',

    howTitle: 'Как это работает',
    step1: 'Введи номер',
    step1Text: 'В любом привычном формате.',
    step2: 'Изучи отзывы',
    step2Text: 'Посмотри оценки и сообщения пользователей.',
    step3: 'Поделись опытом',
    step3Text: 'Помоги другим распознавать нежелательные звонки.',

    communityTitle: 'Создаём полезный справочник вместе',
    communityText:
      'KoZove не раскрывает частные данные абонентов. Отзывы публикуются после модерации.',

    unknown: 'Неизвестный номер',
    knownBusiness: 'Подтверждённая организация',
    noData: 'Об этом номере пока нет опубликованной информации.',
    reviews: 'Отзывы',
    rating: 'Рейтинг',
    complaints: 'Жалобы',
    notEnough: 'Недостаточно оценок',
    reportsWarning: 'На номер поступили жалобы',
    reportNotice: 'Жалобы отражают опыт пользователей, а не доказанный факт мошенничества.',
    writeReview: 'Оставить отзыв',
    writeReport: 'Сообщить о звонке',
    appeal: 'Оспорить информацию',
    noReviews: 'Пока нет опубликованных отзывов.',
    reviewNotice: 'Все сообщения проверяются перед публикацией.',
    source: 'Источник',

    stars: 'Оценка',
    category: 'Категория',
    comment: 'Комментарий',
    send: 'Отправить на проверку',
    cancel: 'Отмена',
    emailOptional: 'Email для ответа (необязательно)',
    pendingMessage: 'Спасибо! Сообщение отправлено на модерацию.',
    errorMessage: 'Не удалось выполнить запрос. Проверь данные и попробуй снова.',

    catNormal: 'Обычный звонок',
    catDelivery: 'Доставка',
    catAds: 'Реклама',
    catSurvey: 'Опрос',
    catSuspicious: 'Подозрительный звонок',
    catRobot: 'Робот / автоматический звонок',
    catOther: 'Другое',

    catScam: 'Подозрение на мошенничество',
    catHarassment: 'Навязчивые звонки',
    catData: 'Попытка получить личные данные',

    aboutTitle: 'О KoZove',
    aboutBody:
      'KoZove — независимый open-source проект для поиска отзывов о телефонных номерах. Мы начинаем с Черногории и планируем расширять географию.',
    aboutBody2:
      'Сервис не определяет личность частного абонента. Публичные названия организаций указываются по проверяемым источникам, а отзывы отражают субъективный опыт пользователей.',

    supportTitle: 'Поддержать проект',
    supportBody:
      'KoZove бесплатный. Добровольная помощь в будущем позволит оплачивать домен, сервер, модерацию и разработку новых функций.',
    supportPending: 'Приём пожертвований пока не подключён.',
    github: 'Исходный код на GitHub',

    privacyTitle: 'Политика конфиденциальности',
    privacyBody:
      'KoZove обрабатывает материалы, которые пользователи отправляют на сайт, и технические данные для предотвращения злоупотреблений. Подробнее — в политике конфиденциальности.',

    termsTitle: 'Правила использования',
    termsBody:
      'Запрещено публиковать ФИО частных лиц, адреса, чужие контакты, угрозы, травлю, рекламу и заведомо ложные сообщения. Отзывы проходят предварительную модерацию. Сведения пользователей не являются доказательством личности владельца номера или совершения правонарушения. Администрация может отклонять и удалять материалы.'
  },

  en: {
    search: 'Search number',
    searchPlaceholder: '+382 20 417 412',
    heroBadge: 'Free Montenegro service',
    heroTitle: "Find out who's calling",
    heroDescription:
      'Look up unknown numbers, read reviews and share your experience.',
    heroHint: 'No account. Free to use. For +382 numbers.',

    home: 'Home',
    about: 'About',
    support: 'Support us',
    privacy: 'Privacy',
    terms: 'Terms',

    howTitle: 'How it works',
    step1: 'Enter a number',
    step1Text: 'Use any common format.',
    step2: 'Read reviews',
    step2Text: 'See ratings and user reports.',
    step3: 'Share your experience',
    step3Text: 'Help others recognize unwanted calls.',

    communityTitle: 'Building a useful directory together',
    communityText:
      'KoZove does not disclose private subscriber identities. Reviews are moderated before publication.',

    unknown: 'Unknown number',
    knownBusiness: 'Verified organization',
    noData: 'No published information is available yet.',
    reviews: 'Reviews',
    rating: 'Rating',
    complaints: 'Reports',
    notEnough: 'Not enough ratings',
    reportsWarning: 'Users have reported this number',
    reportNotice: 'User reports do not prove fraud or establish the caller’s identity.',
    writeReview: 'Write a review',
    writeReport: 'Report a call',
    appeal: 'Dispute information',
    noReviews: 'No published reviews yet.',
    reviewNotice: 'All submissions are reviewed before publication.',
    source: 'Source',

    stars: 'Rating',
    category: 'Category',
    comment: 'Comment',
    send: 'Submit for review',
    cancel: 'Cancel',
    emailOptional: 'Contact email (optional)',
    pendingMessage: 'Thank you! Your submission is awaiting moderation.',
    errorMessage: 'Request failed. Please check your input and try again.',

    catNormal: 'Normal call',
    catDelivery: 'Delivery',
    catAds: 'Advertising',
    catSurvey: 'Survey',
    catSuspicious: 'Suspicious call',
    catRobot: 'Automated call',
    catOther: 'Other',

    catScam: 'Suspected scam',
    catHarassment: 'Repeated unwanted calls',
    catData: 'Attempt to obtain personal data',

    aboutTitle: 'About KoZove',
    aboutBody:
      'KoZove is an independent open-source directory of community reviews for phone numbers. We are starting in Montenegro.',
    aboutBody2:
      'We do not identify private subscribers. Organization names are shown only with supporting public sources, and reviews reflect individual user experiences.',

    supportTitle: 'Support KoZove',
    supportBody:
      'KoZove is free. Voluntary contributions may help fund hosting, moderation and future development.',
    supportPending: 'Donations are not enabled yet.',
    github: 'Source code on GitHub',

    privacyTitle: 'Privacy policy',
    privacyBody:
      'KoZove processes submitted content and security-related technical data. See the privacy policy for details about storage, cookies and removal requests.',

    termsTitle: 'Terms of use',
    termsBody:
      'Do not post private names, home addresses, third-party contact details, threats, harassment, spam or knowingly false statements. All submissions require moderation. User reports do not prove a caller’s identity or wrongdoing. Content may be rejected or removed.'
  },

  sr: {
    search: 'Pretraži broj',
    searchPlaceholder: '+382 20 417 412',
    heroBadge: 'Besplatna usluga za Crnu Goru',
    heroTitle: 'Saznaj ko te zove',
    heroDescription:
      'Provjeri nepoznate brojeve, pročitaj iskustva i podijeli svoje.',
    heroHint: 'Bez registracije. Besplatno. Za brojeve +382.',

    home: 'Početna',
    about: 'O projektu',
    support: 'Podrži projekat',
    privacy: 'Privatnost',
    terms: 'Pravila',

    howTitle: 'Kako funkcioniše',
    step1: 'Unesi broj',
    step1Text: 'U bilo kom uobičajenom formatu.',
    step2: 'Pročitaj iskustva',
    step2Text: 'Pogledaj ocjene i prijave korisnika.',
    step3: 'Podijeli iskustvo',
    step3Text: 'Pomozi drugima da prepoznaju neželjene pozive.',

    communityTitle: 'Zajedno gradimo koristan imenik',
    communityText:
      'KoZove ne otkriva identitet privatnih pretplatnika. Komentari se provjeravaju prije objavljivanja.',

    unknown: 'Nepoznat broj',
    knownBusiness: 'Potvrđena organizacija',
    noData: 'Za ovaj broj još nema objavljenih informacija.',
    reviews: 'Komentari',
    rating: 'Ocjena',
    complaints: 'Prijave',
    notEnough: 'Nema dovoljno ocjena',
    reportsWarning: 'Korisnici su prijavili ovaj broj',
    reportNotice: 'Prijave korisnika nijesu dokaz prevare ili identiteta pozivaoca.',
    writeReview: 'Ostavi komentar',
    writeReport: 'Prijavi poziv',
    appeal: 'Ospori informacije',
    noReviews: 'Još nema objavljenih komentara.',
    reviewNotice: 'Sve objave se provjeravaju prije prikazivanja.',
    source: 'Izvor',

    stars: 'Ocjena',
    category: 'Kategorija',
    comment: 'Komentar',
    send: 'Pošalji na provjeru',
    cancel: 'Otkaži',
    emailOptional: 'Email za odgovor (opciono)',
    pendingMessage: 'Hvala! Poruka je poslata na moderaciju.',
    errorMessage: 'Zahtjev nije uspio. Provjeri podatke i pokušaj ponovo.',

    catNormal: 'Uobičajen poziv',
    catDelivery: 'Dostava',
    catAds: 'Reklama',
    catSurvey: 'Anketa',
    catSuspicious: 'Sumnjiv poziv',
    catRobot: 'Automatski poziv',
    catOther: 'Ostalo',

    catScam: 'Sumnja na prevaru',
    catHarassment: 'Uznemiravajući pozivi',
    catData: 'Pokušaj prikupljanja ličnih podataka',

    aboutTitle: 'O KoZove projektu',
    aboutBody:
      'KoZove je nezavisan projekat otvorenog koda za pretragu korisničkih iskustava o telefonskim brojevima. Počinjemo od Crne Gore.',
    aboutBody2:
      'Ne identifikujemo privatne pretplatnike. Nazivi organizacija prikazuju se uz provjerljive javne izvore, a komentari predstavljaju lična iskustva korisnika.',

    supportTitle: 'Podrži KoZove',
    supportBody:
      'KoZove je besplatan. Dobrovoljna podrška može pomoći u plaćanju hostinga, moderacije i daljeg razvoja.',
    supportPending: 'Donacije još nijesu omogućene.',
    github: 'Izvorni kod na GitHub-u',

    privacyTitle: 'Politika privatnosti',
    privacyBody:
      'KoZove obrađuje dostavljeni sadržaj i tehničke podatke potrebne za zaštitu od zloupotrebe. Više informacija o čuvanju podataka, kolačićima i zahtjevima nalazi se u politici privatnosti.',

    termsTitle: 'Uslovi korišćenja',
    termsBody:
      'Zabranjeno je objavljivati privatna imena, kućne adrese, tuđe kontakte, prijetnje, uznemiravanje, spam i svjesno netačne tvrdnje. Sve prijave prolaze moderaciju. Korisničke prijave ne dokazuju identitet ili protivpravno postupanje. Sadržaj može biti odbijen ili uklonjen.'
  }
}

export function useLocale() {
  const cookie = useCookie<Locale>('kozove_locale', {
    default: () => 'sr',
    sameSite: 'lax'
  })

  const locale = useState<Locale>(
    'kozove_locale_state',
    () => cookie.value || 'sr'
  )

  watch(locale, (value) => {
    cookie.value = value
  })

  const t = (key: keyof typeof translations.ru): string => {
    const lang = translations[locale.value] || translations.sr
    return lang[key]
  }

  return { locale, t }
}