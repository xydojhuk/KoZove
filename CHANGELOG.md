# Changelog

Notable changes to KoZove are recorded here.

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
- Hosting, legal/operator details, secure deployment and backup/restore need completion before public beta.
- Screenshots need to be captured with synthetic content before publishing the release.

## [0.1.3] — 2026-10-14

- PostgreSQL-safe concurrent number creation.
- Atomic moderation transitions and a cleanup command.
- Anti-abuse helper module, basic integration tests and shared version setting.

## [0.1.2]

- Local MVP: phone lookup, reviews and reports, disputes, moderation dashboard and localization.
