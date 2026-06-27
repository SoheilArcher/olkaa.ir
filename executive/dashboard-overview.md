# Executive Dashboard Overview

Version: v1.0.0  
Status: Architecture design  
Scope: CEO landing page

The Executive Dashboard is the default landing page after CEO login. It should present a reliable snapshot of Fava Imen Olka without requiring the CEO to open separate systems first.

## Primary User

Primary user: CEO

Secondary users:

- Company administrator.
- Product owners.
- Finance manager.
- Operations manager.
- Infrastructure lead.
- Support lead.

Secondary users may view limited sections based on permission, but the complete dashboard is designed for executive leadership.

## Dashboard Goals

- Show company health in one screen.
- Highlight urgent alerts before routine information.
- Connect KPIs to reports and source records.
- Show product, project, customer, finance, infrastructure, AI, documentation, and risk status together.
- Support daily, weekly, monthly, and yearly executive review.

## Operating Model

The dashboard is an aggregation layer over FavaOS modules.

Data domains:

- Finance.
- Customers.
- Products.
- Projects.
- Support.
- Infrastructure.
- Security.
- AI Center.
- Documentation.
- Roadmaps.
- Decisions.
- ADRs.
- Knowledge base.
- Research.

## Refresh Cadence

Suggested refresh levels:

- Real-time: infrastructure status, support tickets, security alerts.
- Daily: cash flow, bank balance, company health, AI usage.
- Weekly: roadmap progress, documentation coverage, technical debt, open risks.
- Monthly: revenue, MRR, ARR, product portfolio, research progress.
- Yearly: strategic performance, product family performance, company maturity.

## Health Model

All executive summary widgets should use a consistent health model:

- Healthy: normal state, no executive action required.
- Watch: trend needs attention.
- At Risk: owner must act.
- Critical: CEO attention required now.
- Unknown: data source missing or stale.

## Evidence Model

Every executive number should link to evidence:

- Source module.
- Last update time.
- Record owner.
- Calculation method.
- Data quality status.
- Related report.

## Access Model

The CEO sees the full dashboard.

Other roles see scoped dashboard sections based on permission:

- Finance users see finance KPIs and finance reports.
- HR users see HR-related staff and payroll summaries.
- Support users see ticket and service health.
- Infrastructure users see servers, VPN, mail, and security alerts.
- Product owners see product, roadmap, ADR, and documentation status.
