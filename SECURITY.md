# Security Policy

KoZove is an open-source **alpha** project. Its included development Docker Compose
configuration is **not production-hardened** and must not be deployed publicly as-is.

## Supported Versions

| Version | Security fixes |
| --- | --- |
| Latest development version on `main` | Supported on a best-effort basis |
| `v0.2.0-alpha` and earlier tags | No separate security backports |

Security fixes may be committed to `main` without publishing a new release.
Do not assume an older tagged version includes all fixes available on `main`.

## Reporting a Vulnerability

Do **not** disclose exploitable details in a public GitHub Issue, Discussion or pull request.

Use the repository's **Security** tab and select **Report a vulnerability**
when private vulnerability reporting is enabled.

Include:

- A clear description of the affected component and potential impact.
- Reproduction steps using synthetic data only.
- Affected version or commit, if known.
- Suggested mitigation, if you have one.

Do not submit passwords, API keys, access tokens, private phone-number records,
or other personal data. If the private reporting option is unavailable,
do not publish exploit details publicly; check the repository owner's profile
for an appropriate private contact channel.

## Security Checks

KoZove uses GitHub Actions for backend tests and frontend builds, dependency audits,
and GitHub CodeQL analysis. These checks help detect known problems but do **not**
guarantee that the code is free of vulnerabilities.

- [CI workflow](.github/workflows/ci.yml)
- [Dependency security workflow](.github/workflows/security.yml)

The development stack is intended for local testing. Keep secrets in an untracked
`.env` file, use Turnstile test credentials only in development, and avoid
exposing development services to untrusted networks.
