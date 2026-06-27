# Roadmap After Enterprise Audit

Date: 2026-06-27  
Planning horizon: 90 days

## Roadmap Principles

- Security before feature expansion.
- Permissions before broader staff onboarding.
- Content depth before aggressive SEO campaigns.
- Documentation must follow implementation.
- Public claims must remain aligned with product status.

## Phase 1 — Stabilize Production Foundation

Target: Week 1-2

### Objectives

- Make production settings fail-closed.
- Reduce authentication and authorization risk.
- Establish baseline automated checks.

### Work Items

- Harden Django settings for production.
- Add security headers.
- Add login/OTP/registration throttling.
- Centralize staff portal authorization.
- Add tests for public pages, sitemap, login, OTP, registration, and permissions.
- Create ADR: production security settings.
- Create ADR: staff authorization model.

### Exit Criteria

- `manage.py check --deploy` has no critical production warnings.
- Staff users cannot access unauthorized portal modules.
- Auth throttling is verified.
- Security headers are visible on live responses.

## Phase 2 — SEO and Conversion Depth

Target: Week 3-5

### Objectives

- Improve non-brand ranking potential.
- Improve lead generation.
- Make service pages more useful for real customers.

### Work Items

- Expand each service page with process, deliverables, use cases, industries, and FAQs.
- Add FAQ schema where content is accurate.
- Add Open Graph image.
- Add lead/contact form with spam protection and CRM/notification workflow.
- Add optimized imagery or product screenshots.
- Add Search Console verification documentation.
- Add industry landing pages for aviation, datacenter/network, hospitality/tourism, enterprise.

### Exit Criteria

- Every service page has deeper content and FAQ where appropriate.
- Sitemap includes service and industry pages.
- Lead form creates a traceable inquiry.
- Public pages have shareable OG images.

## Phase 3 — Architecture Cleanup

Target: Week 6-8

### Objectives

- Reduce duplication.
- Improve maintainability of content and portal logic.
- Prepare for larger FavaOS modules.

### Work Items

- Move website content into a structured registry or content models.
- Extract role/permission mapping to a shared access policy module.
- Extract finance/live/manager dashboard summary services.
- Add query optimizations and indexes.
- Add retention policy for ping checks.
- Create ADR: website content architecture.
- Create ADR: monitoring data retention.

### Exit Criteria

- Public content changes no longer require editing large view dictionaries.
- Role definitions exist in one source of truth.
- Dashboard query counts are documented and bounded.

## Phase 4 — Enterprise Operations Maturity

Target: Week 9-12

### Objectives

- Improve operational readiness.
- Align docs, portal, and roadmap.
- Prepare for controlled product growth.

### Work Items

- Create deployment runbook.
- Create backup and restore runbook.
- Create incident response runbook.
- Update changelog and version history.
- Add monitoring alert ownership and escalation docs.
- Add access review process.
- Populate Enterprise Operating System records with real owners, KPIs, risks, and review cadence.

### Exit Criteria

- A new engineer can deploy, restore, and troubleshoot from docs.
- Access review process is documented.
- Enterprise dashboard has real owners and review dates.

## 90-Day Success Metrics

- Zero critical Django deploy warnings.
- 100% public pages covered by basic tests.
- 100% critical auth flows covered by tests.
- Every public service page expanded beyond thin content.
- At least one verified lead capture path.
- At least three concrete ADRs created.
- Search Console sitemap submitted and monitored.

## Deferred Items

- Pricing pages.
- Public case studies.
- Full CMS.
- API layer for mobile application.
- Advanced monitoring beyond ping.
- Field-level encryption for sensitive payroll/bank fields.

These should follow after the security and architecture foundation is stronger.
