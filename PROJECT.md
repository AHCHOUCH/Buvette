# Buvette Manager Project State

`PROJECT.md` is the authoritative source for the current state of Buvette Manager. Future development should update this document whenever structure, behavior, business rules, or technical decisions change.

## Current phase

The project is in the initial organization phase. The repository contains the complete modular project structure and documentation baseline needed before feature implementation begins. No runtime application behavior, routes, models, or migrations have been implemented yet.

## Application structure

- `app/auth`: authentication and session management.
- `app/dashboard`: landing page and operational overview.
- `app/clients`: client records and account status.
- `app/breakfast`: breakfast ordering and tracking workflows.
- `app/lunch`: lunch ordering and tracking workflows.
- `app/charges`: charge creation and review.
- `app/payments`: payment recording and reconciliation.
- `app/ledger`: account ledger views and transaction history.
- `app/settings`: application and operational configuration.
- `app/models`: centralized data models.
- `app/services`: shared business services that span features.
- `app/forms`: shared forms and form helpers.
- `app/templates`: Jinja templates organized by layout and feature.
- `app/static`: CSS, JavaScript, and image assets.
- `app/utils`: cross-cutting utility functions.

## Architectural principles

1. Features are isolated into modules.
2. Models remain centralized under `app/models`.
3. Business logic belongs in service modules.
4. Route handlers coordinate requests, responses, validation, and service calls only.
5. Documentation is part of the application and must be maintained with code changes.

## Implementation status

- Project directories: created.
- Feature route modules: created as non-runnable placeholders; no endpoints are implemented yet.
- Models: directory created; concrete models not yet implemented.
- Database migrations: directory created; migration tooling not yet initialized.
- Templates/static assets: directories created; UI not yet implemented.
- Tests: directory created; test suite not yet implemented.

## Development workflow

Before implementing any module:

1. Explain the proposed design.
2. Explain why it fits the current architecture.
3. Explain required database changes, or explicitly state that none are required.
4. Implement the approved module in its feature directory with models, migrations, services, routes, templates, validation, and tests as appropriate.
5. Update `PROJECT.md` and any affected documents in `docs/`.
6. Stop and wait for approval before beginning the next module.
