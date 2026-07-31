# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, Insight, and Energy & Report sections, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse. Inside a building, `base2.html` provides a building-tab sub-nav (Vault, Insights, Energy, Reports, Charts, Systems, Settings).
The Profile, Client, Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, and **Energy & Report sections are all functionally complete**. The **next active focus is the Charts, Systems, and Settings/Profile section** — three building-tab icons in `base2.html` that currently link to `href="#"` and need real templates, views, and URLs, per `Layout_Ref/12a_Charts_*.png`, `13a_Systems_*.png`, and `14a_Settings__Profile_*.png`. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `myportal/core/views.py` — add view(s) for Charts, Systems, and Settings/Profile.
- `myportal/core/urls.py` — add URL patterns under `/buildings/<pk>/charts/`, `/buildings/<pk>/systems/`, `/buildings/<pk>/settings/`.
- `myportal/templates/base2.html` — replace the placeholder `href="#"` building-tab links for Charts, Systems, and Settings with real routes.
- `myportal/templates/core/` — all new Charts/Systems/Settings templates live here, extending `base2.html`.
- `Layout_Ref/12a_Charts_*.png`, `13a_Systems_*.png`, `14a_Settings__Profile_*.png` — visual mockups for the next section.
- `static/css/app.css` already defines the app's visual language; no new CSS files are needed.

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
| Vault | `trend_logs.html`, `objects.html` | ✅ Complete |
| Insight | `insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html` | ✅ Complete (layout-first) |
| Energy | `energy.html` | ✅ Complete |
| Reports | `report.html` | ✅ Complete |
| Charts | *(new — placeholder tab only)* | 🔲 Next (in progress) |
| Systems | *(new — placeholder tab only)* | 🔲 Next (in progress) |
| Settings / Profile icons | *(new — placeholder tab only)* | 🔲 Next (in progress) |

## Charts, Systems & Settings/Profile — planned work
The next stage wires up the three remaining building-tab icons in `base2.html` (`Charts`, `Systems`, `Settings`), which currently render as inactive links (`href="#"`). The first stage is layout-only using static/sample data; backend wiring follows in a subsequent step, consistent with how Vault, Insight, and Energy & Report were staged.

Planned pages:

- **Charts** — building-scoped charts/visualization page, per `Layout_Ref/12a_Charts_01.png` and `12a_Charts_02.png`.
- **Systems** — building-scoped systems overview/management page, per `Layout_Ref/13a_Systems_01.png` and `13a_Systems_02.png`.
- **Settings / Profile icons** — building-scoped (or icon-nav-linked) settings page, per `Layout_Ref/14a_Settings__Profile_01.png` and `14a_Settings__Profile_02.png`.

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
- `myportal/core/views.py` — add view(s) for Charts, Systems, and Settings/Profile.
- `myportal/core/urls.py` — add URL patterns under `/buildings/<pk>/charts/`, `/buildings/<pk>/systems/`, `/buildings/<pk>/settings/`.
- `myportal/templates/base2.html` — replace placeholder `href="#"` tab links with real routes.
- `myportal/templates/core/charts.html` — new Charts page (name tentative).
- `myportal/templates/core/systems.html` — new Systems page (name tentative).
- `myportal/templates/core/settings.html` — new Settings/Profile page (name tentative).
- `Layout_Ref/12a_Charts_*.png`, `13a_Systems_*.png`, `14a_Settings__Profile_*.png` — mockups to follow.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
