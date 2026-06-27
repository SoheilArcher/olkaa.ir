# Dashboard Layout Plan

Date: 2026-06-27  
Scope: Staff portal, FavaOS, and future Executive Dashboard  
Status: Planning only; no implementation

## Purpose

This plan defines how FavaOS dashboards should be structured so finance, HR, ticketing, datacenter, live operations, and executive views feel like one enterprise product.

## Current Dashboard Surfaces

Existing staff portal dashboard templates:

- `templates/staff_portal/dashboard.html`
- `templates/staff_portal/manager.html`
- `templates/staff_portal/live.html`
- `templates/staff_portal/finance.html`
- `templates/staff_portal/shifts.html`

Current dashboard CSS groups:

- `portal-shell`
- `portal-side`
- `portal-main`
- `portal-top`
- `portal-grid`
- `portal-card`
- `manager-stats`
- `manager-section`
- `live-stats`
- `live-layout`
- `live-panel`
- `finance-stats`
- `finance-layout`
- `finance-panel`
- `monitor-grid`

## Dashboard Problems To Solve

1. Similar dashboard patterns use different class names.
2. Widget states are not standardized.
3. Sidebar markup is repeated.
4. Dense data is displayed as grid lists instead of tables.
5. Mobile layout stacks but does not prioritize workflows.
6. Executive Dashboard architecture exists, but no UI layout contract exists yet.

## Shared Dashboard Anatomy

Every dashboard should use this structure:

1. App shell
2. Sidebar or primary navigation
3. Page header
4. Primary KPI row
5. Main work area
6. Secondary panels
7. Alerts and empty states
8. Optional activity feed

## Page Header

Required elements:

- Page title.
- Short page description.
- Optional eyebrow.
- Primary action.
- Secondary actions.
- Optional timestamp or live clock.

Rules:

- Header text must be concise.
- Actions should remain visible on desktop.
- On mobile, actions should stack below title.

## KPI Row

Use for:

- Finance totals.
- Ticket counts.
- Monitoring state.
- Pending approvals.
- Payroll queue.
- Company health.

Required elements:

- Label.
- Value.
- Unit or caption.
- Trend or state when available.
- Last updated when data can become stale.

States:

- Normal.
- Warning.
- Critical.
- Unknown.
- Stale.

Rules:

- Unknown is not zero.
- Critical KPIs must appear before routine KPIs.
- Numeric values should be LTR-aligned.

## Main Work Area

Recommended desktop layout:

- Two-column layout for operational pages.
- Three-column layout only for short widgets.
- Full-width panels for dense data or queues.

Recommended mobile layout:

- Critical alerts.
- KPI row.
- Primary queue.
- Secondary widgets.
- Feed/history last.

## Widget Sizes

Recommended sizes:

- Small KPI: one grid cell.
- Medium panel: one column.
- Wide panel: two columns.
- Full panel: full width.

Rules:

- Widgets should not resize based on hover.
- Values should not overflow their cards.
- Long Persian labels, emails, hostnames, and IPs must wrap safely.

## Dashboard-Specific Layouts

## Staff Portal Home

Purpose:

- Entry point for approved staff.

Recommended layout:

- Header with role-aware primary action.
- Module grid filtered by permission.
- Optional recent activity later.

Needed improvements:

- Active navigation state.
- Module icons or consistent status badges.
- Permission-limited empty state when user has no modules.

## Manager Dashboard

Purpose:

- Staff approval, HR overview, payroll queue, monitoring summary.

Recommended layout:

- Top KPI row: pending approvals, active employees, unpaid payroll, down monitoring targets.
- Primary full-width approval queue.
- Two-column secondary sections: employees and payroll.
- Monitoring section.
- Recent flow section.

Needed improvements:

- Separate approval queue from general dashboard widgets.
- Add table component for employees/payroll as data grows.
- Add audit/action history.

## Live Operations Dashboard

Purpose:

- Real-time operational visibility.

Recommended layout:

- Critical alerts and down services first.
- Live clock.
- KPI row.
- Wide monitoring panel.
- Ticket panel.
- Event feed.
- Attendance and shift widgets.

Needed improvements:

- Critical state styling.
- Refresh/stale indicator.
- Owner and support hint visibility.
- Mobile priority order.

## Finance Dashboard

Purpose:

- Receivables, costs, cash movement, recent financial records.

Recommended layout:

- KPI row: received income, receivables, paid costs, pending costs.
- Receivables panel.
- Costs panel.
- Full-width recent financial records.

Needed improvements:

- Real table for invoices and expenses.
- Currency formatting component.
- Financial status badges.
- Role-based visibility for sensitive amounts.

## Shift Dashboard

Purpose:

- Weekly operational staffing view.

Recommended layout:

- Page header with assignment action.
- Horizontally scrollable week view on small screens.
- Active assignments table.

Needed improvements:

- Shift color legend.
- Today/current shift emphasis.
- Conflict or coverage warning state.

## Future Executive Dashboard

Purpose:

- CEO first page in FavaOS.

Recommended layout:

- Top row: company health, revenue, monthly revenue, MRR, ARR, cash flow, bank balance, critical alerts.
- Middle: products, projects, customers, support tickets.
- Bottom: risks, infrastructure, AI usage, roadmap progress, documentation, reports.

Required widget states:

- Healthy.
- Watch.
- At Risk.
- Critical.
- Unknown.

Required behavior:

- Read-only summary first.
- Drill down into source modules.
- Every KPI must show source and last update.

## Navigation Plan

Short term:

- Keep sidebar.
- Add active state.
- Use shared include.
- Filter items by permission.

Medium term:

- Add grouped navigation:
  - Operations
  - Finance
  - HR
  - Infrastructure
  - Governance
  - Reports

Mobile:

- Collapse sidebar into top drawer or stacked navigation.
- Keep page title and critical alerts above navigation-heavy content.

## Accessibility Plan

Dashboard pages must include:

- One `h1`.
- Logical heading order.
- Visible focus states.
- Keyboard-friendly sidebar.
- Semantic tables for dense data.
- `aria-current` on active nav item.
- Text labels for status, not color alone.

## Responsive Plan

Breakpoints:

- Desktop: full sidebar and multi-column dashboards.
- Tablet: sidebar can remain, dashboard becomes two columns.
- Mobile: sidebar stacks or becomes drawer, dashboards become one column.

Priority on mobile:

1. Critical alerts.
2. KPI row.
3. Primary queue or work item.
4. Monitoring/tickets.
5. Activity feed.
6. Secondary records.

## Implementation Sequence

1. Create shared dashboard layout rules in documentation.
2. Add shared portal sidebar include.
3. Normalize KPI cards and panel components.
4. Convert finance and staff data lists to table components where needed.
5. Add dashboard state badges.
6. Add accessibility baseline.
7. Build Executive Dashboard UI using the standardized widget system.
