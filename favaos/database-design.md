# FavaOS Database Design

Version: v1.0.0  
Status: Entity design only

This document defines entities only. It does not define Django models, migrations, schema SQL, or implementation code.

## Core Entities

## User

Represents a person who can access FavaOS.

Key concepts:

- Name
- Email
- Role
- Team
- Status
- Last access

## Role

Represents a permission group.

Key concepts:

- Name
- Description
- Permission set

## Product

Represents a company product line.

Key concepts:

- Name
- Category
- Status
- Current version
- Owner
- Next milestone
- Related roadmap
- Related documentation

## Project

Represents an internal or customer-facing project.

Key concepts:

- Name
- Related product
- Customer or sponsor
- Owner
- Status
- Timeline
- Risks
- Dependencies

## Customer

Represents a customer, partner, or organization reference.

Key concepts:

- Name
- Sector
- Account owner
- Relationship status
- Related projects
- Related contracts
- Public reference approval status

## Contract

Represents a customer, vendor, or internal contract record.

Key concepts:

- Name
- Related customer
- Related product or service
- Status
- Start date
- End date
- Renewal date
- Financial indicator
- Obligations
- Risks

## FinanceRecord

Represents high-level financial indicators.

Key concepts:

- Period
- Revenue indicator
- Cost indicator
- Outstanding invoice indicator
- Related contract
- Notes

## Employee

Represents management-level employee information.

Key concepts:

- Name
- Role
- Team
- Employment status
- Related products
- Current responsibilities
- Skills
- Workload indicator

## KnowledgeEntry

Represents an engineering or organizational knowledge item.

Key concepts:

- Title
- Category
- Related product
- Related technologies
- Status
- Source document
- Owner

## DocumentationRecord

Represents a document tracked by FavaOS.

Key concepts:

- Title
- Document path
- Category
- Version
- Status
- Owner
- Last review date

## RoadmapItem

Represents a product or company roadmap milestone.

Key concepts:

- Title
- Related product
- Target period
- Owner
- Status
- Dependencies
- Success metric

## DecisionRecord

Represents an important business or engineering decision.

Key concepts:

- Decision
- Date
- Owner
- Status
- Context
- Alternatives
- Consequences
- Related records

## ADRRecord

Represents an Architecture Decision Record.

Key concepts:

- Title
- Status
- Context
- Decision
- Consequences
- Alternatives
- Related product

## Risk

Represents a company, product, project, customer, contract, security, or infrastructure risk.

Key concepts:

- Title
- Category
- Severity
- Probability
- Impact
- Owner
- Mitigation
- Status
- Review date

## ResearchRecord

Represents a research item.

Key concepts:

- Title
- Topic
- Question
- Findings
- Recommendation
- Status
- Sources
- Related product

## InfrastructureAsset

Represents a server, network, service, monitoring item, or infrastructure dependency.

Key concepts:

- Name
- Type
- Environment
- Owner
- Status
- Criticality
- Monitoring link
- Backup status

## AIUseCase

Represents an approved, proposed, or researched AI use case.

Key concepts:

- Name
- Related product
- Status
- Data sensitivity
- Evaluation status
- Risk notes
- Owner

## KPI

Represents a company metric.

Key concepts:

- Name
- Definition
- Owner
- Source
- Frequency
- Target
- Current value
- Status

## Report

Represents an executive report.

Key concepts:

- Title
- Period
- Author
- Audience
- Summary
- Metrics
- Decisions needed
- Risks
- Follow-up actions

## AuditEvent

Represents a significant system or management change.

Key concepts:

- Actor
- Action
- Entity
- Timestamp
- Before state
- After state
- Reason
