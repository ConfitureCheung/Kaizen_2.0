# TASK

## Current task
Build the **Vault section** — Trend Logs (`trend_log.html`) and Objects (`objects.html`) pages.

## Immediate objective
Create two new building-scoped list-view pages that read data directly from the per-building SQLite database (linked via `BuildingDatabase.db_file`) using raw `sqlite3` connections — no new Django models or migrations. Both pages must fit seamlessly into the existing BLENDY portal shell and visual language.

Specific targets:
- **`trend_log_view`** in `core/views.py` — resolves the active building from the URL (`building_pk`), opens the linked SQLite database with `sqlite3`, queries the Trend Log table, and passes rows + column names to the template as context. Gracefully handles the no-database case.
- **`objects_view`** in `core/views.py` — same pattern as above but queries the Objects table.
- **`trend_log.html`** — list-view template extending `base.html`. Table columns: name, description, object reference, units, timestamps. Top search/filter bar. Empty state if no database is linked. Consistent with `users.html` / `clients.html` visual pattern.
- **`objects.html`** — list-view template extending `base.html`. Table columns: object type, instance, name, description, present value, units. Top search/filter bar. Empty state if no database is linked. Consistent with same visual pattern.
- **URL patterns** — add `/vault/<int:building_pk>/trend-logs/` and `/vault/<int:building_pk>/objects/` to `core/urls.py`.

## Background from the previous step
Django admin consistency is now complete:
- `core/admin.py` has fully configured `ModelAdmin` classes for `Client`, `ClientGroup`, `Building`, `BuildingUser`, and `BuildingDatabase` with `list_display`, `list_filter`, `search_fields`, `fieldsets`, `readonly_fields`, display helpers, and `save_model` overrides.
- `static/css/admin_custom.css` applies BLENDY design tokens to Django admin CSS variables.
- Admin branding (`site_header`, `site_title`, `index_title`) is set.
- `accounts/admin.py` is configured for the custom user model.

## Scope for the next coding round

**In scope:**
- `myportal/core/views.py` — add `trend_log_view` and `objects_view`.
- `myportal/core/urls.py` — add URL patterns for both new views under `/vault/<building_pk>/`.
- `templates/vault/trend_log.html` — new Trend Logs list template (or `templates/trend_log.html` if flat template layout is preferred).
- `templates/vault/objects.html` — new Objects list template.

**Out of scope for this round:**
- Any changes to `admin.py` files or `admin_custom.css`.
- Changes to `static/css/app.css` or `static/js/app.js`.
- New Django models or migrations.
- Refactoring of existing views, URLs, or forms.
- Buildings, Dashboard, Groups, Users, Clients, Profile pages.

## Starting point
- Review `core/models.py` to confirm the `BuildingDatabase` model fields — specifically `db_file` (the SQLite file path) and its relation to `Building`.
- Review `users.html` and `clients.html` for the exact list-view HTML/CSS pattern to replicate in the new templates.
- Review `core/views.py` for the existing view signature conventions (login_required, client resolution, context dict structure).
- The building SQLite database has its own internal schema; inspect the actual `.sqlite3` file (or `create_sample_building_db.py`) to confirm the Trend Log and Objects table names and columns before writing queries.

## Expected deliverables
1. Updated `core/views.py` with `trend_log_view` and `objects_view`.
2. Updated `core/urls.py` with two new URL patterns under `/vault/<building_pk>/`.
3. New `templates/vault/trend_log.html` — Trend Logs list page.
4. New `templates/vault/objects.html` — Objects list page.
5. No changes to any other files.

## Acceptance criteria
- Both pages render inside the shared BLENDY shell (navbar, breadcrumb, left panel) correctly.
- Table data is populated from the linked building SQLite database via raw `sqlite3` queries.
- If no `BuildingDatabase` is linked to the building, an informative empty-state card is shown instead of an error.
- Search/filter bar visually present and consistent with other list views (functional filtering is a bonus; static bar is acceptable for the first iteration).
- URL patterns follow the convention `/vault/<building_pk>/trend-logs/` and `/vault/<building_pk>/objects/`.
- No regressions in any existing pages.
- `app.css` and all admin files are untouched.
