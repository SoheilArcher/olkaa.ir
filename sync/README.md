# Chat-to-Project Sync

Version: v1.0.0  
Status: Initial protocol

The Chat-to-Project Sync Protocol ensures that important decisions discussed outside the repository are converted into repository documentation.

Chat conversations are not the source of truth. Repository documentation is the source of truth.

## Purpose

Any important decision, architecture change, product direction, roadmap update, brand decision, business rule, or technical lesson discussed outside the repository must be summarized and committed to the repository.

## Documents

- [Chat Sync Protocol](CHAT_SYNC_PROTOCOL.md)
- [Change Intake Template](CHANGE_INTAKE_TEMPLATE.md)
- [Daily Sync Log](DAILY_SYNC_LOG.md)
- [Weekly Review Template](WEEKLY_REVIEW_TEMPLATE.md)

## Required Sync Fields

Every sync entry must include:

- Date
- Source
- Topic
- Decision
- Affected Products
- Files Updated
- Follow-up Tasks
- Commit Hash

## Privacy Rule

Do not store private or sensitive chat content. Store only business, product, architecture, brand, and engineering decisions.
