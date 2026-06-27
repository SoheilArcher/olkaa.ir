# Enterprise Architecture and SEO Audit Report

Date: 2026-06-27  
Scope: `olkaa.ir` Django project, public website, staff portal, enterprise documentation, runtime HTTP behavior  
Audit mode: Analysis-only first pass; no production code changes were made during the audit.

## Executive Summary

The project has evolved from a public company website into an early enterprise operating platform with public SEO pages, staff registration, OTP-based staff login, management dashboards, finance, HR, datacenter monitoring, ticketing, and broad enterprise documentation.

The strongest areas are:

- Clear Django app separation at a first-pass level: `website`, `staff_portal`, `core`, `hr`, `accounting`, `datacenter`, `ticketing`.
- Public pages are crawlable and have titles, meta descriptions, canonicals, robots directives, sitemap entries, Open Graph tags, and JSON-LD.
- Internal portal has meaningful operational modules and email OTP after password login.
- Documentation breadth is strong for a young project: Enterprise Manual, standards, roadmap, PLM, FavaOS, product docs, knowledge folders.

The highest-risk areas are:

- Production security defaults in `config/settings.py` are not hardened by default.
- Public HTML lacks CSP and several security headers.
- Staff access control relies heavily on `is_staff` plus permissions, but portal views mostly gate by staff status, not fine-grained permissions.
- Registration and OTP workflows lack throttling/rate limiting.
- Website content is centralized in large dictionaries inside `website/views.py`, which is fast to build but will not scale cleanly for a growing content library.
- SEO is technically valid but content depth, FAQ schema, product/service taxonomy, images, trust signals, and conversion instrumentation are still immature.

## System Inventory

Project name: Fava Imen Olka / olkaa.ir  
Business purpose: Public company website plus early internal enterprise operations portal.  
Product family: Enterprise software, airport/aviation workflows, datacenter/network services, internal FavaOS/Enterprise OS.  
Current status: Production website and early production internal portal; many product lines are documented as planned/in development/research.  
Target customers: Aviation, airport services, enterprises, infrastructure/network customers, hospitality/tourism, public-sector buyers, staff/internal operators.  
Architecture: Django 5 app with SQLite fallback/PostgreSQL option, Django admin, static website templates, staff portal templates, custom user model, modular domain apps.  

## Priority Findings

### Critical

#### C1. Production settings are not fail-closed

Evidence:

- `SECRET_KEY` falls back to `dev-insecure-change-me`.
- `DEBUG` defaults to `True`.
- `ALLOWED_HOSTS` defaults to `*`.
- `manage.py check --deploy` reports warnings for `DEBUG`, weak `SECRET_KEY`, missing secure cookies, and SSL redirect settings.

Estimated impact:

- If environment variables are missing or misconfigured, production can run with insecure settings.
- Debug disclosure, host-header risk, session exposure, and signing weakness become possible.

Recommended fix:

- Make production fail fast when `SECRET_KEY`, `ALLOWED_HOSTS`, and secure flags are missing.
- Default `DEBUG=False`.
- Add explicit `DJANGO_ENV=production` behavior.
- Set `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_SSL_REDIRECT=True` where reverse proxy supports it.
- Document production environment variables in `.env.example`.

#### C2. Authorization is too broad for internal portal views

Evidence:

- `finance`, `live`, `manager`, and `shifts` use `_is_staff_manager`, which checks only `user.is_authenticated and user.is_staff`.
- Fine-grained permissions are assigned during approval, but portal views do not consistently enforce them.

Estimated impact:

- Any approved staff user may access high-sensitivity dashboard pages if they have `is_staff=True`, even without specific finance/HR/datacenter roles.

Recommended fix:

- Add role/permission decorators per portal view.
- Separate admin/staff console access from module permissions.
- Introduce a central `staff_portal/access.py` policy module.

### High

#### H1. OTP and registration flows lack throttling

