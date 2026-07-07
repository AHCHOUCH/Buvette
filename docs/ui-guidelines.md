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

## Tablet production UI additions

- Touch targets must be at least 56px high; primary transaction buttons and keypad buttons should be 64px or larger.
- Administrator screens use French labels and LTR layout. Cashier screens use Arabic labels where provided and RTL layout.
- Active navigation state must be visually obvious and not rely on hover.
- Login uses a centered card, large fields, a large submit button, and shows default test credentials only when Flask debug mode is enabled.
- Numeric amount fields should use the shared keypad behavior in `app/static/js/app.js`.

## Touch client selector

Cashier lunch workflows use large searchable client cards instead of small dropdowns. Client cards support name and employee-number filtering, single-tap selection, and visible selected state. Shared numeric keypad logic supports all amount inputs: empty plus decimal becomes `0.`, duplicate decimals are ignored, digits append, backspace removes one character, and clear empties the field.

## MVP closure UI

- Main backgrounds use a light neutral surface (`#f6f7f9`) with white cards and a moderate teal header/sidebar accent.
- Cashier selectors use reliable dropdowns for pilot operation. A richer searchable selector is deferred until after workflow stability is proven.
- Lunch cashier screens show only client, today's plate, variant, and confirmation. Weekly editing stays on the menu admin screen.

## Visual identity customization

- Use CSS variables from the base layout for primary, accent, header, sidebar, button, and login background colors.
- Keep defaults light: pale page background, white cards, teal/blue accents, clear active navigation, and large touch targets.
- Display the configured logo where brand context matters, but always keep organization-name text as the fallback.
- Administrator settings screens must remain fully French; cashier operational screens remain Arabic RTL after login.
