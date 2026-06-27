# Security Standards

Version: v1.0.0  
Status: Initial structure

## Completed

- Initial security standards document created.
- Sprint 1 production hardening baseline added.
- Production startup validation now rejects insecure `SECRET_KEY` and wildcard or missing `ALLOWED_HOSTS`.
- Staff portal module access policy is centralized.
- Login, OTP, OTP resend, and registration now have cache-based throttling.
- Baseline browser security headers are configured, with CSP in report-only mode.

## In Progress

- Define baseline security principles, ownership, review process, and control requirements.
- Expand access reviews and audit logging for sensitive HR, payroll, finance, datacenter, and user-management actions.

## Planned

- Add security standards for products, infrastructure, identity, data, and operations.
- Add field-level protection guidance for bank, payroll, national ID, and customer financial data.
- Add incident response, backup, restore, and production deployment runbooks.

## Production Configuration Requirements

Production must define:

- `DJANGO_ENV=production`
- `DEBUG=False`
- `SECRET_KEY` with a non-development value
- `ALLOWED_HOSTS` without wildcard values
- `CSRF_TRUSTED_ORIGINS` for trusted HTTPS origins
- `SECURE_SSL_REDIRECT=True` when the reverse proxy supports HTTPS correctly
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_HSTS_SECONDS` after HTTPS is verified

Development may keep local defaults, but production must fail closed when critical values are missing.

## Staff Portal Access

Staff portal access must use module-level policy checks, not broad `is_staff` checks alone.

Protected modules:

- Finance and accounting
- HR
- Attendance
- Payroll
- Datacenter
- Ticketing
- Admin and staff management

Superusers may access all staff modules. Other staff users require the appropriate role or Django permission.