Evidence:

- `/portal/login/`, `/portal/otp/`, and `/portal/register/` do not implement rate limiting.
- OTP resend is available without visible cooldown beyond session state.

Estimated impact:

- Brute-force attempts, mail abuse, user enumeration pressure, and operational noise.

Recommended fix:

- Add per-IP and per-user throttling.
- Add OTP retry limits and resend cooldown.
- Log failed attempts.
- Consider `django-axes`, reverse-proxy limits, or custom cache-based counters.

#### H2. Missing Content Security Policy and hardened browser headers

Evidence:

- Live responses include `X-Frame-Options: DENY` and HSTS from server/proxy.
- CSP header is absent.
- Referrer-Policy, Permissions-Policy, X-Content-Type-Options are not visible in sampled responses.

Estimated impact:

- Higher XSS blast radius and weaker browser-side security posture.

Recommended fix:

- Add CSP in report-only mode first.
- Add `Referrer-Policy: strict-origin-when-cross-origin`.
- Add `X-Content-Type-Options: nosniff`.
- Add `Permissions-Policy` with conservative defaults.

#### H3. Website content architecture will not scale

Evidence:

- Public multilingual content, service pages, about content, and sitemap logic are stored as large Python dictionaries in `website/views.py`.

Estimated impact:

- Content changes require code deploys.
- Translation drift and duplicate business copy become likely.
- SEO/content governance becomes harder as pages grow.

Recommended fix:

- Move public content to structured data files or CMS-like models.
- Add a content registry with validation.
- Keep sitemap generation data-driven.

#### H4. Service pages are SEO-valid but still thin for competitive rankings

Evidence:

- Service pages have unique title/meta/H1/schema but limited body depth.
- No FAQ schema, case studies, industry-specific proof, screenshots, comparison sections, or detailed lead capture.

Estimated impact:

- Brand queries can improve, but non-brand service keywords will rank slowly.

Recommended fix:

- Add deeper sections per service: problems solved, process, deliverables, FAQs, industries, trust signals.
- Add FAQ schema where accurate.
- Add internal links between service, product, industry, and contact pages.

### Medium

#### M1. Duplicate access mapping logic exists

Evidence:

- `ACCESS_FIELDS` and `ACCESS_PERMISSIONS` exist in `staff_portal/views.py`.
- Similar role/permission mapping exists again in `hr/admin.py`.

Estimated impact:

- Role behavior can drift between manager portal and admin bulk actions.

Recommended fix:

- Move access definitions to a single module, e.g. `core/access_policies.py` or `staff_portal/access.py`.
- Reuse it in views and admin actions.

#### M2. Query performance will degrade as data grows

Evidence:

- Dashboard views calculate sums in Python over sliced querysets.
- Some properties such as invoice totals call related lines repeatedly.
- Live dashboard assembles mixed event feeds in Python.

Estimated impact:

- Acceptable now, but can become slow with invoices, tickets, payroll, ping checks, and registrations.

Recommended fix:

- Use `annotate`, `Sum`, `Count`, and materialized summaries where needed.
- Add indexes for common filters.
- Add query-count tests for dashboard views.

#### M3. Public website has no real images and minimal media optimization

Evidence:

- Public pages use inline SVG marks and no `<img>` tags.
- No `alt` attributes are needed for absent images, but visual trust is limited.

Estimated impact:

- SEO and conversion trust suffer because product/service pages lack real visuals, screenshots, diagrams, or office/service imagery.

Recommended fix:

- Add optimized WebP/AVIF imagery or screenshots with explicit width/height and alt text.
- Lazy-load below-the-fold images.
- Use real product/service visuals where possible.

#### M4. Fonts and CSS are render-blocking

Evidence:

- Google Fonts and `site.css` load in the document head.
- CSS file is ~32 KB and all public/internal styles are bundled together.

Estimated impact:

- Acceptable today, but render performance and Core Web Vitals can degrade on mobile.

