# Database Design

The database schema has not been implemented yet. Models will be centralized under `app/models`, and migrations will live under `migrations` once migration tooling is initialized. The current project-organization phase introduces no database changes.

## Expected core entities

- User: authenticated application user.
- Client: person or account receiving meals and charges.
- Meal item: breakfast or lunch item available for billing.
- Charge: amount owed by a client for meals or other billable activity.
- Payment: amount paid by a client.
- Ledger entry: normalized transaction record used to calculate balances.
- Setting: operational configuration values.

## Initial database rules

1. Ledger balances should be derived from immutable charge and payment history whenever possible.
2. Payments must be traceable to the client and recording user.
3. Charges must identify the source workflow, such as breakfast, lunch, or manual charge.
4. Deletions of financial records should be avoided; prefer reversal or adjustment entries.

## Migration policy

Every schema change must include a migration and an update to this document describing the intent and impact of the change. Before implementing a feature, the required database changes must be explained; if none are required, that must be stated explicitly.
