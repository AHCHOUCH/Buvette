# Buvette Manager

Buvette Manager is a modular web application for managing clients, meals, charges, payments, and ledger activity for a buvette operation.

The project is intentionally organized by feature area so route handlers, forms, and business services can evolve independently while shared models remain centralized.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py run
```

See `PROJECT.md` for the authoritative current project state and `docs/` for architecture, database, business rules, UI guidelines, and development history.
