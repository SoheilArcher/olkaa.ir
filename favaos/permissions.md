# FavaOS Permissions

Version: v1.0.0  
Status: Architecture design

## Permission Principles

- Least privilege.
- Role-based access control.
- Sensitive finance, HR, contracts, customers, and security data must be restricted.
- Important changes should be auditable.
- Read and write permissions should be separated.

## Roles

## Executive Admin

Full access to all modules, permissions, reports, and settings.

## Executive Viewer

Read-only access to executive dashboards, reports, product status, roadmap status, risks, and KPIs.

## Product Owner

Manage assigned product records, product roadmap items, product risks, product documentation, and related decisions.

## Project Owner

Manage assigned projects, milestones, blockers, risks, and status updates.

## Finance Manager

Manage finance indicators, contract financial notes, revenue indicators, and finance reports.

## HR Manager

Manage employee records, roles, workload indicators, and HR reports.

## Documentation Manager

Manage documentation records, knowledge-base links, standards, decisions, ADR links, and documentation coverage.

## Infrastructure Manager

Manage infrastructure assets, status, incidents, backups, and monitoring records.

## AI Manager

Manage AI use cases, evaluation records, data sensitivity notes, AI risks, and AI roadmap items.

## Research Contributor

Create and update research records, findings, sources, and recommendations.

## Read-Only User

Read approved non-sensitive records only.

## Sensitive Data Rules

- Finance data requires finance or executive permission.
- HR data requires HR or executive permission.
- Contract details require contract, finance, or executive permission.
- Security and infrastructure records may require restricted access.
- Customer public reference approval must be visible to users who create website or sales content.
