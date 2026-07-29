# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, and the Vault section, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse.
The Profile page, Client pages, Groups pages (fully client-scoped), Users pages, Dashboard, sliding left panel, Django admin consistency, and **Vault section (Trend Logs + Objects) are all functionally complete**. The **next active focus is the Insight section** — five new pages: `insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, and `insight_subscription.html`. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `myportal/core/views.py` — add five Insight view stubs.
- `myportal/core/urls.py` — add URL patterns under `/insight/`.
- `myportal/templates/core/` — all new Insight templates live here, extending `base.html` or `base2.html`.
- `static/css/app.css` already defines the app's visual language; no new CSS files are needed for Insight pages.

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
| Vault | `trend_log.html`, `objects.html` | ✅ Complete |
| Insight | `insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html` | 🔲 In progress (next) |

## Insight section — planned work
The Insight section introduces the analytics and rules engine layer of the BLENDY portal. The first stage is layout-only using static/sample data; backend wiring follows in a subsequent step.

Planned pages:

- **`insight_management.html`** — section landing page. Lists existing insight reports as summary cards or table rows (title, building, rule count, last run, status). Provides entry points to create a new report or manage existing ones.
- **`create_insight_report.html`** — form/wizard page to create a new Insight Report. Captures report name, linked building, date range, and selected rule sets.
- **`manage_rules.html`** — rule management list page. Displays all insight rules (name, description, category, severity, active/inactive). Allows toggling, editing, or adding rules.
- **`golden_standard_configuration.html`** — configuration page for Golden Standard reference values. Sets expected setpoints, thresholds, and acceptable ranges per building or object type, used as the benchmark for rule evaluation.
- **`insight_subscription.html`** — subscription management page. Users subscribe or unsubscribe to scheduled report deliveries, configure frequency (daily/weekly/monthly), and manage recipient lists.

## Vault section — completed state
The Vault section is fully implemented:
- **`trend_log_view`** — resolves the active building from `building_pk`, opens the linked SQLite database with raw `sqlite3`, queries the Trend Log table, and passes rows to the template. Handles the no-database case with an empty-state card.
- **`objects_view`** — same pattern, queries the Objects table.
- **`trend_log.html`** — list-view template extending `base2.html`. Filterable/searchable table of trend log entries with sub-navigation tabs for the Vault section.
- **`objects.html`** — split-panel list/detail template extending `base2.html`. Left panel shows a searchable list of BACnet objects; right panel shows the selected object's field details.
- **URL patterns** — `/vault/<int:building_pk>/trend-logs/` and `/vault/<int:building_pk>/objects/` are registered in `core/urls.py`.

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
- `myportal/core/views.py` — add five Insight view stubs.
- `myportal/core/urls.py` — add URL patterns under `/insight/`.
- `myportal/templates/core/insight_management.html` — new Insight landing page.
- `myportal/templates/core/create_insight_report.html` — new Create Report form page.
- `myportal/templates/core/manage_rules.html` — new Rules management list page.
- `myportal/templates/core/golden_standard_configuration.html` — new Golden Standard config page.
- `myportal/templates/core/insight_subscription.html` — new Subscription management page.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
