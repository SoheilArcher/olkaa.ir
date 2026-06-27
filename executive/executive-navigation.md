# Executive Navigation

Version: v1.0.0  
Status: Navigation architecture

The Executive Dashboard should be the first page opened for the CEO.

## Primary Entry

Primary route concept:

- Executive Dashboard.

This document does not define Django routes. It defines navigation intent only.

## Navigation Hierarchy

Suggested executive navigation:

- Executive Dashboard
- Reports
- Finance
- Products
- Projects
- Customers
- Support
- Infrastructure
- Security
- AI Center
- Roadmaps
- Documentation
- Decisions
- ADRs
- Risks
- Research

## Dashboard Drill-Downs

Each dashboard widget should link to the source module:

- Company Health links to the executive summary.
- Revenue, Monthly Revenue, MRR, ARR, Cash Flow, and Bank Balance link to Finance.
- Projects links to Project Management.
- Products links to Product Management.
- Active Customers links to Customer Management.
- Support Tickets links to Support.
- Infrastructure Status, Servers, VPN Status, and Mail Status link to Infrastructure.
- Security Alerts link to Security.
- AI Usage links to AI Center.
- Roadmap Progress and Upcoming Releases link to Roadmaps.
- Documentation Coverage and Knowledge Growth link to Documentation and Knowledge Base.
- Technical Debt and Recent ADRs link to Engineering and ADR.
- Open Risks links to Risk Register.
- Recent Decisions links to Decision Log.
- Research Progress links to Research.

## Report Navigation

Reports section should include:

- Daily Executive Report.
- Weekly Executive Report.
- Monthly Executive Report.
- Yearly Executive Report.

## Breadcrumb Model

Suggested breadcrumb pattern:

- Executive Dashboard
- Executive Dashboard / Finance / Monthly Revenue
- Executive Dashboard / Infrastructure / Servers
- Executive Dashboard / Reports / Weekly Report
- Executive Dashboard / Decisions / Decision Detail

## Permission Model

The CEO has complete access.

Other users should see only modules allowed by their role.

Permission examples:

- Finance manager: finance widgets and reports.
- Infrastructure lead: infrastructure, servers, VPN, mail, and security alerts.
- Support lead: support tickets and customer support indicators.
- Product owner: products, roadmaps, documentation, ADRs, and releases.
- HR manager: HR-related executive summaries when added.

## Future Mobile Navigation

The navigation model should support a future mobile app with:

- Home summary.
- Alerts.
- Reports.
- Approvals.
- Drill-down records.
