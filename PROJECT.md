# Buvette Manager Project State

`PROJECT.md` is the authoritative source for the current state of Buvette Manager. Future development should update this document whenever structure, behavior, business rules, or technical decisions change.

## Current phase

The project is in the MVP phase. The repository contains the modular project structure, an operational Flask application factory, registered feature blueprints, centralized SQLAlchemy models, repositories, reusable domain services, authentication, Docker support, and a touch-first UI for daily buvette operations.

## Application structure

- `app/auth`: authentication and session management.
- `app/dashboard`: landing page and operational overview service interface.
- `app/clients`: client records and account status service interface.
- `app/breakfast`: breakfast product administration and touchscreen ordering workflows.
- `app/lunch`: weekly lunch menu administration and daily lunch charging.
- `app/charges`: manual miscellaneous charge entry.
- `app/payments`: cash payment recording and payment history.
- `app/ledger`: ledger preparation and balance services.
- `app/settings`: application configuration, products, menus, and password management entry points.
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
6. Services expose stable interfaces and repositories centralize database access.

## Implementation status

- Project directories: created.
- Application factory, SQLAlchemy, Flask-Login, Flask-Migrate, and CSRF initialization: implemented.
- Feature route modules: registered with protected working pages for clients, breakfast, lunch, charges, payments, ledger, dashboard, and settings.
- Models: users, clients, ledger entries, breakfast products/orders, lunch menus/orders, manual charges, payments, and settings implemented.
- Database migrations: `0001_domain_foundation.sql` and `0002_mvp.sql` document additive table creation.
- Services and repositories: client, ledger, dashboard, breakfast, lunch, charges, payments, and settings workflows implemented.
- Templates/static assets: touch-first base layout, navigation, login, dashboard, CRUD and transaction pages, reusable components, design-system CSS, Bootstrap loading, and minimal JavaScript utilities implemented.
- Default routes: `/` redirects by authentication state and `/health` returns `{"status": "ok"}` for Docker health checks.
- Docker: `Dockerfile`, `docker-compose.yml`, and `.dockerignore` added for foreground startup on port 5000.
- Tests: unittest MVP flow coverage implemented for authentication, dashboard, clients, transactions, ledger, and settings.

## Development workflow

For future changes:

1. Keep routes thin and place business behavior in services.
2. Add or update repositories for database access.
3. Explain required database changes and add an additive migration when schema changes.
4. Update tests and documentation in the same change set.
5. Preserve touchscreen-first UI conventions.

## Production hardening update

The application now includes database-backed users, role permissions, French/Arabic role-aware UI shell behavior, supplier expenses, audit logs, automatic employee numbers, guarded archive/delete patterns, and corrected numeric keypad decimal input. Supplier charges are expenses and are intentionally excluded from client balances and client ledger entries.

## Final MVP closure pass

The branch now prioritizes reliable pilot operation: dropdown selectors replace fragile hidden client cards, weekly lunch orders no longer depend on legacy `menu_id`, Saturday/Sunday are closed by default, weekly plate/variant editing is available, historical lunch snapshots are preserved, the UI theme is lighter, and closure migration/deployment notes are documented.

## 2026-07 identity/settings/export refinement

- Settings are now the source of truth for organization name, short name, logo path, visual colors, footer text, and currency.
- The base layout exposes identity colors through CSS variables and uses the configured name/logo in titles, header, footer, and login.
- Login no longer displays development credentials in any mode; credentials are documented only for local development.
- Ledger CSV export supports complete and filtered exports and records an audit event.
- Migration `0006_identity_settings_ledger_export.sql` seeds the new key/value settings for existing SQLite databases.

## Functional refinement: products, expenses, dashboards, lunch, and ledger

- Administrators can create, edit, deactivate/archive, and safely delete unused products with password confirmation; used products remain protected to preserve order snapshots.
- Cashiers may create buvette supplier expenses through the expenses workflow while supplier expenses remain separate from client balances.
- The cashier dashboard is intentionally simplified to operational counts, payments, expenses created today, and quick actions; the admin dashboard keeps financial analytics and supports `daily`, `weekly`, `monthly`, and `3months` periods.
- Lunch charging uses active plate variants configured on the weekly menu and stores the selected label/price snapshot. Active drink or lunch-extra products can be added with quantities and are included in the single lunch debit.
- The client ledger remains balance-only for breakfast, lunch, and payments. The global ledger/report combines client income rows and supplier expense rows with income, expense, and net totals plus CSV export.
- The application header now uses left/center/right zones so the logo and organization name stay visually centered in LTR and RTL layouts.
- RTL pages use logical spacing and overflow guards so Arabic back buttons stay inside the viewport without horizontal page scroll.
- Apply `migrations/0007_functional_refinement.sql` on existing databases before deployment.
