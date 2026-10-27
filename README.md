<div align="center">

# 📞 KoZove

**Who's calling? Find out together.**

A free, open-source platform for looking up phone numbers and sharing community experiences,
starting in **Montenegro (+382)**.

Search numbers, read reports, and share your experience. No account required for public submissions.

[![Release](https://img.shields.io/github/v/release/xydojhuk/KoZove?display_name=tag&include_prereleases&sort=semver&label=release&style=flat-square)](https://github.com/xydojhuk/KoZove/releases)
[![CI](https://github.com/xydojhuk/KoZove/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/xydojhuk/KoZove/actions/workflows/ci.yml)
[![Security checks](https://github.com/xydojhuk/KoZove/actions/workflows/security.yml/badge.svg?branch=main)](https://github.com/xydojhuk/KoZove/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-22a06b?style=flat-square)](LICENSE)

**[Features](#-features) · [Screenshots](#-screenshots) · [Run locally](#-run-locally) · [Tests](#-tests) · [Contributing](#-contributing)**

</div>

## ✨ Features

- 🔎 **Phone lookup** — search numbers from Montenegro's +382 numbering plan.
- 💬 **Community reviews** — submit and read experiences about phone numbers.
- 🛡️ **Manual moderation** — reviews and reports are checked before publication.
- 🌍 **Three languages** — Serbian, English and Russian.
- 🔐 **Admin dashboard** — manage submissions and disputes.
- 🧩 **Open source** — inspect, modify and self-host the code.

> KoZove displays community-submitted experiences, **not verified caller identities**.
> A report is not proof that a person or organization has done anything wrong.

## 📸 Screenshots

<p align="center">
  <img src="docs/screenshots/home-desktop.webp" alt="KoZove homepage" width="850">
</p>

<p align="center">
  <img src="docs/screenshots/number-details.webp" alt="Phone-number details" width="49%">
  <img src="docs/screenshots/admin-dashboard.webp" alt="Admin dashboard" width="49%">
</p>

## 🚀 Run locally

**Requirements:** Git and Docker with Docker Compose.

```bash
git clone https://github.com/xydojhuk/KoZove.git
cd KoZove
cp .env.example .env
```

Before starting, edit `.env`:

- Replace `POSTGRES_PASSWORD` with a strong password.
- Generate **different** values for `ABUSE_PEPPER` and `PROXY_SHARED_SECRET`.
- Set `ADMIN_PASSWORD_HASH` to an Argon2id password hash.
- Replace the placeholder `CONTACT_EMAIL` with an address you control.
- Keep `PUBLIC_ORIGIN=http://localhost:3000` for local development.
- Use the included Cloudflare Turnstile **test keys only in development**.

Generate a random secret (run it separately for each secret):

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Generate the administrator password hash using the API image:

```bash
docker compose build api
docker compose run --rm --no-deps api python -c 'from getpass import getpass; from argon2 import PasswordHasher; print(PasswordHasher().hash(getpass("Admin password: ")))'
```

Copy the hash into `ADMIN_PASSWORD_HASH` in `.env`, then start the stack:

```bash
docker compose up --build -d
```

| Service | Local URL |
| --- | --- |
| Web interface | http://localhost:3000 |
| API documentation | http://localhost:8000/docs |
| Health check | http://localhost:8000/healthz |

**Development only:** the included Compose stack is not hardened for public hosting.
In particular, the web service currently binds port 3000 to all host interfaces;
do not expose it to the internet or an untrusted network. See [SECURITY.md](SECURITY.md).

## 🧪 Tests

Create a separate test database (only once; skip this command if it already exists):

```bash
docker compose exec db sh -lc 'psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE kozove_test;"'
```

Run backend tests against the disposable test database:

```bash
docker compose exec api sh -lc 'export KOZOVE_TEST_DATABASE_URL="${DATABASE_URL%/*}/kozove_test"; python -m pytest -v tests/'
```

Check the frontend (from the repository root):

```bash
cd apps/web
npm ci
npm run build
npm audit
```

The repository also runs [CI](.github/workflows/ci.yml) on pull requests and pushes to `main`,
plus [scheduled and manual dependency audits](.github/workflows/security.yml).

## 🧰 Tech stack

- **Frontend:** Nuxt 4, Vue 3, TypeScript
- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL 17
- **Development environment:** Docker Compose

## 🤝 Contributing

Found a bug? [Open an issue](https://github.com/xydojhuk/KoZove/issues).
To propose a change, create a branch, make your changes and open a pull request.

Use only synthetic phone numbers and other synthetic data in tests and screenshots.
Do not commit passwords, API keys or personal information.

For security vulnerabilities, follow [SECURITY.md](SECURITY.md) rather than opening a public issue.
For release history, see [CHANGELOG.md](CHANGELOG.md) and [GitHub Releases](https://github.com/xydojhuk/KoZove/releases).

## 📄 License

KoZove is released under the [MIT License](LICENSE).

<sub>Built with care for an open and useful web.</sub>
