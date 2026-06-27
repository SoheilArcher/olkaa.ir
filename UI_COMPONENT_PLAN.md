# UI Component Plan

Date: 2026-06-27  
Scope: Fava Imen Olka website and FavaOS staff portal  
Status: Planning only; no implementation

## Purpose

This plan defines the UI components needed before the project grows into a larger FavaOS interface. It should guide future template and CSS changes without redesigning the current product all at once.

## Design Principles

- Enterprise first, not marketing-heavy for internal tools.
- Persian-first with correct RTL behavior.
- Dense but readable dashboards.
- Consistent status language across finance, HR, tickets, datacenter, and executive views.
- Components must support mobile layouts.
- Use semantic HTML when data is tabular.
- Keep public website components visually refined and staff portal components operational.

## Token System

### Color Tokens

Current brand tokens:

- `--navy`
- `--navy-700`
- `--navy-600`
- `--gold`
- `--gold-soft`
- `--paper`
- `--cream`
- `--panel`
- `--steel`
- `--muted`
- `--line`

Recommended semantic tokens:

- `--surface-page`
- `--surface-panel`
- `--surface-card`
- `--text-primary`
- `--text-muted`
- `--border-subtle`
- `--status-success`
- `--status-warning`
- `--status-danger`
- `--status-info`
- `--status-unknown`

### Typography Tokens

Recommended scale:

- Display title
- Page title
- Section title
- Panel title
- Card title
- Body
- Body small
- Metadata
- Numeric KPI

Rules:

- Persian uses `Vazirmatn`.
- English metadata and numeric KPIs may use `Space Grotesk`.
- Do not use viewport-width-only font sizing.
- Do not use negative letter spacing.
- Keep dense dashboard titles smaller than hero titles.

### Spacing Tokens

Recommended spacing:

- `xs`: 4px
- `sm`: 8px
- `md`: 12px
- `lg`: 16px
- `xl`: 24px
- `2xl`: 32px
- `section`: 72px

## Component Catalog

## 1. App Shell

Variants:

- Public website shell.
- Staff portal shell.
- Auth shell.
- Future executive shell.

Required parts:

- Header or sidebar.
- Main content landmark.
- Optional page actions.
- Optional breadcrumbs.

Rules:

- Staff portal shell should use a shared sidebar include.
- Auth shell should remain focused and narrow.
- Public shell can keep sticky top navigation.

## 2. Navigation

Components:

- Public top navigation.
- Language switcher.
- Staff sidebar.
- Mobile menu.
- Breadcrumb.
- Tab navigation.

States:

- Active.
- Hover.
- Focus.
- Disabled.
- Restricted.
- External/admin destination.

Rules:

- Current page must be visually clear.
- Role-hidden items should not leave confusing gaps.
- Keyboard focus must be visible.

## 3. Buttons

Variants:

- Primary: gold.
- Secondary: ghost.
- Neutral.
- Danger.
- Link button.
- Icon button.
- Small button.

States:

- Default.
- Hover.
- Active.
- Focus.
- Disabled.
- Loading.

Rules:

- Destructive buttons must be visually distinct.
- Buttons in dense dashboards should not change layout width on state change.
- Use icon buttons only when icon meaning is familiar or tooltip exists.

## 4. Cards

Variants:

- Public service card.
- Portal module card.
- KPI card.
- Status card.
- Entity card.
- Empty card.

Required regions:

- Header.
- Title.
- Body.
- Metadata.
- Status.
- Actions.

Rules:

- Cards should not be nested inside other cards.
- Border radius should stay at 8px or less.
- KPI cards need fixed height or stable constraints.

## 5. Dashboard Widgets

Variants:

- KPI widget.
- Alert widget.
- List widget.
- Monitoring widget.
- Finance widget.
- Timeline/feed widget.
- Approval queue widget.

States:

- Healthy.
- Warning.
- Critical.
- Unknown.
- Empty.
- Loading.
- Stale.
- Permission-limited.

Rules:

- Every widget must show title, value or content, state, and optional drill-down.
- Unknown values must not be displayed as zero.
- Critical widgets should visually outrank routine cards.

## 6. Tables

Use real tables for:

- Invoices.
- Expenses.
- Payroll.
- Employees.
- Users.
- Tickets.
- Subscriptions.
- Ping checks.
- Audit logs.

Required features:

- Header row.
- Row hover.
- Focusable row action.
- Empty state.
- Responsive overflow.
- Numeric alignment.
- Status badges.

Rules:

- Use grid lists only for compact summaries.
- Use table markup for dense data comparison.

## 7. Forms

Components:

- Field wrapper.
- Label.
- Help text.
- Error text.
- Text input.
- Password input.
- Email input.
- Select.
- Textarea.
- Checkbox.
- Search field.
- Action row.

States:

- Default.
- Focus.
- Error.
- Disabled.
- Read-only.
- Required.

Rules:

- Keep labels visible.
- Error messages must stay near the field.
- LTR values such as email, domain, host, IP, and money should be formatted intentionally.

## 8. Status Badges

Statuses:

- Production.
- In Development.
- Planned.
- Research.
- Active.
- Suspended.
- Paid.
- Overdue.
- Open.
- Closed.
- Up.
- Down.
- Unknown.

Rules:

- Status colors must be semantic and consistent across modules.
- Do not use gold for every status; reserve gold for brand emphasis or neutral highlight.

## 9. Alerts and Messages

Variants:

- Success.
- Warning.
- Danger.
- Info.
- System notice.

Rules:

- Critical errors must be visible without relying only on color.
- Messages should include action guidance where useful.

## 10. Empty States

Required content:

- What is missing.
- Why it matters.
- Optional next action.

Rules:

- Empty state should not look like an error.
- Do not over-explain inside small widgets.

## 11. Accessibility Baseline

Requirements:

- Visible focus states for all interactive elements.
- Semantic headings in order.
- Skip link for public and portal shells.
- Real table markup for tabular data.
- Sufficient color contrast.
- Reduced motion support.
- Keyboard access for menus.
- `aria-current` for active navigation.

## Implementation Sequence

1. Document tokens in `design-system/design-tokens.md`.
2. Add component rules to `design-system/ui-components.md`.
3. Create shared sidebar/navigation include.
4. Normalize button, card, form, table, and widget classes.
5. Add accessibility baseline styles.
6. Split CSS after components are stable.

## Non-Goals

- No immediate redesign.
- No change to business logic.
- No new product feature.
- No frontend framework migration.
- No visual rewrite before component rules are approved.
