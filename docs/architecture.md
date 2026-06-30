# Architecture

Buvette Manager uses a feature-module architecture. Each feature owns its routes, feature-specific forms, and feature-specific service layer. Shared models and cross-feature services remain centralized.

## Layers

### Routes

Routes live in `app/<feature>/routes.py`. They should remain thin and only handle HTTP concerns: reading request data, invoking services, selecting templates, redirecting, and returning responses. During the current organization phase, route files are placeholders and must not define endpoints until the associated feature module is approved for implementation.

### Services

Services hold business logic. Feature-specific services live in `app/<feature>/service.py`; cross-feature services live in `app/services`. If a service grows too large or covers multiple responsibilities, split it into smaller modules before it becomes difficult to maintain.

### Forms

Feature-specific forms live in `app/<feature>/forms.py` when needed. Shared form components and validators live in `app/forms`.

### Models

All database models live under `app/models` to keep the domain schema discoverable and avoid duplicated entity definitions.

### Templates and static assets

Templates are grouped by feature under `app/templates`. Shared page shells live in `app/templates/layouts`. Static assets live under `app/static/css`, `app/static/js`, and `app/static/images`.

## Initial feature modules

- Authentication
- Dashboard
- Clients
- Breakfast
- Lunch
- Charges
- Payments
- Ledger
- Settings

## Dependency direction

Routes may depend on forms and services. Services may depend on models and utilities. Models should not depend on routes or request-specific code.

## Feature implementation workflow

Each new feature must remain inside its own module. Before writing code for a module, document the design, architectural fit, and required database changes. After implementation, update project documentation with new routes, models, services, database changes, business rules, UI decisions, and future TODOs.
