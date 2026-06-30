# Business Rules

This document records operational rules for Buvette Manager. It must be updated whenever behavior changes.

## Financial records

- Charges increase a client's balance.
- Payments decrease a client's balance.
- Ledger entries should provide a complete audit trail for balance-affecting events.
- Financial records should favor corrections through adjustments rather than destructive edits.

## Meal workflows

- Breakfast and lunch are separate feature modules because they may evolve distinct menus, pricing, cutoff times, and reporting needs.
- Meal-related charges should be created through services so pricing and ledger effects remain consistent.

## Client accounts

- Each client should have a clear account status.
- Client balance should be calculated from ledger activity rather than manually maintained unless a documented optimization is introduced.

## Authentication and permissions

Authentication is planned but not implemented. Future permission rules should define which users can manage settings, record payments, modify charges, and view ledger data.


## Documentation maintenance

When a feature changes business behavior, this document must be updated in the same change set. New rules should identify the affected module, route or service, and any ledger or client-balance impact.
