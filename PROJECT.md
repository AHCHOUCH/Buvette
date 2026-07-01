# Buvette Manager Project State

`PROJECT.md` is the authoritative source for the current state of Buvette Manager. Future development should update this document whenever structure, behavior, business rules, or technical decisions change.

## Current phase

The project is in the runnable foundation phase. The repository contains the modular project structure, an operational Flask application factory, registered feature blueprints, centralized SQLAlchemy models, reusable domain services, shared validators/helpers, authentication placeholders, Docker support, and a touch-first UI foundation. Complete business workflows are intentionally not implemented yet.

## Application structure

- `app/auth`: authentication and session management placeholders.
- `app/dashboard`: landing page and operational overview service interface.
- `app/clients`: client records and account status service interface.
- `app/breakfast`: future breakfast ordering and tracking workflows.
- `app/lunch`: future lunch ordering and tracking workflows.
- `app/charges`: future charge creation and review workflows.
- `app/payments`: future payment recording and reconciliation workflows.
- `app/ledger`: ledger preparation and balance services.
- `app/settings`: application and operational configuration placeholders.
- `app/models`: centralized `User`, `Client`, and `LedgerEntry` models.
- `flask_login.py` and `flask_migrate.py`: local compatibility shims that preserve offline runnable behavior when third-party packages are unavailable; production installs should use the dependencies listed in `requirements.txt`.
- `app/services`: shared business services that span features.
- `app/forms`: shared form helpers and validators.
- `app/templates`: Jinja templates organized by layout, components, and feature.
- `app/static`: global CSS and JavaScript assets.
- `app/utils`: constants, formatting, date, and validation helpers.

## Architectural principles

1. Features are isolated into modules.
2. Models remain centralized under `app/models`.
3. Business logic belongs in service modules.
4. Route handlers coordinate requests, responses, validation, and service calls only.
5. Documentation is part of the application and must be maintained with code changes.
6. Foundation services expose stable interfaces before workflows are built.

## Implementation status

- Project directories: created.
- Application factory, SQLAlchemy, Flask-Login, Flask-Migrate, and CSRF initialization: implemented.
- Feature route modules: registered with protected placeholder pages until each workflow is implemented.
- Models: `User`, `Client`, and `LedgerEntry` implemented for the shared domain foundation.
- Database migrations: `migrations/0001_domain_foundation.sql` documents non-destructive table creation.
- Services: reusable `ClientService`, `LedgerService`, and `DashboardService` interfaces implemented.
- Templates/static assets: touch-first base layout, navigation, login, dashboard placeholders, reusable components, design-system CSS, Bootstrap loading, and minimal JavaScript utilities implemented.
- Default routes: `/` redirects by authentication state and `/health` returns `{"status": "ok"}` for Docker health checks.
- Docker: `Dockerfile`, `docker-compose.yml`, and `.dockerignore` added for foreground startup on port 5000.
- Tests: directory created; test suite not yet implemented.

## Development workflow

Before implementing any business workflow:

1. Explain the proposed design.
2. Explain why it fits the current architecture.
3. Explain required database changes, or explicitly state that none are required.
4. Implement the approved module in its feature directory with models, migrations, services, routes, templates, validation, and tests as appropriate.
5. Update `PROJECT.md` and any affected documents in `docs/`.
6. Stop and wait for approval before beginning the next module.