Recommended fix:

- Self-host fonts or preload critical font subsets.
- Split public website CSS from staff portal/admin-oriented CSS.
- Add critical CSS strategy if needed.

#### M5. Product status and website claims are partially aligned but need stronger governance

Evidence:

- Product docs distinguish Production/In Development/Research/Planned.
- Public service pages include service status, but homepage language still groups multiple capabilities together.

Estimated impact:

- Risk of overclaiming if users interpret planned/in-development products as fully delivered.

Recommended fix:

- Add product/service status labels consistently on public pages.
- Link public service pages to product docs or public product pages with status.

#### M6. Accessibility is basic but incomplete

Evidence:

- Semantic headings exist and each page has one H1.
- Navigation uses links and a menu button with `aria-expanded`.
- Inline SVG marks are often `aria-hidden`, but contrast/focus state and keyboard flow need testing.

Estimated impact:

- Usability and compliance gaps for keyboard and assistive-technology users.

Recommended fix:

- Add visible focus states.
- Test with keyboard-only navigation.
- Add skip link.
- Validate color contrast for gold-on-dark and muted text.

### Low

#### L1. Sitemap is valid but minimal

Evidence:

- Sitemap includes home, language pages, about page, and service pages.

Estimated impact:

- Good baseline, but growth requires better sitemap organization.

Recommended fix:

- Add sitemap index if content grows.
- Add lastmod from content version/update metadata instead of always today.

#### L2. Changelog is out of sync

Evidence:

- `CHANGELOG.md` still has generic initial entries.

Estimated impact:

- Lower operational traceability.

Recommended fix:

- Update changelog per release or deployment batch.

#### L3. Documentation is broad but some files are placeholders

Evidence:

- Brand, architecture, security, and design-system documents exist but many are initial/short.

Estimated impact:

- Documentation structure is good but decision support may be weaker than it appears.

Recommended fix:

- Prioritize filling ADRs, security access-control details, deployment runbooks, backup/restore, and service ownership.

## Architecture Audit

### Strengths

- Modular Django app layout reflects business domains.
- Custom user model exists early, which avoids later migration pain.
- Shared `Party` and `TimeStamped` models establish useful common foundations.
- Staff registration and approval lifecycle is explicit.
- Datacenter monitoring has a command-based architecture suitable for cron/systemd.

### Technical Debt

- Portal authorization policy is not centralized.
- Public content is code-bound.
- Admin classes contain business actions and duplicate role assignment logic.
- Large `staff_portal/views.py` and `website/views.py` are becoming orchestration hotspots.
- No service layer for registration, approval, finance summaries, or monitoring alerts.
- No automated tests are visible for critical auth, OTP, registration, sitemap, or payment logic.

### Scalability Risks

- SQLite fallback is useful locally but production should standardize on PostgreSQL.
- Event feed and dashboard calculations will become expensive.
- Ping history can grow quickly without retention/archival policy.
- Admin-only workflows may not scale for employees/customers.

## SEO Audit

### Current Public URLs Reviewed

- `/`
- `/en/`
- `/ar/`
- `/about/`
- `/services/aviation-software/`
- `/services/datacenter/`
- `/services/ipv4-leasing/`
- `/services/home-check-in/`
- `/services/cip-express/`
- `/robots.txt`
- `/sitemap.xml`

### Strengths

- All sampled public pages return 200.
- HTTP redirects to HTTPS.
- `www` redirects to apex.
- Titles and meta descriptions are present.
- Canonical URLs are present.
- `robots` directives are indexable for public pages.
- Sitemap includes public URLs.
- Homepage has Organization and WebSite schema.
- Service pages have Service and Breadcrumb schema.
- Heading hierarchy starts with one H1 per page.

### Gaps

