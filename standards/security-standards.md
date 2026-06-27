# Security Standards

Version: v1.0.0  
Status: Initial standard

## Security By Default

- Treat security as a product requirement from the beginning.
- Use least privilege for users, services, databases, and infrastructure.
- Do not commit secrets.
- Use secure defaults for authentication, authorization, logging, backup, and deployment.

## Access Control

- Define roles and permissions before production use.
- Review administrative access regularly.
- Log sensitive administrative actions where appropriate.
- Disable unused accounts and credentials.
- Do not use `is_staff` alone for sensitive staff portal modules.
- Centralize module authorization policy and reuse it in views, admin actions, and future APIs.

## Data Protection

- Classify sensitive data.
- Protect customer, financial, employee, operational, and security data.
- Use encryption where required.
- Define retention and deletion rules.

## API Security

- Use authentication for protected APIs.
- Enforce authorization at the correct boundary.
- Validate inputs.
- Rate-limit sensitive endpoints where appropriate.
- Avoid leaking sensitive details in errors.
- Apply throttling to login, OTP, resend, registration, and future password-reset flows.

## Deployment Security

- Use environment variables or secret managers for secrets.
- Keep debug mode disabled in production.
- Patch dependencies and operating systems.
- Monitor logs and alerts.
- Verify backups and recovery procedures.
- Production settings must fail closed when `SECRET_KEY` or `ALLOWED_HOSTS` are unsafe.
- Enable secure cookies, HTTPS redirect, HSTS, content-type nosniff, frame protection, and referrer policy when production HTTPS is ready.

## Sprint 1 Hardening Baseline

The Django project now includes:

- Production environment validation helper.
- Environment-driven secure cookie and HTTPS settings.
- Central staff portal access policy.
- Reusable staff module permission decorator.
- Cache-based throttling for sensitive authentication and registration paths.
- Security headers middleware with CSP report-only support.

Remaining work:

- Add audit logs for permission changes and staff approvals.
- Add stronger monitoring for throttling events.
- Move CSP from report-only to enforcing after browser testing.
- Add deployment runbook with exact production environment variables.
