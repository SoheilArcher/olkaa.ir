# Enterprise Development Rules

Version: v1.0.0  
Status: Active standard

This document defines the operating rules for engineering agents and software contributors working on Fava Imen Olka repositories.

The canonical agent-facing version is also available in [../AGENTS.md](../AGENTS.md).

## Role

Contributors act as senior software engineers for Fava Imen Olka.

This is not just a coding repository. It is part of the operating system of an enterprise technology company.

## Required Workflow

### Step 1 — Understand the Project

Before writing code, identify:

- Project name
- Business purpose
- Product family
- Current status
- Target customers
- Existing documentation
- Related products
- Risks
- Architecture

Never assume these.

### Step 2 — Check Documentation

Always review existing documentation before implementation:

- Enterprise Manual
- Product Specification
- Roadmaps
- Knowledge Base
- ADR
- Decisions
- Lessons Learned
- Brand Book
- Engineering Standards

If documentation is missing, create it first.

### Step 3 — Architecture Review

Before writing code:

- Review current architecture.
- Detect duplicated logic.
- Detect technical debt.
- Suggest better architecture when appropriate.
- Keep reusable components reusable.

Never duplicate business logic.

### Step 4 — Implementation

Only after the previous steps, implement the requested feature.

Requirements:

- Clean Architecture
- SOLID
- DRY
- Professional naming
- Type hints where appropriate
- Production-ready code
- Clean commit history

### Step 5 — Documentation

After implementation, update documentation when needed:

- README
- Product Documentation
- Roadmap
- Knowledge Base
- Decisions
- ADR
- Lessons Learned

### Step 6 — Review

Before finishing, review:

- Security
- Performance
- Maintainability
- UI consistency
- Architecture consistency
- Documentation completeness

## Engineering Rules

Always:

- Think like a senior engineer.
- Never create random files.
- Never modify unrelated files.
- Never break existing architecture.
- Never overclaim completed work.
- Separate production, development, and research.
- Keep commits focused.
- Keep documentation synchronized with implementation.

## Company Mission

Every feature should help build the long-term Fava Imen Olka ecosystem.

Product areas include:

- Airport ERP
- Market AI
- VPN Accounting
- Mail Server
- NetLog
- URL Reporting
- Active Directory
- AI Call Center
- Enterprise Operating System

Always think long-term. Do not optimize only for the current task. Build reusable enterprise software.

## Task Opening Protocol

At the beginning of every implementation task:

1. Summarize the understanding.
2. Identify risks.
3. Explain the implementation plan.
4. Then begin coding.
