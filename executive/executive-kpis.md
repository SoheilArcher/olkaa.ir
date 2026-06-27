# Executive KPIs

Version: v1.0.0  
Status: KPI architecture

Executive KPIs define the measurable signals used by the CEO dashboard.

## KPI Categories

- Company health.
- Finance.
- Products.
- Projects.
- Customers.
- Support.
- Infrastructure.
- Security.
- AI.
- Documentation.
- Roadmaps.
- Research.
- Risks.

## Finance KPIs

| KPI | Definition | Cadence | Owner |
| --- | --- | --- | --- |
| Revenue | Total recognized revenue for the selected period. | Monthly | Finance |
| Monthly Revenue | Revenue recognized in the current month. | Daily / Monthly | Finance |
| MRR | Monthly recurring revenue from active recurring contracts. | Monthly | Finance |
| ARR | Annual recurring revenue, normally MRR multiplied by 12 unless contract terms require adjustment. | Monthly | Finance |
| Cash Flow | Cash received minus cash paid during the selected period. | Daily | Finance |
| Bank Balance | Available bank balance based on verified bank records. | Daily | Finance |

## Operational KPIs

| KPI | Definition | Cadence | Owner |
| --- | --- | --- | --- |
| Active Projects | Projects currently in active delivery. | Daily | Project owners |
| Blocked Projects | Active projects with unresolved blockers. | Daily | Project owners |
| Active Products | Products currently maintained, sold, researched, or delivered. | Weekly | Product owners |
| Active Customers | Customers with active contracts, support, or delivery. | Weekly | Account owners |
| Support Tickets | Open, urgent, overdue, and recently closed tickets. | Real-time | Support lead |

## Infrastructure KPIs

| KPI | Definition | Cadence | Owner |
| --- | --- | --- | --- |
| Infrastructure Status | Overall status of critical company services. | Real-time | Infrastructure lead |
| Servers | Availability and health of registered servers. | Real-time | Infrastructure lead |
| VPN Status | Health of VPN services and related network access. | Real-time | Network lead |
| Mail Status | Mail server availability and delivery health. | Real-time | Infrastructure lead |
| Security Alerts | Active security warnings and incidents. | Real-time | Security owner |

## Knowledge KPIs

| KPI | Definition | Cadence | Owner |
| --- | --- | --- | --- |
| Documentation Coverage | Coverage of required product, architecture, process, decision, and support documentation. | Weekly | Documentation owner |
| Recent Decisions | Decisions recorded in the selected period. | Weekly | CEO office |
| Recent ADRs | Architecture decision records created or updated. | Weekly | Engineering lead |
| Knowledge Growth | Net growth of useful knowledge-base records. | Weekly | Documentation owner |
| Research Progress | Progress of active research items. | Monthly | Research owner |

## Risk KPIs

| KPI | Definition | Cadence | Owner |
| --- | --- | --- | --- |
| Technical Debt | Active engineering debt by severity and business impact. | Weekly | Engineering lead |
| Open Risks | Strategic, operational, financial, security, or delivery risks not closed. | Daily | Risk owners |
| Upcoming Releases | Releases planned for the selected period. | Weekly | Release owners |
| Roadmap Progress | Progress against approved company and product roadmaps. | Weekly | Product owners |

## KPI Quality Rules

- Every KPI must identify its owner.
- Every KPI must show last updated time.
- Every KPI must show whether data is verified, estimated, manual, or automated.
- Financial KPIs must not be shown as final unless finance validates them.
- Unknown data must be shown as unknown, not zero.
- Manual KPI updates must retain an audit trail.
