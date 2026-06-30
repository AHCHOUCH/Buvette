# UI Guidelines

Buvette Manager's UI is simple, consistent, high contrast, and optimized for Windows 7 touchscreen operation.

## Layout

- Shared page layouts belong in `app/templates/layouts`.
- Feature templates belong in their matching feature template directory.
- Reusable fragments belong in `app/templates/components`.
- Navigation exposes dashboard, clients, breakfast, lunch, charges, payments, ledger, and settings.

## Interaction principles

1. Common workflows should require as few taps as practical.
2. Financial actions should provide clear confirmation and feedback.
3. Validation errors should explain how to correct the input.
4. Balance-affecting screens should show the relevant client and amount prominently.
5. Avoid hover-only interactions.
6. Minimize typing; prefer search, selections, large buttons, and clear defaults.

## Design system

Global styling lives in `app/static/css/app.css` and defines colors, spacing, font sizes, touch target sizes, cards, tables, forms, alerts, modals, and buttons. Future pages should reuse these variables and classes instead of adding one-off styles.

## Components

The foundation includes reusable components for buttons, cards, modals, search boxes, confirmation dialogs, alert banners, empty states, table toolbars, and flash messages.

## JavaScript

Global JavaScript lives in `app/static/js/app.js`. It provides reusable utilities only: confirmation helper, autofocus behavior, debounced search events, and notification helper. No JavaScript framework or jQuery is used.
