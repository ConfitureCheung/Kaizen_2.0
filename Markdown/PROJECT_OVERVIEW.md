# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, and Insight sections, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse.
The Profile, Client, Groups, Users, Dashboard, left panel, Django admin, Vault, and **Insight sections are all functionally complete**. The **next active focus is the Energy & Report section** — five new pages: `energy_overview.html`, `energy_detail.html`, `report_list.html`, `report_detail.html`, and `report_export.html`. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `myportal/core/views.py` — add five Energy & Report view stubs.
- `myportal/core/urls.py` — add URL patterns under `/energy/` and `/reports/`.
- `myportal/templates/core/` — all new Energy & Report templates live here, extending `base.html` or `base2.html`.
- `static/css/app.css` already defines the app’s visual language; no new CSS files are needed.

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
| Insight | `insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html` | ✅ Complete (layout-first) |
| Energy | `energy_overview.html`, `energy_detail.html` | 🔲 Next (in progress) |
| Reports | `report_list.html`, `report_detail.html`, `report_export.html` | 🔲 Next (in progress) |

## Energy & Report section — planned work
The Energy & Report section introduces the energy monitoring and reporting layer of the BLENDY portal. The first stage is layout-only using static/sample data; backend wiring follows in a subsequent step.

Planned pages:

- **`energy_overview.html`** — Energy section landing page. Shows building-scoped energy KPI cards (consumption, cost, benchmark), a time-series trend chart placeholder, and a period selector (daily/weekly/monthly).
- **`energy_detail.html`** — Detailed energy breakdown page. Drills into specific energy meters or systems (HVAC, lighting, etc.) with a table of meter readings and a chart placeholder. Uses a split-panel layout.
- **`report_list.html`** — Report library landing page. Lists generated reports as table rows: report name, type, building, date generated, status badge, and action buttons.
- **`report_detail.html`** — Individual report view. Shows report metadata and a structured content area with section headings, data tables, and chart placeholders.
- **`report_export.html`** — Report export/generation form. Fields: report type, building, date range, output format (PDF/CSV/Excel).

## Insight section — completed state
The Insight section is fully implemented (layout-first stage):
- **`insight_management_view`** — section landing page showing a list of insight reports.
- **`create_insight_report_view`** — form page to create a new Insight Report.
- **`manage_rules_view`** — rule management list page.
- **`golden_standard_configuration_view`** — configuration page for Golden Standard reference values.
- **`insight_subscription_view`** — subscription management page.
- **URL patterns** — `/insight/`, `/insight/create/`, `/insight/rules/`, `/insight/golden-standard/`, `/insight/subscriptions/` are all registered in `core/urls.py`.
- All five templates extend `base2.html`, use static/sample data, and share consistent sub-navigation tabs.

## Vault section — completed state
The Vault section is fully implemented:
- **`trend_log_view`** — resolves the active building from `building_pk`, opens the linked SQLite database with raw `sqlite3`, queries the Trend Log table, and passes rows to the template.
- **`objects_view`** — same pattern, queries the Objects table.
- **`trend_log.html`** — list-view template extending `base2.html`.
- **`objects.html`** — split-panel list/detail template extending `base2.html`.
- **URL patterns** — `/vault/<int:building_pk>/trend-logs/` and `/vault/<int:building_pk>/objects/` are registered in `core/urls.py`.

## Django admin — completed state
Django admin is fully consistent with the frontend portal view:
- **`core/admin.py`** — complete `ModelAdmin` classes for all core models with full `list_display`, `list_filter`, `search_fields`, `fieldsets`, `readonly_fields`, and display helpers.
- **`static/css/admin_custom.css`** — BLENDY design token overrides applied to Django admin CSS variables.
- **Admin branding** — `site_header`, `site_title`, and `index_title` are set to the BLENDY product name.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `myportal/core/views.py` — add five Energy & Report view stubs.
- `myportal/core/urls.py` — add URL patterns under `/energy/` and `/reports/`.
- `myportal/templates/core/energy_overview.html` — new Energy landing page.
- `myportal/templates/core/energy_detail.html` — new Energy detail page.
- `myportal/templates/core/report_list.html` — new Report list page.
- `myportal/templates/core/report_detail.html` — new Report detail page.
- `myportal/templates/core/report_export.html` — new Report export form page.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
