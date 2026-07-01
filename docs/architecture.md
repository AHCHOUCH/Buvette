# Architecture

Buvette Manager uses a feature-module architecture. Each feature owns its routes, feature-specific forms, and feature-specific service layer. Shared models and cross-feature services remain centralized.

## Layers

### Application factory

`app.create_app` initializes Flask and shared extensions: SQLAlchemy, Flask-Login, Flask-Migrate, and CSRF protection. It registers all feature blueprints during startup, installs default `/` and `/health` routes, configures error handlers, and creates missing SQLite database tables for the foundation schema.

### Routes

Routes live in `app/<feature>/routes.py`. They should remain thin and only handle HTTP concerns: reading request data, invoking services, selecting templates, redirecting, and returning responses. Unimplemented business modules expose authenticated placeholder pages instead of failing, so navigation remains verifiable while workflows are built incrementally.

### Services

Services hold business logic. Feature-specific services live in `app/<feature>/service.py`; cross-feature services live in `app/services`. Current foundation services are:

- `ClientService`: client lookup, balance calculation, non-blocking debt warnings, activation, and deactivation.
- `LedgerService`: ledger-entry preparation, balance calculation, and a future posting interface.
- `DashboardService`: placeholder methods for today's charges, today's payments, and outstanding balances.

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
- Ledger posting is deliberately unimplemented until the first financial workflow is approved.
- The global UI is optimized for Windows 7 touchscreen use: large controls, high contrast, simple navigation, and no required hover interactions.


## Startup and Docker

`python run.py` starts the development server on `0.0.0.0:5000` with debug reload enabled by default. The startup banner prints the application name, environment, database URI, listening address, and loaded blueprints. Docker uses the same entrypoint and the `/health` endpoint for container health checks.

## Authentication foundation

Flask-Login protects dashboard and module routes. The foundation build includes temporary administrator and cashier accounts for validating session flow; durable user administration remains a later business module.
