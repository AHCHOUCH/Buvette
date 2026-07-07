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

## Weekly lunch menus

Lunch menus are now organized by week. A `WeeklyMenu` owns seven `DailyMenu` rows, each day can contain multiple `FoodPlate` rows, and each plate has active/inactive `FoodPlateVariant` price options. Default variants are small (`Petit / صغير`, 20 DH) and big (`Grand / كبير`, 25 DH). Cashiers must select a client, plate, and variant before charging lunch. If no active menu exists for today, the UI shows a translated warning and no silent charge is created.

## Dashboard metrics

Dashboard average activity metrics use the last 30 days as the default period: breakfast orders per day, lunch orders per day, client payments per day, and supplier expenses per day.

## MVP closure rules

- Weekly lunch service days are Monday through Friday. Saturday and Sunday are closed and displayed as closed in cashier and menu screens.
- New lunch orders use `food_plate_id`, `variant_id`, and snapshot fields as the source of truth; legacy `menu_id` is nullable for compatibility only.
- Dropdown client selection is the reliable MVP selector for breakfast, lunch, and payments.
- Empty or invalid selected IDs are validation errors and must not create traceback pages.
- Historical lunch order amounts and labels remain unchanged after a variant price or label is edited.

## Organization identity and ledger export rules

- Organization name is the official display name for page titles, header, login, dashboard layout context, and ledger export metadata; blank values fall back to Buvette Manager.
- Currency is configurable and defaults to DH. Exported monetary columns remain numeric; currency is declared in CSV metadata instead of mixed into amount cells.
- Ledger export is a finance action requiring ledger permission. In the default roles, administrators may export and cashiers may not.
- Every ledger export must create an audit log entry with scope/filter metadata and row count.

## Functional refinement: products, expenses, dashboards, lunch, and ledger

- Administrators can create, edit, deactivate/archive, and safely delete unused products with password confirmation; used products remain protected to preserve order snapshots.
- Cashiers may create buvette supplier expenses through the expenses workflow while supplier expenses remain separate from client balances.
- The cashier dashboard is intentionally simplified to operational counts, payments, expenses created today, and quick actions; the admin dashboard keeps financial analytics and supports `daily`, `weekly`, `monthly`, and `3months` periods.
- Lunch charging uses active plate variants configured on the weekly menu and stores the selected label/price snapshot. Active drink or lunch-extra products can be added with quantities and are included in the single lunch debit.
- The client ledger remains balance-only for breakfast, lunch, and payments. The global ledger/report combines client income rows and supplier expense rows with income, expense, and net totals plus CSV export.
- The application header now uses left/center/right zones so the logo and organization name stay visually centered in LTR and RTL layouts.
- RTL pages use logical spacing and overflow guards so Arabic back buttons stay inside the viewport without horizontal page scroll.
- Apply `migrations/0007_functional_refinement.sql` on existing databases before deployment.
