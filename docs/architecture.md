# Architecture

Buvette Manager uses a feature-module architecture. Each feature owns its routes, feature-specific forms, and feature-specific service layer. Shared models and cross-feature services remain centralized.

## Layers

### Application factory

`app.create_app` initializes Flask and shared extensions. Blueprints are still not registered because no complete business workflow has been approved yet.

### Routes

Routes live in `app/<feature>/routes.py`. They should remain thin and only handle HTTP concerns: reading request data, invoking services, selecting templates, redirecting, and returning responses. Route files remain placeholders until the associated workflow is approved.

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
