# TASK

## Current task
Build the **Charts, Systems, and Settings/Profile section** — wire up the three placeholder building-tab icons in `base2.html`:
`Charts`, `Systems`, `Settings` (referencing Profile), currently pointing to `href="#"`.

## Immediate objective
Create layout-first pages for Charts, Systems, and Settings/Profile using static/sample data, matching `Layout_Ref/12a_Charts_*.png`, `13a_Systems_*.png`, and `14a_Settings__Profile_*.png`. All pages must fit seamlessly into the existing BLENDY building-tab shell (`base2.html`) and visual language. Backend wiring (queryset-backed data, live chart data, real settings persistence) is a **subsequent step** and is out of scope here.

Specific targets:

- **Charts page** — building-scoped charts/visualization page, per `Layout_Ref/12a_Charts_01.png` and `12a_Charts_02.png`. Likely chart widgets/graphs over building data (trend logs, energy, or systems), distinct from the raw Vault trend-log table.
- **Systems page** — building-scoped systems overview/management page, per `Layout_Ref/13a_Systems_01.png` and `13a_Systems_02.png`. Lists/manages the building's mechanical/electrical systems at a higher level than Vault objects.
- **Settings / Profile page** — settings section tied to the profile/settings icon, per `Layout_Ref/14a_Settings__Profile_01.png` and `14a_Settings__Profile_02.png`. Clarify with the user whether this is building-scoped settings or an extension of the existing account-level `accounts/profile.html` before finalizing routing.

## Background from the previous step
Energy & Report section is now complete:
- `building_energy` and `building_reports` view functions are implemented in `core/views.py`.
- URL patterns `/buildings/<int:pk>/energy/` and `/buildings/<int:pk>/reports/` are registered in `core/urls.py`.
- `energy.html` and `report.html` are built as templates extending `base2.html`, wired into the building-tab sub-nav with `building_tab` active-state highlighting, consistent with the Vault and Insight patterns.

## Scope for the next coding round

**In scope:**
- `myportal/core/views.py` — add view(s) for Charts, Systems, and Settings/Profile (login_required, resolve building from `pk`, render template with minimal static context).
- `myportal/core/urls.py` — add URL patterns under `/buildings/<pk>/charts/`, `/buildings/<pk>/systems/`, `/buildings/<pk>/settings/`.
- `myportal/templates/base2.html` — replace the placeholder `href="#"` links (Charts, Systems, Settings tabs, around lines 128–139) with real `{% url %}` routes and `active` state highlighting consistent with the Energy/Reports tabs.
- `myportal/templates/core/charts.html` — new layout template (name tentative).
- `myportal/templates/core/systems.html` — new layout template (name tentative).
- `myportal/templates/core/settings.html` — new layout template (name tentative).

**Out of scope for this round:**
- Any changes to `admin.py` files or `admin_custom.css`.
- Changes to `static/css/app.css` or `static/js/app.js`.
- New Django models or migrations.
- Real queryset-backed data, live chart data, or settings persistence logic.
- Refactoring of existing views, URLs, or forms.
- Buildings, Dashboard, Groups, Users, Clients, Profile (account-level), Vault, Insight, Energy, or Reports pages.

## Starting point
- Review `base2.html` (lines ~118–140) for the current placeholder `href="#"` tabs and the pattern used by the Energy/Reports tabs for how to wire a new one in.
- Review `Layout_Ref/12a_Charts_01.png`, `12a_Charts_02.png` for the Charts page layout and content.
- Review `Layout_Ref/13a_Systems_01.png`, `13a_Systems_02.png` for the Systems page layout and content.
- Review `Layout_Ref/14a_Settings__Profile_01.png`, `14a_Settings__Profile_02.png` for the Settings/Profile page layout and content.
- Review `energy.html` / `report.html` for the general building-tab page structure to follow.
- Review `objects.html` for a split-panel or table-heavy layout pattern if Systems or Charts need one.
- Review `dashboard.html` for the KPI card + chart widget layout pattern if Charts needs summary cards.
- Confirm URL suffixes `/charts/`, `/systems/`, `/settings/` under `/buildings/<pk>/` do not conflict with existing URL patterns in `core/urls.py`.

## Expected deliverables
1. Updated `core/views.py` with view(s) for Charts, Systems, and Settings/Profile.
2. Updated `core/urls.py` with new URL patterns under `/buildings/<pk>/charts/`, `/buildings/<pk>/systems/`, `/buildings/<pk>/settings/`.
3. Updated `templates/base2.html` with real routes and active-state highlighting for the Charts, Systems, and Settings tabs.
4. New `myportal/templates/core/charts.html`.
5. New `myportal/templates/core/systems.html`.
6. New `myportal/templates/core/settings.html`.

## Acceptance criteria
- All three pages render inside the shared BLENDY building-tab shell (`base2.html`) correctly, with the building-tab sub-nav still functional.
- Static/sample data is used for all list rows, KPI values, and chart placeholders — no real database queries required at this stage.
- Each page follows the correct visual pattern consistent with the referenced `Layout_Ref` mockups and existing pages.
- The Charts, Systems, and Settings tabs in `base2.html` link to real pages (no more `href="#"`) and correctly show an `active` state when on that page.
- URL patterns follow the convention `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, `/buildings/<int:pk>/settings/`.
- No regressions in any existing pages, including the Vault, Insight, Energy, and Reports tabs.
- `app.css` and all admin files are untouched.
