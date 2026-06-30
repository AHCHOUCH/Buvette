# UI Guidelines

Buvette Manager's UI should be simple, consistent, and optimized for fast operational use.

## Layout

- Shared page layouts belong in `app/templates/layouts`.
- Feature templates belong in their matching feature template directory.
- Navigation should expose dashboard, clients, breakfast, lunch, charges, payments, ledger, and settings.

## Interaction principles

1. Common workflows should require as few clicks as practical.
2. Financial actions should provide clear confirmation and feedback.
3. Validation errors should explain how to correct the input.
4. Balance-affecting screens should show the relevant client and amount prominently.

## Visual style

The initial visual system is not yet implemented. Future styles should be centralized in `app/static/css`, with JavaScript in `app/static/js` only where it improves usability.
