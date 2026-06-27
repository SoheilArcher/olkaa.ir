# Executive Dashboard Widgets

Version: v1.0.0  
Status: Widget architecture

This document defines the first widget catalog for the FavaOS Executive Dashboard.

## Widget Standards

Each widget must define:

- Purpose.
- Source module.
- Owner.
- Update cadence.
- Health state.
- Drill-down destination.
- Data quality status.

Widgets must not duplicate source-of-truth records. They summarize and link to the owning module.

## Core Widgets

| Widget | Purpose | Source Module | Cadence | Owner |
| --- | --- | --- | --- | --- |
| Company Health | Overall executive health score. | Executive aggregation | Daily | CEO office |
| Revenue | Total recognized revenue view. | Finance | Monthly | Finance |
| Monthly Revenue | Current month revenue progress. | Finance | Daily | Finance |
| MRR | Monthly recurring revenue. | Finance / Contracts | Monthly | Finance |
| ARR | Annual recurring revenue. | Finance / Contracts | Monthly | Finance |
| Cash Flow | Cash-in and cash-out movement. | Finance | Daily | Finance |
| Bank Balance | Available bank balance. | Finance | Daily | Finance |
| Projects | Active project health. | Projects | Daily | Project owners |
| Products | Product portfolio health. | Product management | Weekly | Product owners |
| Active Customers | Current customer base status. | Customers / CRM | Weekly | Account owners |
| Support Tickets | Open, urgent, and overdue tickets. | Support | Real-time | Support lead |
| Infrastructure Status | Overall infrastructure health. | Infrastructure | Real-time | Infrastructure lead |
| Servers | Server availability and incidents. | Monitoring | Real-time | Infrastructure lead |
| VPN Status | VPN service health. | Infrastructure / VPN | Real-time | Network lead |
| Mail Status | Mail service and delivery health. | Mail Server | Real-time | Infrastructure lead |
| Security Alerts | Security incidents and warnings. | Security | Real-time | Security owner |
| AI Usage | Approved AI usage and risk status. | AI Center | Weekly | AI governance owner |
| Roadmap Progress | Company and product roadmap progress. | Roadmaps | Weekly | Product owners |
| Documentation Coverage | Documentation maturity and gaps. | Documentation | Weekly | Documentation owner |
| Technical Debt | Engineering debt affecting delivery or risk. | Engineering / ADR | Weekly | Engineering lead |
| Open Risks | Active strategic and operational risks. | Risk register | Daily | Risk owners |
| Upcoming Releases | Planned product and system releases. | Roadmaps / Projects | Weekly | Release owners |
| Recent Decisions | Recent management decisions. | Decisions | Weekly | CEO office |
| Recent ADRs | Recent architecture decisions. | ADR | Weekly | Engineering lead |
| Knowledge Growth | Knowledge-base updates and coverage. | Knowledge base | Weekly | Documentation owner |
| Research Progress | Active research initiatives. | Research | Monthly | Research owner |

## Widget States

Every widget should support:

- Normal state.
- Empty state.
- Loading state.
- Stale data state.
- Error state.
- Permission-limited state.
- Critical alert state.

## Widget Drill-Down

Each widget should open the relevant module page:

- Finance widgets open finance reports or ledgers.
- Infrastructure widgets open monitoring and incident views.
- Support widgets open ticket queues.
- Product widgets open product portfolio pages.
- Documentation widgets open documentation governance views.
- Roadmap widgets open roadmap detail pages.
- Decision and ADR widgets open records in company memory.

## Data Quality Labels

Suggested labels:

- Verified.
- Manual update.
- Automated source.
- Needs review.
- Stale.
- Missing source.
