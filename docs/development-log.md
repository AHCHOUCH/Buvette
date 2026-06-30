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
