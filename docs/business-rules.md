# Business Rules

This document records operational rules for Buvette Manager. It must be updated whenever behavior changes.

## Client accounts

- Each client has an active/inactive status.
- Inactive clients are archived and excluded from normal transaction selectors; they can be restored from the client list.
- Current balance is calculated from ledger activity.
- Debt limit is a review threshold, not a hard stop.
- Debt-limit warnings are non-blocking: cashiers can continue, and administrators review excessive balances later.

## Financial records

- Charges increase a client's balance.
- Payments decrease a client's balance.
- Ledger entries provide the reusable audit trail for balance-affecting events.
- Ledger entries support debit, credit, running balance, reference data, and timestamp.
- Financial records should favor corrections through adjustments rather than destructive edits.
- Ledger posting is performed by breakfast, lunch, manual charge, and payment services after source records are created.

## Meal workflows

- Breakfast and lunch are separate feature modules because they may evolve distinct menus, pricing, cutoff times, and reporting needs.
- Meal-related charges should be created through services so pricing and ledger effects remain consistent.
- Breakfast and lunch workflows create client ledger debits when confirmed by a cashier.

## Authentication and permissions

Authentication supports administrator and cashier users. Authenticated staff can access operational modules; administrator-only permissions can be expanded later when durable user management is introduced.

## Documentation maintenance

When a feature changes business behavior, this document must be updated in the same change set. New rules should identify the affected module, route or service, and any ledger or client-balance impact.

## MVP transaction rules

- Breakfast orders debit the selected client for the sum of product quantities and prices.
- Lunch charges debit the selected client using the configured menu for the current weekday.
- Manual charges debit the selected client and require a positive amount and approved category.
- Cash payments credit the selected client and may be partial payments or overpayments.
- Every balance-affecting event is visible in the chronological ledger.
- Over-limit debt displays a warning badge but does not block purchases.
