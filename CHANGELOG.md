# Changelog

Notable changes to KoZove are recorded here. Changes merged after the latest
published release remain under **Unreleased** until a new version is tagged.

## [Unreleased]

### Security
- Updated Nuxt to 4.6.2, including the associated `undici` dependency update.
- Updated `serialize-javascript` to 7.1.4 to address the reported XSS vulnerability.
- Updated `node-forge` to 1.4.1 to address known security issues.

### Changed
- Updated `@lucide/vue` to 1.61.0.
- Raised minimum supported dependency versions for `argon2-cffi`, Pydantic,
  FastAPI, Uvicorn and SQLAlchemy.

### Development
- Added GitHub Actions CI and dependency-security workflows with PostgreSQL
  integration tests, dependency audits and Dependabot updates.
- Improved PostgreSQL test schema isolation.
- Added a separate production web image build. Public production deployment
  remains outside the scope of the development Compose configuration.

## [0.2.0-alpha] — 2026-10-14

The first source-code preview for GitHub.

### Added
- English README with setup instructions and screenshots.
- MIT license and security reporting guidelines.
- Multilingual Privacy Policy and Terms of Use.
- PostgreSQL integration tests and regression checks.

### Fixed
- Removed legacy anti-abuse helpers that shadowed the hardened implementations.
- Added a regression test to catch accidental reintroduction.
- Removed outdated legal-page placeholder copy.

### Known limitations
- Docker Compose is configured for development; do not expose it publicly.
- Hosting, legal/operator details, secure deployment and backup/restore need
  completion before public beta.

## [0.1.3] — 2026-10-14

- PostgreSQL-safe concurrent number creation.
- Atomic moderation transitions and a cleanup command.
- Anti-abuse helper module, basic integration tests and shared version setting.

## [0.1.2]

- Local MVP: phone lookup, reviews and reports, disputes, moderation dashboard and localization.
