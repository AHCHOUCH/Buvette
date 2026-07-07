# Architecture

Buvette Manager uses a feature-module architecture. Each feature owns its routes, feature-specific forms, and feature-specific service layer. Shared models and cross-feature services remain centralized.

## Layers

### Application factory

`app.create_app` initializes Flask and shared extensions: SQLAlchemy, Flask-Login, Flask-Migrate, and CSRF protection. It registers all feature blueprints during startup, installs default `/` and `/health` routes, configures error handlers, and creates missing SQLite database tables for the foundation schema.

### Routes

Routes live in `app/<feature>/routes.py`. They should remain thin and only handle HTTP concerns: reading request data, invoking services, selecting templates, redirecting, and returning responses. Implemented business modules expose authenticated pages backed by repositories and services; routes remain responsible for HTTP coordination only.

### Services

Services hold business logic. Feature-specific services live in `app/<feature>/service.py`; cross-feature services live in `app/services`. Current services are:

- `ClientService`: client lookup, balance calculation, non-blocking debt warnings, activation, and deactivation.
- `LedgerService`: ledger-entry preparation, posting, balance calculation, recent activity, and filtered ledger listing.
- `DashboardService`: daily counts, revenue, outstanding debt, over-limit clients, recent payments, and recent charges.

### Forms

Feature-specific forms live in `app/<feature>/forms.py` when needed. Shared form components and validators live in `app/forms`. `NonNegativeMoney` is available for future amount fields.

### Models

All database models live under `app/models` to keep the domain schema discoverable and avoid duplicated entity definitions. Models define persistence structure and simple helpers only; workflow decisions stay in services.

### Templates and static assets

Templates are grouped by feature under `app/templates`. Shared page shells live in `app/templates/layouts`; reusable touch-first fragments live in `app/templates/components`. Static assets live under `app/static/css`, `app/static/js`, and `app/static/images`.

## Dependency direction

Routes may depend on forms and services. Services may depend on models and utilities. Models should not depend on routes or request-specific code.

## Foundation decisions

- Debt-limit checks return warnings and never block transactions.
- Ledger posting is deliberately unimplemented only through transaction services.
- The global UI is optimized for Windows 7 touchscreen use: large controls, high contrast, simple navigation, and no required hover interactions.


## Startup and Docker

`python run.py` starts the development server on `0.0.0.0:5000` with debug reload enabled by default. The startup banner prints the application name, environment, database URI, listening address, and loaded blueprints. Docker uses the same entrypoint and the `/health` endpoint for container health checks.

## Authentication

Flask-Login protects dashboard and module routes. Administrator and cashier credentials can be changed from Settings for the running deployment.

## Repositories

Database access for MVP workflows is centralized in `app/repositories/core.py`. Feature services use repositories for queries and persistence while routes stay thin and focused on request/response coordination.

## MVP modules

Clients, breakfast, lunch, manual charges, payments, ledger, dashboard, and settings now have working authenticated pages. Transaction services post ledger entries immediately after their source record is flushed so balances, filtering, and dashboard metrics stay consistent.

## Production hardening architecture

- Authentication is database-backed through the centralized `User` model and `app.auth.service`.
- Authorization is enforced server-side through `app.permissions.permission_required`; navigation visibility is only a UI convenience and not the security boundary.
- Localization is intentionally lightweight in `app.i18n`, selecting French LTR for administrators and Arabic RTL for cashiers.
- Supplier expenses use the charges module but are modeled independently from client ledger entries.
- Audit logging is centralized in `app.audit.log_audit` and stored in `AuditLog` for administrator review.

## Localization and authorization refinement

Localization now uses the `app/i18n` package with key-based translations and role-aware language selection. Administrator pages default to French/LTR and cashier pages default to Arabic/RTL. Templates receive `_`, `weekday_key`, `ui_lang`, and `ui_dir` from the application context.

Authorization uses named permissions such as `lunch.manage`, `payments.create`, and `dangerous.delete`. Legacy route aliases are normalized for backward compatibility, but server-side decorators remain the security boundary.

## Identity settings and ledger export

The key/value `settings` table remains the source for organization identity. `SettingsService.identity()` normalizes defaults for templates, and the base layout maps configured colors to CSS variables instead of scattering inline color values. Logos are saved under `app/static/uploads/` and referenced by their static relative path.

Ledger export is implemented in the ledger blueprint as an admin-protected CSV endpoint. It reuses `LedgerService.list_entries()` so exported rows and on-screen filters follow the same query behavior. Export actions are written to `AuditLog` through the centralized audit helper.
