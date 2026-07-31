# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) remain layout-only or sample-data driven and are **deferred** to a later stage.
The Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections are all **layout/route complete** — all eight building-tab icons in `base2.html` (Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings) point to real routes with `active` state highlighting; none are `href="#"` placeholders.
The **next active implementation stage is the function of `core/settings_profile.html`** (the building-tab "Settings" page). It currently renders a **read-only** profile table (building name, location ID, address, timezone, contact info, building type, size, occupancy, etc.) with a toolbar **Edit button that has no behaviour yet** — no edit mode, no form, no save/POST handling. The `building_dashboard.html` content work (five empty placeholder cards) documented previously remains a separate, still-pending stage and has **not** been started.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups, Clients, and Users pages are fully functional (client-scoped where relevant).
- Account-level Profile page (`accounts/profile.html`) save flow, avatar upload, and Django admin visibility are implemented — this is the reference pattern to follow for the settings_profile.html save flow.
- `dashboard.html` (app-level dashboard, not building-scoped) is fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- The sliding left panel in `base.html` is fully interactive.
- **Django admin is fully consistent with the frontend view**.
- **Vault section is complete**: `trend_logs.html` and `objects.html` are both live, reading data from the building-linked SQLite database via raw `sqlite3` connections.
- **Insight section is complete (layout-first)**: all five pages (`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`) extend `base2.html`, using static/sample data and sub-navigation tabs.
- **Energy & Report section is complete**: `energy.html` (`building_energy` view) and `report.html` (`building_reports` view), both extending `base2.html` and wired into the building-tab sub-nav.
- **Charts and Systems are complete (layout-first)**: `building_charts` renders `core/chart.html`, `building_systems` renders `core/systems.html`.
- **Settings/Profile page exists but is read-only**: `building_settings_profile` view (`/buildings/<pk>/settings/profile/`) resolves the building via `pk`, enforces `_user_can_access_object_client`, and renders `core/settings_profile.html` with `selected_building`/`selected_client`/`building_tab="settings"`. The template displays all Building model fields (name, code/location id, country, state, city, postal, address, timezone, phone, fax, technical contact name/phone/email, building type, gross floor area, occupancy, energy_star_id, dashboard_chart) as a static two-column table. The `Building` model (`core/models.py`) already has all of these fields defined, so no schema/migration work is expected for the next step.

## What is not yet done — current target
**Settings/Profile function — `core/settings_profile.html` + `building_settings_profile` view.** The page currently only displays building data; it needs real edit/save functionality:

- **Edit mode toggle** — the existing `.edit-btn` (pencil icon) in `.settings-toolbar` should switch the profile table into an editable form (inline or via a distinct edit state), following the same UX spirit as the account-level `profile.html` edit/save flow.
- **Editable fields** — name, address, city, state, postal, country, timezone, building_phone, building_fax, tech_contact_name, tech_contact_phone, tech_contact_email, building_type, gross_floor_area, occupancy, energy_star_id, dashboard_chart, and photo upload (reusing the `Building.photo` ImageField, same pattern as building/client logo uploads elsewhere in the app).
- **Form + POST handling** — add a `BuildingSettingsProfileForm` (or similar) in `core/forms.py` and extend `building_settings_profile` in `core/views.py` to handle `GET` (render read-only or form) and `POST` (validate + save), keeping the existing `_user_can_access_object_client` permission check intact.
- **Save confirmation / redirect** — after a successful save, redisplay the page (read-only or with a success message), consistent with how `profile.html`'s save flow behaves.

## Important implementation notes
- This page is **building-scoped** — resolve the active building context consistently with the existing `building_settings_profile` view (`selected_building`, `pk` in the URL).
- Template must keep extending `base2.html` (building-tab shell) and reuse existing `.settings-profile-page` / `.profile-card` / `.profile-table` / `.edit-btn` classes already defined inline in `settings_profile.html`; avoid new CSS files unless strictly necessary.
- Reuse the account-level `profile.html` + `accounts/forms.py` + `accounts/views.py` save pattern as the primary reference for form structure, validation, and file upload handling.
- Keep all existing display fields and their current fallback/default values working when a field is blank.
- `building_dashboard.html` (five placeholder cards: Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts) remains a **separate, still-pending** stage — do not work on it in this round.
- No changes needed to `base2.html` nav itself — the Settings tab already links correctly to `building_settings_profile`.

## Relevant files for the next session
- `myportal/templates/core/settings_profile.html` — add edit-mode markup/form fields alongside the existing read-only table.
- `myportal/core/views.py` — extend `building_settings_profile` to handle `POST` and form validation/save.
- `myportal/core/forms.py` — add a form class for the editable Building profile fields.
- `myportal/core/models.py` — reference only; the `Building` model already has all needed fields (no migration expected).
- `myportal/accounts/views.py` / `myportal/accounts/forms.py` / `myportal/templates/accounts/profile.html` — reference pattern for the existing working save/edit flow.
- `myportal/core/urls.py` — no new routes expected; existing `/buildings/<int:pk>/settings/profile/` route already exists.

## Next task
Work on **making `core/settings_profile.html` functional** — turn the read-only building profile table into an editable form wired to a real save flow, using the account-level Profile page as the pattern to follow.

This next step should include:
- Reviewing `accounts/profile.html`, `accounts/forms.py`, and `accounts/views.py` to confirm the existing edit/save UX pattern.
- Adding a form class in `core/forms.py` covering the editable Building fields (including photo upload).
- Extending `building_settings_profile` in `core/views.py` to accept `POST`, validate, and save changes, keeping the existing permission check intact.
- Updating `settings_profile.html` so the Edit button actually toggles into an editable state and submits to the view.
- Keeping the existing `.settings-profile-page` / `.profile-table` styling and layout intact.

## Constraints for the next edit
- Focus on the Settings/Profile page function only (`core/settings_profile.html`, `core/views.py`'s `building_settings_profile`, and `core/forms.py`).
- Do not start work on `building_dashboard.html` in this round — it remains a separate future stage.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Users, app-level Dashboard, Vault, Insight, Energy, Reports, Charts, Systems, Left panel, Admin).
- Do not modify `static/css/app.css`/`app2.css` structurally (adding small scoped styles for the edit form is acceptable if unavoidable) or any existing admin files.
- Preserve all existing model registrations and view signatures where not directly needed for the new POST handling.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: make the building-tab Settings/Profile page functional —
turn core/settings_profile.html from a read-only display into an editable
form wired to a real save flow.
Constraints:
- reuse the account-level profile.html / accounts/forms.py / accounts/views.py
  edit-save pattern as the reference
- add a form class in core/forms.py for the editable Building fields
  (name, address, city, state, postal, country, timezone, building_phone,
  building_fax, tech_contact_name/phone/email, building_type,
  gross_floor_area, occupancy, energy_star_id, dashboard_chart, photo)
- extend building_settings_profile in core/views.py to handle POST,
  validate, and save, keeping _user_can_access_object_client intact
- the existing .edit-btn should toggle into an edit state and submit to the view
- reuse existing .settings-profile-page / .profile-table CSS; avoid new CSS files
- no changes to base2.html nav (Settings tab already links correctly)
- no work on building_dashboard.html in this round
- no modifications to app.css, admin files, or any already-completed views
Reference:
- accounts/profile.html, accounts/forms.py, accounts/views.py for the working save pattern
- core/models.py Building model for the exact field list and types
- existing building_settings_profile view (core/views.py) and template
  (core/settings_profile.html) for current structure
Please return complete updated files only.
```
