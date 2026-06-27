# Dashboard Layout

Version: v1.0.0  
Status: Layout architecture

The Executive Dashboard layout should support fast scanning and clear prioritization.

## Layout Structure

### Top Row: Company KPIs

The top row should show the most important company-level signals:

- Company Health.
- Revenue.
- Monthly Revenue.
- MRR.
- ARR.
- Cash Flow.
- Bank Balance.
- Critical Alerts.

This row must be visible immediately after login.

### Middle: Products, Projects, Customers

The middle section should show execution and market-facing activity:

- Products.
- Projects.
- Active Customers.
- Support Tickets.
- Upcoming Releases.
- Roadmap Progress.

This section should show whether the company is delivering correctly.

### Bottom: Risks, Infrastructure, AI, Roadmaps, Reports

The bottom section should show governance and operational control:

- Open Risks.
- Infrastructure Status.
- Servers.
- VPN Status.
- Mail Status.
- Security Alerts.
- AI Usage.
- Documentation Coverage.
- Technical Debt.
- Recent Decisions.
- Recent ADRs.
- Knowledge Growth.
- Research Progress.
- Executive Reports.

## Visual Priority

Suggested visual priority:

- Critical alerts first.
- Financial indicators second.
- Delivery indicators third.
- Governance indicators fourth.
- Knowledge and research indicators fifth.

## Responsive Behavior

Desktop:

- Multi-column KPI row.
- Large middle grid for products, projects, and customers.
- Bottom governance grid.

Tablet:

- Two-column KPI layout.
- Stacked middle and bottom sections.

Mobile:

- Single-column layout.
- Critical alerts and Company Health first.
- Reports and detailed governance lower on the page.

## Widget Density

The CEO view should be compact but readable.

Avoid:

- Overly decorative cards.
- Marketing-style hero sections.
- Long explanatory text inside widgets.
- Hidden critical alerts.

Prefer:

- Clear numbers.
- Short status labels.
- Trend indicators.
- Drill-down links.
- Owner and last update metadata.

## Empty and Error States

Every widget must show clear states:

- No data yet.
- Data source missing.
- Data stale.
- Permission denied.
- Source module unavailable.
- Calculation pending.

Unknown should never be displayed as zero.
