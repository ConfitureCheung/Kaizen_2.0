# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections, and a common visual system in `static/css/app.css` / `app2.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse. Inside a building, `base2.html` provides the building-tab sub-nav with all 8 icons now fully wired: **Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings**.
The Profile, Client, Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, and **Charts, Systems, and Settings/Profile sections are all functionally complete**. The **next active focus is the building-tab Dashboard's content** — `core/building_dashboard.html` (behind the first "Dashboard" icon in `base2.html`) currently renders only an empty layout skeleton and needs real card content per `Layout_Ref/07b_New_Dashboard.png`. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `myportal/templates/core/building_dashboard.html` — fill in the five empty `building-card-body` sections (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts).
- `myportal/core/views.py` — `building_dashboard` view may need extended context (sample building profile fields, chart data, insight counts, energy breakdown, green fact tips).
- `myportal/core/urls.py` — no new routes needed; `/buildings/<int:building_id>/dashboard/` (`building_dashboard`) already exists.
- `Layout_Ref/07b_New_Dashboard.png` — visual mockup for this page (also see `01a_Dashboard.png` / `01a_Dashboard_02.png` for related dashboard styling references).
- `static/css/app2.css` already defines `.building-card` / `.building-card-tall` / `.building-card-wide` tokens for this page; no new CSS files are needed.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional + client-scoped |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard (app-level) | `dashboard.html` | ✅ Functional |
| Left panel | Sliding panel in `base.html` | ✅ Functional |
| Django admin | `core/admin.py`, `accounts/admin.py`, `admin_custom.css` | ✅ Complete |
| Vault | `trend_logs.html`, `objects.html` | ✅ Complete |
| Insight | `insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html` | ✅ Complete (layout-first) |
| Energy | `energy.html` | ✅ Complete |
| Reports | `report.html` | ✅ Complete |
| Charts | `chart.html` | ✅ Complete (layout-first) |
| Systems | `systems.html` | ✅ Complete (layout-first) |
| Settings / Profile icons | `settings_profile.html` | ✅ Complete (layout-first) |
| **Building Dashboard** | `core/building_dashboard.html` | 🔲 **Next (in progress)** — layout skeleton only, no card content yet |

## Building Dashboard — planned work
The next stage builds out the content of `core/building_dashboard.html`, the page behind the first "Dashboard" icon in the `base2.html` building-tab nav. The template currently extends `base2.html` and renders a `building-dashboard-grid` of five `.building-card` sections, but each `building-card-body` is empty. The first stage is layout-first using static/sample data; backend/queryset wiring follows in a subsequent step, consistent with how Vault, Insight, Energy & Report, and Charts/Systems/Settings were staged.

Planned card content, per `Layout_Ref/07b_New_Dashboard.png`:

- **BUILDING PROFILE** — building photo, name, data collection device status, fault detection insight count/progress bar, mini weather widget (multi-day forecast), building address, and embedded location map.
- **DASHBOARD** (chart card) — a report-style chart (e.g. average cooling load / equipment-operation stacked bar with overlay line), similar in spirit to `chart.html`'s chart widgets.
- **INSIGHTS** — total insight count and a short "system with the most insights" list.
- **ENERGY BREAKDOWN (current week)** — labelled kWh breakdown by system (e.g. Chiller Plant).
- **GREEN FACTS** — small rotating tip/fact panel with icon and short text, with pagination indicator.

## Charts, Systems & Settings/Profile section — completed state
The Charts, Systems, and Settings/Profile section is fully implemented (layout-first stage):
- **`building_charts`** — resolves the active building from `pk`, enforces client-access permission, renders `core/chart.html` with `building_tab="charts"`.
- **`building_systems`** — same pattern, renders `core/systems.html` with `building_tab="systems"`.
- **`building_settings_profile`** — same pattern, renders `core/settings_profile.html` with `building_tab="settings"`.
- **URL patterns** — `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, and `/buildings/<int:pk>/settings/profile/` are registered in `core/urls.py`.
- All three templates extend `base2.html`, use static/sample data, and the `base2.html` building-tab nav now links all three with correct `active` state highlighting — no more `href="#"` placeholders remain in the nav.

## Energy & Report section — completed state
The Energy & Report section is fully implemented:
- **`building_energy`** — resolves the active building from `pk`, renders `core/energy.html` with `building_tab="energy"`.
- **`building_reports`** — resolves the active building from `pk`, renders `core/report.html` with `building_tab="reports"`.
- **URL patterns** — `/buildings/<int:pk>/energy/` and `/buildings/<int:pk>/reports/` are registered in `core/urls.py`.
- Both templates extend `base2.html` and are wired into the building-tab sub-nav alongside Vault and Insights.

## Insight section — completed state
The Insight section is fully implemented (layout-first stage):
- **`insight_management`** — section landing page showing a list of insight reports.
- **`create_insight_report`** — form page to create a new Insight Report.
- **`manage_rules`** — rule management list page.
- **`golden_standard_configuration`** — configuration page for Golden Standard reference values.
- **`insight_subscription`** — subscription management page.
- **URL patterns** — all registered under `/buildings/<int:pk>/insights/` in `core/urls.py`.
- All five templates extend `base2.html`, use static/sample data, and share consistent sub-navigation tabs.

## Vault section — completed state
The Vault section is fully implemented:
- **`vault_trend_logs`** — resolves the active building from `pk`, opens the linked SQLite database with raw `sqlite3`, queries the Trend Log table, and passes rows to the template.
- **`vault_objects`** — same pattern, queries the Objects table.
- **`trend_logs.html`** — list-view template extending `base2.html`.
- **`objects.html`** — split-panel list/detail template extending `base2.html`.
- **URL patterns** — `/buildings/<int:pk>/vault/trend-logs/` and `/buildings/<int:pk>/vault/objects/` are registered in `core/urls.py`.

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
- `myportal/templates/core/building_dashboard.html` — fill in the five empty `building-card-body` sections.
- `myportal/core/views.py` — extend `building_dashboard` view context with sample data per card if needed.
- `Layout_Ref/07b_New_Dashboard.png` — primary mockup to follow.
- `static/css/app2.css` — reuse existing `.building-card` tokens; avoid structural changes.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
