# Business Rules

This document records operational rules for Buvette Manager. It must be updated whenever behavior changes.

## Client accounts

- Each client has an active/inactive status.
- Inactive clients should be hidden or discouraged in future workflows, but exact workflow behavior must be defined when those workflows are implemented.
- Current balance is calculated from ledger activity.
- Debt limit is a review threshold, not a hard stop.
- Debt-limit warnings are non-blocking: cashiers can continue, and administrators review excessive balances later.

## Financial records

- Charges increase a client's balance.
- Payments decrease a client's balance.
- Ledger entries provide the reusable audit trail for balance-affecting events.
- Ledger entries support debit, credit, running balance, reference data, and timestamp.
- Financial records should favor corrections through adjustments rather than destructive edits.
- Ledger posting is not implemented yet; only preparation and balance calculation helpers exist.

## Meal workflows

- Breakfast and lunch are separate feature modules because they may evolve distinct menus, pricing, cutoff times, and reporting needs.
- Meal-related charges should be created through services so pricing and ledger effects remain consistent.
- Breakfast and lunch workflows are not implemented in the foundation phase.

## Authentication and permissions

Authentication is planned but not implemented. Constants exist for administrator and cashier roles. Future permission rules should define which users can manage settings, record payments, modify charges, and view ledger data.

## Documentation maintenance

When a feature changes business behavior, this document must be updated in the same change set. New rules should identify the affected module, route or service, and any ledger or client-balance impact.
