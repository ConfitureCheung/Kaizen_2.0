# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, Vault, Insight, and the now-complete **Energy & Report** sections.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) remain layout-only or sample-data driven and are **deferred** to a later stage.
The Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, and **Energy & Report sections are all complete**.
The **next active implementation stage is the Charts, Systems, and Settings/Profile section** — three currently-placeholder building-tab icons in `base2.html` (`Charts`, `Systems`, `Settings`) need real templates, views, and URL wiring, following the `Layout_Ref/12a_Charts_*.png`, `13a_Systems_*.png`, and `14a_Settings__Profile_*.png` mockups.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional and client-scoped.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional.
- Users pages are fully functional.
- `dashboard.html` is fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- The sliding left panel in `base.html` is fully interactive.
- **Django admin is fully consistent with the frontend view**.
- **Vault section is complete**: `trend_logs.html` and `objects.html` are both live, reading data from the building-linked SQLite database via raw `sqlite3` connections.
- **Insight section is complete**: all five pages (`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`) are built as layout-first templates extending `base2.html`, using static/sample data and sub-navigation tabs. Five views and URL patterns under `/buildings/<pk>/insights/` are registered in `core/views.py` and `core/urls.py`.
- **Energy & Report section is complete**: implemented as `energy.html` (`building_energy` view, `/buildings/<pk>/energy/`) and `report.html` (`building_reports` view, `/buildings/<pk>/reports/`), both extending `base2.html` and wired into the building-tab sub-nav.

## What is not yet done — current target
**Charts, Systems, and Settings/Profile section — three new building-tab areas.** In `templates/base2.html`, the `Charts`, `Systems`, and `Settings` building-tab links currently point to `href="#"` (placeholder, not wired to any view):

- **Charts** — new charts/visualization page for a building, matching `Layout_Ref/12a_Charts_01.png` and `12a_Charts_02.png`. Likely a dedicated charting view over building trend-log/energy data, distinct from the existing Vault trend-log table.
- **Systems** — new systems overview page for a building, matching `Layout_Ref/13a_Systems_01.png` and `13a_Systems_02.png`. Lists/manages the building's mechanical/electrical systems (e.g. HVAC, lighting) at a higher level than Vault objects.
- **Settings / Profile icons** — settings section tied to the building/profile icon area, matching `Layout_Ref/14a_Settings__Profile_01.png` and `14a_Settings__Profile_02.png`. Distinct from the existing account-level `accounts/profile.html` — likely a building-scoped settings page reachable from the same icon nav.

## Important implementation notes
- All pages are **building-scoped** — resolve the active building context consistently with existing views (`selected_building`, `pk` in the URL).
- Templates must extend `base2.html` (building-tab shell) and use the existing BLENDY CSS tokens; no new CSS files unless strictly necessary.
- Follow existing visual patterns: `energy.html`/`report.html` for building-tab page structure; `objects.html` for split-panel or table-heavy layouts; `dashboard.html` for KPI card + chart widget layout if Charts needs summary cards.
- Un-comment/replace the placeholder `href="#"` links in `base2.html` for `Charts`, `Systems`, and `Settings` with real `{% url %}` tags once views exist, and add an `active` state check (`building_tab == 'charts' | 'systems' | 'settings'`) consistent with the Energy/Reports tabs.
- URL patterns should follow the existing convention, e.g. `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, `/buildings/<int:pk>/settings/`.
- Start with layout-first (static/sample data) pages; backend wiring is a subsequent step, consistent with how Insight and Energy & Report were staged.

## Relevant files for the next session
- `myportal/core/views.py` — add view(s) for Charts, Systems, and Settings/Profile.
- `myportal/core/urls.py` — add URL patterns under `/buildings/<pk>/charts/`, `/buildings/<pk>/systems/`, `/buildings/<pk>/settings/`.
- `myportal/templates/base2.html` — replace placeholder `href="#"` links (lines ~128-139) with real routes for Charts, Systems, Settings tabs.
- `myportal/templates/core/charts.html` — new template (name tentative).
- `myportal/templates/core/systems.html` — new template (name tentative).
- `myportal/templates/core/settings.html` or `settings_profile.html` — new template (name tentative).
- `Layout_Ref/12a_Charts_01.png`, `12a_Charts_02.png` — Charts mockups.
- `Layout_Ref/13a_Systems_01.png`, `13a_Systems_02.png` — Systems mockups.
- `Layout_Ref/14a_Settings__Profile_01.png`, `14a_Settings__Profile_02.png` — Settings/Profile mockups.
- `static/css/app.css` — read-only reference for CSS tokens; do not modify.

## Next task
Work on **Charts, Systems, and Settings/Profile section layout** — wire up the three placeholder building-tab icons in `base2.html`:
`Charts`, `Systems`, `Settings` (referencing Profile).

This next step should include:
- Reviewing `Layout_Ref/12a_Charts_*.png`, `13a_Systems_*.png`, `14a_Settings__Profile_*.png` to confirm page layout and content.
- Building new templates extending `base2.html`, using static/sample data for layout validation.
- Adding view(s) to `core/views.py` for each of the three sections.
- Registering URL patterns in `core/urls.py` under `/buildings/<pk>/charts/`, `/buildings/<pk>/systems/`, `/buildings/<pk>/settings/`.
- Replacing the placeholder `href="#"` links in `base2.html` with the new `{% url %}` routes, including `active` state highlighting.

## Constraints for the next edit
- Focus on Charts, Systems, and Settings/Profile section layout pages only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard, Vault, Insight, Energy, Reports, Left panel, Admin).
- Do not modify `static/css/app.css` or any existing admin files.
- Preserve all existing model registrations and view signatures.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the Charts, Systems, and Settings/Profile section layout —
wire up the three placeholder building-tab icons in base2.html (Charts, Systems, Settings)
with real templates, views, and URL patterns.
Constraints:
- layout-first using static/sample data; backend wiring is a later step
- extend base2.html; use existing BLENDY CSS tokens
- follow energy.html / report.html for overall building-tab page structure
- follow objects.html for split-panel or table-heavy layouts if needed
- follow dashboard.html for KPI card + chart widget layout if Charts needs summary cards
- reference Layout_Ref/12a_Charts_*.png, 13a_Systems_*.png, 14a_Settings__Profile_*.png for page content and layout
- add view(s) to core/views.py for charts, systems, and settings/profile
- add URL patterns under /buildings/<pk>/charts/, /buildings/<pk>/systems/, /buildings/<pk>/settings/
- replace the placeholder href="#" links in base2.html with real {% url %} routes and active-state highlighting
- no modifications to app.css, admin files, or any already-completed views
Reference:
- energy.html and report.html for building-tab page structure
- objects.html for split-panel pattern
- dashboard.html for KPI card + chart widget layout
- Layout_Ref mockups for exact content per section
Please return complete updated files only.
```
