# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse.
The Profile page, Client pages, Groups pages (fully client-scoped), Users pages, Dashboard, sliding left panel, and **Django admin consistency are all functionally complete**. The **next active focus is the Vault section** — `trend_log.html` (Trend Logs) and `objects.html` (Objects). Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `myportal/core/views.py` — add `trend_log_view` and `objects_view` for the Vault section.
- `myportal/core/urls.py` — add URL patterns under `/vault/<building_pk>/`.
- `myportal/core/models.py` — `BuildingDatabase` model provides the path to the per-building SQLite file.
- `templates/` — all new Vault templates must extend `base.html` and follow the existing list-view visual pattern.
- `static/css/app.css` already defines the app's visual language; no new CSS files are needed for Vault pages.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional + client-scoped |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard | `dashboard.html` | ✅ Functional |
| Left panel | Sliding panel in `base.html` | ✅ Functional |
| Django admin | `core/admin.py`, `accounts/admin.py`, `admin_custom.css` | ✅ Complete |
| Vault | `trend_log.html`, `objects.html` | 🔲 In progress (next) |

## Vault section — planned work
The Vault is a building-scoped data viewer that reads directly from the per-building SQLite database linked via `BuildingDatabase.db_file`. It does not use Django ORM models for the building data — all queries are raw `sqlite3` connections.

Planned work includes:

- **`trend_log_view`** — opens the building SQLite database, queries the Trend Log table, and passes records to `trend_log.html` as context. Handles the no-database case with an empty state.
- **`objects_view`** — opens the building SQLite database, queries the Objects table, and passes records to `objects.html` as context. Handles the no-database case with an empty state.
- **`trend_log.html`** — list-view template extending `base.html`. Shows a searchable/filterable table of trend log entries: name, description, object reference, units, and timestamps. Follows the `users.html` / `clients.html` visual pattern.
- **`objects.html`** — list-view template extending `base.html`. Shows a searchable/filterable table of BACnet objects: object type, instance, name, description, present value, and units. Follows the same visual pattern.
- **URL patterns** — `/vault/<int:building_pk>/trend-logs/` and `/vault/<int:building_pk>/objects/` added to `core/urls.py`.

## Django admin — completed state
Django admin is now fully consistent with the frontend portal view:
- **`core/admin.py`** — complete `ModelAdmin` classes for `Client`, `ClientGroup`, `Building`, `BuildingUser`, and `BuildingDatabase` with `list_display`, `list_filter`, `search_fields`, `ordering`, `fieldsets`, `readonly_fields`, computed display helpers (`logo_preview`, `photo_preview`, `db_file_link`, `description_short`), and `save_model` overrides.
- **`static/css/admin_custom.css`** — BLENDY design token overrides applied to Django admin CSS variables (primary colour, font stack, border radius, card/table styles).
- **Admin branding** — `site_header`, `site_title`, and `index_title` are set to the BLENDY product name.

## Groups pages — completed state (client-scoped)
All four Groups screens are fully functional and client-scoped:
- **`groups.html`** — queryset-backed list view filtered to the active client; shows group name, member count, and action buttons.
- **`group_detail.html`** — handles create and edit flows with POST save, permission flag saving, client ownership guard (403 if mismatch), and redirect to `group_saved`.
- **`group_saved.html`** — confirmation screen showing real group context (name, permissions, members) with ownership guard.
- **`group_members.html`** — member-selection screen with checkbox table and POST membership update; enforces client ownership.
- The `ClientGroup` model carries a `ForeignKey` to `Client`; all Group views resolve the active client via `get_active_client` / `get_allowed_client_ids` helpers in `core/sidebar.py`.

## Sliding left panel — completed state
The full interactive behaviour has been implemented:
- **Open/close toggle** — hamburger button triggers a smooth CSS `transform: translateX()` slide-in/out animation.
- **Overlay backdrop** — semi-transparent overlay appears behind the panel when open; clicking it closes the panel.
- **Keyboard dismissal** — pressing `Escape` closes the panel.
- **Tree expand/collapse** — client rows in the panel expand and collapse to show/hide their buildings.
- **Active state highlighting** — the currently visited page's building or client is visually highlighted in the tree.

## Dashboard page — completed state
`dashboard.html` is fully connected to real queryset-backed data:
- **Summary KPI cards** — live counts for active users, clients, buildings, and groups.
- **Recent activity feed** — most recently created or updated records across key models.
- **Client → Building overview** — summary table consistent with the left panel hierarchy.
- **Insight/alert strip** — flagged conditions (users with no group, buildings with no client assignment).
- **Chart widgets** — data visualisations wired to context data from `dashboard_view`.

## Users pages — completed state
Both Users screens are fully functional:
- **`users.html`** — queryset-backed list view showing full name, email, work phone, group badges, and action buttons (edit, activate/deactivate).
- **`user_detail.html`** — handles both create (no `pk`) and edit (with `pk`) flows with POST save, validation feedback, group assignment, and active status toggling.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `myportal/core/views.py` — add `trend_log_view` and `objects_view`.
- `myportal/core/urls.py` — add `/vault/<building_pk>/` URL patterns.
- `templates/vault/trend_log.html` — new Trend Logs list template.
- `templates/vault/objects.html` — new Objects list template.
- `myportal/core/models.py` — reference `BuildingDatabase` for `db_file` path.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
