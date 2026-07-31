# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and the now-complete **Charts, Systems, and Settings/Profile** sections.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) remain layout-only or sample-data driven and are **deferred** to a later stage.
The Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, and **Charts, Systems, and Settings/Profile sections are all complete** — all eight building-tab icons in `base2.html` (Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings) now point to real routes with `active` state highlighting; none are `href="#"` placeholders anymore.
The **next active implementation stage is the building-tab Dashboard function** — `core/building_dashboard.html` (the page behind the first icon, "Dashboard", in the `base2.html` nav) currently renders as an empty layout skeleton with five blank card sections (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts) and needs real content, following the `Layout_Ref/07b_New_Dashboard.png` mockup.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional and client-scoped.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional.
- Users pages are fully functional.
- `dashboard.html` (app-level dashboard, not building-scoped) is fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- The sliding left panel in `base.html` is fully interactive.
- **Django admin is fully consistent with the frontend view**.
- **Vault section is complete**: `trend_logs.html` and `objects.html` are both live, reading data from the building-linked SQLite database via raw `sqlite3` connections.
- **Insight section is complete**: all five pages (`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`) are built as layout-first templates extending `base2.html`, using static/sample data and sub-navigation tabs. Five views and URL patterns under `/buildings/<pk>/insights/` are registered in `core/views.py` and `core/urls.py`.
- **Energy & Report section is complete**: implemented as `energy.html` (`building_energy` view, `/buildings/<pk>/energy/`) and `report.html` (`building_reports` view, `/buildings/<pk>/reports/`), both extending `base2.html` and wired into the building-tab sub-nav.
- **Charts, Systems, and Settings/Profile section is complete**: `building_charts` renders `core/chart.html` at `/buildings/<pk>/charts/`, `building_systems` renders `core/systems.html` at `/buildings/<pk>/systems/`, and `building_settings_profile` renders `core/settings_profile.html` at `/buildings/<pk>/settings/profile/`. All three views are `@login_required`, resolve the building via `pk`, enforce `_user_can_access_object_client`, and pass `selected_building`/`selected_client`/`building_tab`. All three templates extend `base2.html` and are wired into the building-tab nav with correct `active` state highlighting — the placeholder `href="#"` links have been fully replaced.

## What is not yet done — current target
**Building Dashboard function — `core/building_dashboard.html`.** This is the page rendered by the `building_dashboard` view (`/buildings/<int:building_id>/dashboard/`) and is what appears behind the first ("Dashboard") icon in the `base2.html` 8-icon nav. It currently extends `base2.html` correctly but only outputs an empty layout skeleton (`building-dashboard-placeholder` / `building-dashboard-grid`) with five card sections that have no content in `building-card-body`:

- **BUILDING PROFILE** — needs building photo, name, data-collection device status, fault-detection insight count/bar, a small weather widget, building address, and an embedded location map, per `Layout_Ref/07b_New_Dashboard.png`.
- **DASHBOARD** (main chart area) — needs the building's cooling-load / equipment-operation chart (e.g. "Average Cooling Load Report" stacked bar + line chart) matching the mockup.
- **INSIGHTS** — needs a total-insights counter and a short list of systems with the most insights.
- **ENERGY BREAKDOWN** (current week) — needs a labelled breakdown (e.g. by system, such as "Chiller Plant") with a kWh figure.
- **GREEN FACTS** — needs a small rotating tip/fact panel with an icon and short text.

## Important implementation notes
- This page is **building-scoped** — resolve the active building context consistently with the existing `building_dashboard` view (`selected_building`, `building_id`/`pk` in the URL).
- Template must keep extending `base2.html` (building-tab shell) and reuse the existing `.building-card` / `.building-card-tall` / `.building-card-wide` CSS classes already defined in `static/css/app2.css`; avoid new CSS files unless strictly necessary.
- Follow `Layout_Ref/07b_New_Dashboard.png` as the primary visual reference for this page.
- Start with layout-first (static/sample data) content inside each card; live queryset/chart wiring (e.g. pulling from the building's linked SQLite DB the way Vault does) can be a subsequent step, consistent with how other sections were staged.
- No changes needed to `base2.html` nav itself — the Dashboard tab already links correctly to `building_dashboard`.

## Relevant files for the next session
- `myportal/templates/core/building_dashboard.html` — replace the empty `building-card-body` divs with real content for each of the five cards.
- `myportal/core/views.py` — extend the `building_dashboard` view context if new sample/queryset data is needed per card.
- `myportal/core/urls.py` — no new routes expected; existing `/buildings/<int:building_id>/dashboard/` route already exists.
- `Layout_Ref/07b_New_Dashboard.png` — primary mockup for this page (building profile, chart, insights, energy breakdown, green facts).
- `static/css/app2.css` — read-only reference for `.building-card` tokens; do not modify unless a new card layout is genuinely required.

## Next task
Work on **building the Dashboard tab's content** inside `core/building_dashboard.html` — fill in the five placeholder cards (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts) with static/sample data matching `Layout_Ref/07b_New_Dashboard.png`.

This next step should include:
- Reviewing `Layout_Ref/07b_New_Dashboard.png` to confirm page layout and content for each card.
- Filling in `building-card-body` sections in `building_dashboard.html` using static/sample data for layout validation.
- Extending the `building_dashboard` view in `core/views.py` with any additional sample context needed per card.
- Keeping the existing `.building-card` CSS classes and grid structure intact.

## Constraints for the next edit
- Focus on the building-tab Dashboard page content only (`core/building_dashboard.html` and its view).
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users, app-level Dashboard, Vault, Insight, Energy, Reports, Charts, Systems, Settings, Left panel, Admin).
- Do not modify `static/css/app.css`/`app2.css` structurally (adding small scoped styles for new content is acceptable if unavoidable) or any existing admin files.
- Preserve all existing model registrations and view signatures.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build out the content of the building-tab Dashboard page —
fill in the five placeholder cards in core/building_dashboard.html
(Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts).
Constraints:
- layout-first using static/sample data; live queryset/chart wiring is a later step
- extend base2.html; reuse existing .building-card CSS classes from app2.css
- reference Layout_Ref/07b_New_Dashboard.png for exact content and layout per card
- extend the building_dashboard view in core/views.py with sample context if needed
- no changes to base2.html nav (Dashboard tab already links correctly)
- no modifications to app.css, admin files, or any already-completed views
Reference:
- Layout_Ref/07b_New_Dashboard.png for exact content per card
- existing building_dashboard view (core/views.py) and template (core/building_dashboard.html) for current structure
Please return complete updated files only.
```
