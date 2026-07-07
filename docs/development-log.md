# Development Log

## 2026-06-30

- Created initial project organization for Buvette Manager.
- Added feature modules for auth, dashboard, clients, breakfast, lunch, charges, payments, ledger, and settings.
- Added centralized folders for models, shared services, forms, templates, static assets, and utilities.
- Added initial documentation set: project state, architecture, database, business rules, UI guidelines, and development log.
- Added minimal Flask application factory, configuration, environment example, requirements, and development entrypoint.
- Revised the initial scaffold to remove premature runnable early endpoints and blueprint wiring so the repository remains strictly in the organization phase before feature implementation.
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
- Registered all existing feature blueprints and added protected working pages for the MVP modules.
- Added default `/` routing by authentication state and a JSON `/health` endpoint for future Docker health checks.
- Added temporary administrator and cashier login/logout flow to verify protected navigation.
- Completed the base layout with header, sidebar navigation, flash messages, content area, footer, Bootstrap assets, and local static assets.
- Added reusable custom error pages for 400, 403, 404, and 500 responses.
- Added Dockerfile, Compose configuration, and `.dockerignore` so the container runs in the foreground on port 5000.
- Documented startup, database initialization, Docker, and authentication foundation decisions.
- Added local Flask-Login and Flask-Migrate compatibility shims so the foundation remains runnable in restricted offline environments while retaining the same extension APIs.

## 2026-07-01 MVP completion

- Added MVP SQLAlchemy models for breakfast products/orders, lunch menus/orders, manual charges, payments, and settings.
- Added repository classes for client, ledger, breakfast, lunch, charge, payment, and settings persistence.
- Implemented client CRUD, search, archive/restore, balance display, outstanding badges, and non-blocking debt warnings.
- Implemented touchscreen breakfast ordering, product management, lunch charging, menu administration, manual charges, cash payments, ledger filtering, dashboard metrics, and settings editing.
- Added additive SQL migration `0002_mvp.sql` and startup seed data for immediate use after deployment.
- Added automated unittest coverage for authentication, clients, breakfast, lunch, charges, payments, ledger, dashboard, and settings.

## 2026-07-01 production hardening

- Replaced fixed in-memory demo authentication with database-backed users, password hashes, last-login tracking, and administrator/cashier roles.
- Added backend permission helpers, explicit protected route decorators, localized French administrator navigation, Arabic RTL cashier shell behavior, and a clean 403 path.
- Added suppliers, supplier expenses, supplier archive/delete-with-password flows, and separated supplier charges from client ledger balances.
- Added audit logs for authentication, authorization failures, user management, suppliers, dangerous actions, and supplier charge creation with an administrator log viewer.
- Added automatic client employee number generation using `EMP-0001` style identifiers when the administrator leaves the field blank.
- Fixed numeric keypad decimal behavior: first decimal becomes `0.`, duplicate decimals are ignored, digits append, backspace removes one character, and clear empties the field.
- Updated tests for database users, permissions, localization direction, audit logs, employee number generation, supplier expenses, and ledger separation.

## 2026-07-01 production refinement continuation

- Added key-based i18n package with French administrator and Arabic cashier translations for navigation, buttons, weekdays, dashboard, lunch, client selection, errors, and common fields.
- Added weekly lunch menu models with daily menus, food plates, variants, default small/big prices, and lunch order snapshots.
- Reworked lunch routes and templates to support week creation, plate creation, copy-previous-week workflow, and touch-friendly plate/variant charging.
- Grouped navigation by role and permission, changed default currency to DH, improved dashboard metrics, and extended numeric keypad/client selector JavaScript.
- Added migration `0004_weekly_menu_i18n_permissions.sql` and documented ledger separation and 30-day dashboard averages.

## 2026-07-01 MVP closure pass

- Made `lunch_orders.menu_id` legacy/nullable for weekly plate and variant orders, with migration `0005_mvp_closure.sql` documenting the SQLite table rebuild.
- Replaced fragile card/hidden client selection on cashier meal/payment flows with standard dropdowns and safe integer parsing to prevent `int("")` tracebacks.
- Simplified lunch cashier flow to client, plate, variant, confirm; Saturday and Sunday are closed and do not require menu setup.
- Completed weekly menu editing for working days, including plate and variant activation, labels, and prices while preserving lunch order snapshots.
- Added translated UI strings for closure screens, logs, breakfast, payments, and menu actions; admin remains French/LTR and cashier Arabic/RTL.
- Lightened the application theme and documented the final pilot limitations.

## 2026-07-07 identity/settings/export refinement

- Converted administrator settings UI to French labels, messages, and validation feedback through i18n keys.
- Added functional organization identity settings, safe logo upload, CSS-variable theming, and dynamic layout/login branding.
- Removed visible debug/default credentials from the login page while documenting them for development use.
- Added protected ledger CSV export for all rows or current filters, with UTF-8 BOM, organization/currency metadata, and audit logging.
- Added migration `0006_identity_settings_ledger_export.sql` for new identity setting keys.
