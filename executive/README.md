# FavaOS Executive Dashboard

Version: v1.0.0  
Status: Architecture design  
Scope: Documentation only

The Executive Dashboard is the first FavaOS page opened by the CEO. It is the leadership command center for company health, finance, products, customers, projects, infrastructure, risks, AI usage, documentation maturity, decisions, ADRs, and roadmap execution.

This folder defines architecture only. It does not include Django code, database models, routes, templates, migrations, or implementation files.

## Business Purpose

The dashboard helps the CEO answer five questions quickly:

- Is the company healthy today?
- Are revenue, cash flow, and bank balance under control?
- Are products, projects, customers, and support moving correctly?
- Are infrastructure, security, mail, VPN, and servers stable?
- Which decisions, risks, ADRs, releases, and reports need attention?

## Product Family

This design belongs to FavaOS, the internal enterprise operating system for Fava Imen Olka.

Related product areas:

- Finance
- HR
- Support
- Datacenter
- Infrastructure monitoring
- Product management
- Project management
- Knowledge base
- Roadmaps
- Decisions and ADRs
- AI Center

## Document Map

- [Dashboard Overview](dashboard-overview.md)
- [Widgets](widgets.md)
- [Executive KPIs](executive-kpis.md)
- [Executive Alerts](executive-alerts.md)
- [Executive Workflows](executive-workflows.md)
- [Dashboard Layout](dashboard-layout.md)
- [Executive Navigation](executive-navigation.md)
- [Daily Executive Report](daily-report.md)
- [Weekly Executive Report](weekly-report.md)
- [Monthly Executive Report](monthly-report.md)
- [Yearly Executive Report](yearly-report.md)

## Architecture Boundaries

The Executive Dashboard should aggregate trusted data from FavaOS modules. It should not own detailed business logic that belongs to finance, HR, support, infrastructure, documentation, or product modules.

Allowed responsibilities:

- Executive summary.
- KPI visualization.
- Alert prioritization.
- Report access.
- Drill-down links into source modules.
- Decision and risk visibility.

Not allowed responsibilities:

- Replacing finance accounting logic.
- Replacing HR workflows.
- Replacing ticketing workflows.
- Replacing monitoring engines.
- Storing duplicate source-of-truth records.
- Editing operational records directly without routing to the owning module.

## Source of Truth

Every widget must declare its source module, owner, update cadence, and data quality status.

If a widget cannot identify a source of truth, it must be marked as incomplete instead of showing guessed information.

## Design Principles

- CEO-first visibility.
- Read-only overview before operational editing.
- Fast scan in less than five minutes.
- Drill down from summary to evidence.
- Separate production facts from plans and research.
- Show missing data openly.
- Use consistent health states across all widgets.
- Preserve decisions, ADRs, lessons learned, and reports as company memory.