- No FAQ schema.
- No Product schema for actual product pages.
- No Article schema for knowledge/research content.
- Service pages are thin relative to SEO targets.
- No visible testimonials, certifications, case studies, customer proof, or trust assets.
- No optimized real images with alt text.
- Open Graph image is missing.
- Twitter card is only on homepage variants, not all pages.
- CSS and fonts are blocking.
- No analytics/search-console verification artifact is visible.

## UI/UX Audit

### Strengths

- Visual identity is consistent: dark navy, gold accent, clean cards, strong typography.
- Public homepage gives immediate brand and domain signal.
- Staff portal has operational dashboards for finance, live ops, manager, shifts.
- Buttons and CTAs are visible.
- Persian/English/Arabic language options exist.

### Gaps

- Homepage tries to cover many services at once; customer journey is broad.
- Service pages are mostly text cards and lack visual proof.
- Contact path is basic; no structured lead form, sales qualification, or CRM capture.
- Staff login/register links may distract public visitors unless visually grouped as staff-only.
- Accessibility testing is not documented.
- No explicit mobile screenshot/regression checks are documented.

## Business Audit

### Strengths

- Company positioning is clearer than before: enterprise software, aviation, datacenter, CIP.
- Service pages map to key SEO/service areas.
- Enterprise documentation reduces overclaiming by tracking status.

### Gaps

- Lead generation is weak: contact is email/phone only.
- No pricing or package framing.
- No industry landing pages yet.
- No case studies or approved client proof.
- Product/service status language is present but not fully integrated into journey.

## Performance Audit

### Strengths

- Static assets use long cache headers.
- CSS size is modest for a small site (~32 KB), but not split.
- No heavy JavaScript framework.
- Inline SVG marks avoid extra image requests.

### Gaps

- HTML responses did not show compression/cache headers in sampled HEAD responses.
- Google Fonts are external render-blocking resources.
- Public and portal CSS are bundled together.
- No performance budget or Lighthouse/Core Web Vitals baseline is documented.
- No image optimization pipeline because there are almost no images.

## Security Audit

### Strengths

- CSRF middleware is enabled.
- X-Frame-Options is DENY.
- HSTS header appears on live HTML responses.
- Password validation is enabled.
- OTP code is hashed in session using salted HMAC.
- Registration users are inactive until email verification and manager approval.

### Gaps

- `manage.py check --deploy` reports six security warnings in local settings.
- CSP is missing.
- Secure session/CSRF cookie settings are not configured in Django settings.
- Rate limiting is missing.
- OTP and login audit logs are missing.
- Staff portal uses broad staff gating.
- Payroll/bank data is stored as plain model fields without field-level encryption or masking policy.

## Documentation Audit

### Strengths

- Documentation surface is unusually strong: Enterprise Manual, standards, product docs, FavaOS, PLM, sync protocol, roadmap.
- Product status rules are explicit.
- Chat-to-project sync is documented.

### Gaps

- Many governance docs are initial placeholders.
- ADR folder has no concrete architecture decisions yet.
- Deployment runbook, backup/restore, incident response, monitoring runbook, and data retention policy are missing or incomplete.
- Website and product documentation need stronger cross-linking.

## Branding Audit

### Strengths

- Brand name, alternate spellings, logo mark, colors, and multilingual identity are present.
- Visual identity is consistent across public pages and portal.

### Gaps

- Logo system documentation is thin.
- No full brand asset pack or usage examples.
- No consistent real-world imagery.
- Typography rules exist as placeholders and need finalization.

## Recommended Next Steps

1. Harden production settings and headers.
2. Centralize authorization policies and enforce module-level permissions.
3. Add rate limiting and auth audit logs.
4. Expand service SEO pages with FAQ, proof, visuals, and conversion forms.
5. Split public content into structured content registry/CMS-like files or models.
6. Add automated tests for auth, OTP, registration approval, sitemap, public pages, and permissions.
7. Add lead capture/contact workflow.
8. Create ADRs for auth/permission model, website content architecture, and production settings.
