# Development Log

## 2026-06-30

- Created initial project organization for Buvette Manager.
- Added feature modules for auth, dashboard, clients, breakfast, lunch, charges, payments, ledger, and settings.
- Added centralized folders for models, shared services, forms, templates, static assets, and utilities.
- Added initial documentation set: project state, architecture, database, business rules, UI guidelines, and development log.
- Added minimal Flask application factory, configuration, environment example, requirements, and development entrypoint.
- Revised the initial scaffold to remove premature runnable placeholder endpoints and blueprint wiring so the repository remains strictly in the organization phase before feature implementation.
- Implemented the reusable domain foundation: SQLAlchemy extension, application factory, `User`, `Client`, and `LedgerEntry` models.
- Added `ClientService`, `LedgerService`, and `DashboardService` interfaces without implementing full business workflows.
- Added constants, formatting helpers, weekday helpers, validation helpers, and shared WTForms money validation.
- Added the additive SQL migration `0001_domain_foundation.sql` for users, clients, and ledger entries.
- Added a touch-first base layout, reusable UI components, global CSS design system, and minimal framework-free JavaScript utilities.
- Updated documentation to record the domain rules, database impact, UI decisions, and future extension points.


## 2026-07-01

- Completed the runnable application foundation without replacing the existing feature-module architecture.
- Updated `run.py` so `python run.py` starts Flask on `0.0.0.0:5000`, enables development debug/reload behavior, and prints a startup banner.
- Initialized SQLAlchemy, Flask-Login, Flask-Migrate, and CSRF protection in the application factory.
- Registered all existing feature blueprints and added safe placeholder pages for unfinished modules.
- Added default `/` routing by authentication state and a JSON `/health` endpoint for future Docker health checks.
- Added temporary administrator and cashier login/logout flow to verify protected navigation.
- Completed the base layout with header, sidebar navigation, flash messages, content area, footer, Bootstrap assets, and local static assets.
- Added reusable custom error pages for 400, 403, 404, and 500 responses.
- Added Dockerfile, Compose configuration, and `.dockerignore` so the container runs in the foreground on port 5000.
- Documented startup, database initialization, Docker, and authentication foundation decisions.
- Added local Flask-Login and Flask-Migrate compatibility shims so the foundation remains runnable in restricted offline environments while retaining the same extension APIs.
