# Chat-to-Project Sync Protocol

Version: v1.0.0  
Status: Initial protocol

Chat conversations are not the source of truth. Repository documentation is the source of truth.

## 1. What Must Be Synced

Sync any discussion outside the repository that affects:

- Business decisions.
- Product direction.
- Architecture changes.
- Roadmap updates.
- Brand decisions.
- Business rules.
- UI or UX direction.
- Security requirements.
- Documentation structure.
- Technical lessons learned.
- Code behavior or implementation direction.
- Operational procedures.
- Research findings.

If a discussion affects code, roadmap, product, UI, brand, or documentation, it must create or update repository files.

## 2. What Must Not Be Synced

Do not sync:

- Private chat content.
- Personal messages.
- Sensitive employee information.
- Credentials, secrets, tokens, or private keys.
- Customer private data.
- Raw logs containing sensitive data.
- Unapproved confidential commercial details.
- Speculation that has not become a decision, requirement, lesson, or follow-up task.

## 3. How To Summarize Chat Decisions

Summaries must be professional, concise, and factual.

Every sync entry must include:

- Date.
- Source.
- Topic.
- Decision.
- Affected Products.
- Files Updated.
- Follow-up Tasks.
- Commit Hash.

Summaries should capture the decision and its impact, not the private conversation.

## 4. Where To Store Updates

Store updates in the appropriate repository location:

- Product changes: `products/`
- Roadmap updates: `roadmap/` or `MASTER_ROADMAP.md`
- Executive management changes: `enterprise/` or `favaos/`
- Architecture decisions: `adr/`
- Business or engineering decisions: `decisions/`
- Lessons learned: `lessons/`
- Research: `research/`
- Innovation ideas: `innovation/`
- Engineering knowledge: `knowledge/`
- Brand decisions: `brand/`
- Website content decisions: `website/`
- Standards changes: `standards/`
- Security changes: `security/`
- Sync records: `sync/DAILY_SYNC_LOG.md`

## 5. How To Reference Commits

After committing the documentation update, record the commit hash in the sync entry.

Use this format:

```text
Commit Hash: abc1234
```

If the sync entry is prepared before commit, use:

```text
Commit Hash: Pending
```

Then update the entry after commit if required.

## 6. Daily Sync Workflow

1. Review important chats, meetings, calls, and external discussions from the day.
2. Identify decisions, requirements, lessons, and follow-up tasks.
3. Remove private or sensitive details.
4. Update the relevant repository documents.
5. Add a daily sync entry to `DAILY_SYNC_LOG.md`.
6. Commit the documentation updates.
7. Record the commit hash in the sync log when available.

## 7. Weekly Review Workflow

1. Review daily sync entries from the week.
2. Confirm completed and open decisions.
3. Identify product, architecture, roadmap, brand, documentation, and security changes.
4. Move unresolved decisions into the correct decision or ADR documents.
5. Update risks and next-week priorities.
6. Commit the weekly review document or updates.
