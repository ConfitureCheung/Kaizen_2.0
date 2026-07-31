# TASK

## Current task
Build out the **function of the building-tab Settings/Profile page** — turn `core/settings_profile.html`, the template rendered by `building_settings_profile` view (`/buildings/<int:pk>/settings/profile/`) and shown behind the "Settings" icon in the `base2.html` 8-icon building-tab nav, from a read-only display into a real editable/save flow.

## Immediate objective
Make the existing `.edit-btn` (pencil icon in the page toolbar) actually do something: toggle the profile table into an editable state (form fields for each Building attribute), submit changes back to `building_settings_profile`, validate them, and persist them to the `Building` model instance. The page must continue to fit seamlessly into the existing BLENDY building-tab shell (`base2.html`) and reuse the existing `.settings-profile-page` / `.profile-card` / `.profile-table` / `.edit-btn` styling already defined inline in the template. The account-level `accounts/profile.html` + `accounts/forms.py` + `accounts/views.py` edit/save/avatar-upload flow is the primary reference pattern.

Specific fields to make editable (all already exist on the `Building` model in `core/models.py` — no migration expected):

- **Identity/location**: name, code (Location ID), country, state, city, postal, address, timezone.
- **Contact**: building_phone, building_fax, tech_contact_name, tech_contact_phone, tech_contact_email.
- **Building attributes**: building_type, gross_floor_area (Building Size), occupancy.
- **Other**: energy_star_id, dashboard_chart (label text), and the building `photo` (image upload, same pattern as building/client logo uploads elsewhere in the app).

## Background from the previous step
Charts and Systems sections are complete (layout-first), and the Settings/Profile page exists as a **read-only** display:
- `building_charts`, `building_systems`, and `building_settings_profile` view functions are implemented in `core/views.py`, each `@login_required`, resolving the building via `pk` and enforcing `_user_can_access_object_client`.
- URL patterns `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, and `/buildings/<int:pk>/settings/profile/` are registered in `core/urls.py`.
- `chart.html`, `systems.html`, and `settings_profile.html` are built as templates extending `base2.html`, wired into the building-tab sub-nav with `building_tab` active-state highlighting.
- `settings_profile.html` currently renders a static `.profile-table` of all Building fields with default/fallback sample values shown when a field is blank, plus a toolbar Edit button with no behaviour yet.
- All 8 icons in the `base2.html` building-tab nav (Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings) point to real `{% url %}` routes — no `href="#"` placeholders remain.
- `building_dashboard.html` (five empty placeholder cards) is a **separate, still-pending** stage and is explicitly out of scope for this round.

## Scope for the next coding round

**In scope:**
- `myportal/templates/core/settings_profile.html` — add an editable form state triggered by the existing Edit button, covering all fields listed above.
- `myportal/core/forms.py` — add a new form class (e.g. `BuildingSettingsProfileForm`) for the editable Building fields, including the photo upload.
- `myportal/core/views.py` — extend `building_settings_profile` to handle `POST` (bind form, validate, save) in addition to the existing `GET` rendering, keeping `_user_can_access_object_client` and session handling intact.

**Out of scope for this round:**
- Any changes to `admin.py` files or `admin_custom.css`.
- Structural changes to `static/css/app.css` / `app2.css` or `static/js/app.js` (small additive/scoped styles only if unavoidable).
- New Django models or migrations — the `Building` model already has every needed field.
- `core/building_dashboard.html` and its view — remains a separate future stage.
- Changes to `core/urls.py` — the `building_settings_profile` route already exists and needs no new patterns.
- Buildings, app-level Dashboard, Groups, Users, Clients, account-level Profile, Vault, Insight, Energy, Reports, Charts, or Systems pages.

## Starting point
- Review `myportal/templates/core/settings_profile.html` for the current read-only `.profile-table` markup and the toolbar `.edit-btn`.
- Review `myportal/accounts/templates/accounts/profile.html`, `myportal/accounts/forms.py`, and `myportal/accounts/views.py` for the existing working edit/save/avatar-upload pattern.
- Review `myportal/core/models.py`'s `Building` model for the exact field list, types, and choices (e.g. `COUNTRY_CHOICES`, `TIMEZONE_CHOICES`, `BUILDING_TYPE_CHOICES`, `AREA_UNIT_CHOICES`).
- Review `myportal/core/views.py`'s `building_settings_profile` view (currently `GET`-only, resolves `pk`, checks `_user_can_access_object_client`, passes `selected_building`/`selected_client`/`building_tab="settings"`) for the current context shape.
- Review `myportal/core/forms.py` for existing form conventions/style used elsewhere in the app (e.g. any building or client forms already present).

## Expected deliverables
1. Updated `myportal/templates/core/settings_profile.html` with a working edit-mode form wired to the Edit button, covering all listed fields plus photo upload.
2. New/updated form class in `myportal/core/forms.py` for the editable Building profile fields.
3. Updated `myportal/core/views.py` (`building_settings_profile` view) handling `GET` and `POST`, with validation and save logic.

## Acceptance criteria
- The Settings/Profile page renders inside the shared BLENDY building-tab shell (`base2.html`) correctly, with the building-tab sub-nav still functional and the "Settings" tab showing an active state.
- Clicking the Edit button switches the page into an editable state with form fields pre-populated from the current `Building` instance.
- Submitting the form validates input and persists changes to the `Building` model, then reflects the updated values on the page.
- Photo upload works using the existing `Building.photo` ImageField, consistent with upload handling elsewhere in the app.
- The existing `_user_can_access_object_client` permission check remains intact and enforced on both `GET` and `POST`.
- No regressions in any existing pages, including Vault, Insight, Energy, Reports, Charts, and Systems tabs.
- `app.css` and all admin files are untouched (aside from any minor, additive, clearly-scoped CSS if genuinely unavoidable).
- `building_dashboard.html` is left unchanged in this round.
