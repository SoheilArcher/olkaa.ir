# UI Design System Audit

Date: 2026-06-27  
Scope: Django templates and `static/css/site.css`  
Status: Audit only; no application code changes

## Executive Summary

The current UI has a clear brand direction: navy, gold, light paper backgrounds, Persian-first typography, compact enterprise cards, and separate public website and staff portal surfaces. The public website is visually stronger than the internal portal. The staff portal already has useful operational screens, but it needs a stricter design system before more modules are added.

The main risk is that all UI styles currently live in one CSS file and templates define repeated patterns manually. As more FavaOS modules are added, layout drift, duplicated component markup, inconsistent dashboards, and mobile issues will increase.

## Reviewed Files

- `templates/base.html`
- `templates/website/*.html`
- `templates/staff_portal/*.html`
- `static/css/site.css`

## Strengths

- Brand colors are defined as CSS variables.
- Persian and English font families are separated with `--fa` and `--en`.
- Public pages have consistent hero, card, section, and CTA patterns.
- Staff portal has a repeatable shell with sidebar and main content area.
- Cards, stats, empty states, monitor items, finance lists, and event feeds already exist.
- Mobile breakpoints exist for major grids.
- RTL is the default and Persian content is first-class.
- Forms have basic focus styling.
- Reduced-motion media query is present.

## Priority Findings

### High: CSS Is Monolithic

Current state:

- Public website, staff portal, auth pages, dashboards, forms, finance, monitoring, and mobile rules are all in `static/css/site.css`.

Impact:

- Future changes can unintentionally affect unrelated pages.
- Component ownership is unclear.
- Dashboard and public website styles can drift or conflict.

Recommended fix:

- Keep current CSS during stabilization, then split into documented layers:
  - `tokens.css`
  - `base.css`
  - `public.css`
  - `portal.css`
  - `components.css`
  - `dashboards.css`

### High: No Formal Component Contract

Current state:

- Reusable patterns exist, but they are not documented as components.
- Cards, stats, lists, panels, buttons, forms, tables, and monitor states use repeated markup patterns.

Impact:

- New FavaOS modules may create their own variants.
- UI consistency will degrade quickly.

Recommended fix:

- Define component names, variants, states, and usage rules before redesigning templates.

### High: Sidebar Navigation Needs System Rules

Current state:

- Portal pages repeat sidebar markup in each template.
- Active state is not consistently represented.
- Sidebar content differs slightly across dashboard, finance, manager, shifts, and live pages.

Impact:

- Users may not understand where they are.
- Future modules will duplicate navigation code.

Recommended fix:

- Create a single portal navigation component or template include.
- Define active, disabled, restricted, external/admin, and notification states.

### Medium: Dashboard Widgets Are Useful But Not Standardized

Current state:

- Dashboard widgets include `manager-stats`, `live-stats`, `finance-stats`, `portal-card`, `monitor-item`, `live-panel`, `finance-panel`, and `manager-section`.
- Similar widgets use different class names and layout assumptions.

Impact:

- Executive Dashboard and future FavaOS dashboards will be hard to keep consistent.

Recommended fix:

- Define a dashboard widget system with fixed states: normal, warning, danger, unknown, empty, loading, stale, permission-limited.

### Medium: Tables Are Actually Grid Lists

Current state:

- `compact-table`, `finance-list`, `recent-flow`, and `live-list` are grid/list patterns, not semantic tables.

Impact:

- Fine for compact dashboards, but weaker for accessibility, sorting, scanning, and dense financial data.

Recommended fix:

- Keep grid lists for summaries.
- Add a real table component for finance, payroll, users, tickets, subscriptions, and audit logs.

### Medium: Forms Need a Field System

Current state:

- Auth forms have good base styling.
- Manager approval form, access checkboxes, note field, and registration forms use separate patterns.

Impact:

- Error messages, help text, labels, and required states may become inconsistent.

Recommended fix:

- Define form field wrapper, label, help text, error, checkbox, textarea, select, password, and action row patterns.

### Medium: Mobile Portal Is Functional But Not Yet Ergonomic

Current state:

- Portal sidebar stacks above content under `760px`.
- Dense dashboards become single-column.

Impact:

- Mobile works, but staff users may need too much scrolling.
- Important actions can move far from context.

Recommended fix:

- Add mobile dashboard priority rules.
- Convert sidebar to compact top navigation or drawer later.
- Keep critical stats and alerts first.

### Medium: Accessibility Needs Baseline Rules

Current state:

- Some ARIA is present on website navigation and SVGs.
- Focus styling exists for auth inputs.
- Button/link focus states are incomplete.
- Color contrast likely passes in many areas but needs measured validation.

Impact:

- Keyboard users may lose focus context.
- Internal users may struggle in dense dashboards.

Recommended fix:

- Add visible focus styles for links, buttons, cards, sidebar items, and list rows.
- Add skip link.
- Validate contrast for gold text on light surfaces and muted text on navy.

### Low: Typography Is Strong But Needs Scale Names

Current state:

- Typography uses direct values and `clamp()` in many places.
- English and Arabic headline sizes were already reduced.

Impact:

- Visual quality is good, but future pages may use arbitrary sizes.

Recommended fix:

- Define type tokens: display, page-title, section-title, panel-title, card-title, body, small, metadata.

## Area Review

## Layout Consistency

Public layouts are cohesive. Portal layouts are operationally useful but need a shared grid model for dashboard pages. Current layout classes should be converted into named layout primitives before more modules are added.

## Sidebar / Navigation

Portal sidebar is visually consistent but duplicated in templates. It needs active state, role-aware item visibility, and a template include.

## Buttons

Buttons use `btn`, `btn-gold`, `btn-ghost`, and `btn danger`. This is a good start. Missing states: disabled, loading, icon button, small button, destructive confirm, secondary light variant.

## Cards

Cards exist across website and portal. Public cards are polished. Portal cards need standardized density, header, metadata, action, and status regions.

## Tables

Dense business data currently uses list/grid cards. This is not enough for accounting, payroll, ticket queues, user management, and audit logs.

## Forms

Auth forms are stronger than operational forms. Forms need consistent field wrappers, errors, required labels, help text, and action placement.

## Dashboard Widgets

Widget patterns exist but are fragmented. The Executive Dashboard should not be built until widget rules are formalized.

## Mobile Responsiveness

Public website is responsive. Portal is responsive but needs UX prioritization for operational use, not just stacking.

## RTL / Persian Support

RTL is strong by default. LTR values like email, amounts, hostnames, and times are handled in several places. This should become a formal data-formatting rule.

## Brand Colors

The navy/gold/paper palette is consistent but can become too monotone. Introduce semantic status colors carefully:

- Success
- Warning
- Danger
- Info
- Unknown

## Typography

Persian typography is strong. English and Arabic scaling is partially handled. Need formal type scale and line-height rules for dense panels.

## Spacing

Spacing is mostly consistent but not tokenized. Need spacing tokens for section, panel, card, field, row, and inline gaps.

## Accessibility

Accessibility is partially considered but not yet governed. Focus, semantics, table markup, skip navigation, and contrast need a formal baseline.

## Recommended Priority

1. Define tokens and component contracts.
2. Standardize portal navigation.
3. Standardize dashboard widgets.
4. Add table and form component rules.
5. Add accessibility baseline.
6. Split CSS only after component rules are approved.
