# Master TODO After Enterprise Audit

Date: 2026-06-27  
Source: `AUDIT_REPORT.md`

## Critical

- [ ] Harden production settings.
  - Impact: prevents accidental insecure deployment.
  - Fix: require production `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG=False`, secure cookies, SSL redirect settings.

- [ ] Replace broad staff gating with module-level authorization.
  - Impact: prevents staff users from seeing finance/HR/datacenter areas outside their role.
  - Fix: central access policy module and decorators for each portal view.

## High

- [ ] Add throttling to login, OTP, resend, and registration.
  - Impact: reduces brute-force, OTP abuse, and email spam.
  - Fix: cache-based counters or `django-axes` plus reverse-proxy rate limits.

- [ ] Add security headers.
  - Impact: lowers browser-side attack surface.
  - Fix: CSP report-only, Referrer-Policy, Permissions-Policy, X-Content-Type-Options.

- [ ] Move website content out of large view dictionaries.
  - Impact: improves maintainability and content governance.
  - Fix: structured YAML/JSON/Markdown registry or content models.

- [ ] Expand service pages for SEO depth.
  - Impact: improves non-brand ranking potential.
  - Fix: add FAQs, process sections, industries, trust assets, and internal links.

## Medium

- [ ] Remove duplicated role/permission mappings.
  - Impact: avoids access drift between manager portal and admin actions.
  - Fix: shared policy module.

- [ ] Optimize dashboard database queries.
  - Impact: prevents slow dashboards as operational data grows.
  - Fix: annotations, aggregation, indexes, query-count tests.

- [ ] Add optimized public images and Open Graph image.
  - Impact: improves trust, sharing, and SEO presentation.
  - Fix: WebP/AVIF assets with dimensions and alt text.

- [ ] Split CSS by public site and staff portal.
  - Impact: improves rendering and maintainability.
  - Fix: `public.css`, `portal.css`, optional critical CSS.

- [ ] Add accessibility baseline.
  - Impact: improves keyboard and assistive technology usability.
  - Fix: focus states, skip link, contrast validation, keyboard tests.

- [ ] Add tests for critical flows.
  - Impact: reduces regression risk.
  - Fix: Django tests for public pages, sitemap, auth, OTP, registration, permissions.

## Low

- [ ] Improve sitemap metadata.
  - Impact: better crawl freshness signaling.
  - Fix: content-driven `lastmod`.

- [ ] Update `CHANGELOG.md`.
  - Impact: improves release traceability.
  - Fix: add entries for public SEO pages, staff login, OTP, shift scheduling.

- [ ] Fill placeholder documentation.
  - Impact: improves enterprise governance quality.
  - Fix: expand ADRs, brand asset docs, deployment runbook, incident response.

## Suggested Issue Labels

- `priority:critical`
- `priority:high`
- `priority:medium`
- `priority:low`
- `area:security`
- `area:seo`
- `area:architecture`
- `area:ui-ux`
- `area:performance`
- `area:documentation`
- `area:business`

## First Sprint Recommendation

1. Production settings hardening.
2. Module-level portal authorization.
3. Auth/OTP throttling.
4. Security headers.
5. Automated tests for auth and public URLs.

These five items reduce the most operational risk before more feature work.
