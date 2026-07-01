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

## Production hardening rules

- Administrators can manage dashboard, clients, breakfast products, lunch menus, suppliers, supplier charges, payments, ledger, settings, users, logs, archive, and guarded delete actions.
- Cashiers can use operational screens only: dashboard, breakfast ordering, lunch charging, payments, client selection, and basic balance visibility. They cannot access settings, users, logs, system configuration, password management, or dangerous delete routes.
- Supplier charges are buvette expenses. They never require a client, never post to the client ledger, and never change client balances.
- Client ledger history is limited to breakfast debits, lunch debits, and payment credits.
- Archive is the normal safe removal operation. Dangerous delete requires an administrator password, writes an audit log, and is blocked for records with financial history.
- Employee numbers are generated automatically when blank, using a simple `EMP-0001` style sequence; administrators may still override with a unique value.
- Amount keypads keep valid decimal input: blank plus `.` becomes `0.`, a second `.` is ignored, backspace deletes one character, and clear empties the field.
