# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections, and a common visual system in `static/css/app.css` / `app2.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse. Inside a building, `base2.html` provides the building-tab sub-nav with all 8 icons fully wired: **Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings**.
The Profile (account-level), Client, Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, Charts, and Systems sections are all functionally/layout complete. The **next active focus is making the building-tab Settings/Profile page functional** — `core/settings_profile.html` currently only displays a read-only table of building fields with a non-functional Edit button; it needs a real edit-and-save flow wired to the `Building` model. Buildings pages and the `building_dashboard.html` card content remain deferred to later stages.

## Existing structure relevant to the next step
- `myportal/templates/core/settings_profile.html` — currently a read-only `.profile-table` of Building fields with a toolbar Edit button (`.edit-btn`) that has no behaviour; needs an editable form/state.
- `myportal/core/views.py` — `building_settings_profile` view currently only handles `GET`/render; needs `POST` handling, validation, and save logic.
- `myportal/core/forms.py` — no form exists yet for the Building profile fields; a new form class is needed.
- `myportal/core/models.py` — the `Building` model already defines every field shown on the page (name, code, address, city, state, postal, country, timezone, building_phone, building_fax, tech_contact_name/phone/email, building_type, gross_floor_area, occupancy, energy_star_id, dashboard_chart, photo) — no migration expected.
- `myportal/accounts/views.py`, `myportal/accounts/forms.py`, `myportal/templates/accounts/profile.html` — the existing working edit/save/avatar-upload pattern to reuse as reference.
- `myportal/core/urls.py` — no new routes needed; `/buildings/<int:pk>/settings/profile/` (`building_settings_profile`) already exists.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile (account-level) | `profile.html` | ✅ Functional |
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
| **Settings / Profile (building-tab)** | `settings_profile.html` | 🔲 **Next (in progress)** — read-only display only, Edit button has no function yet |
| Building Dashboard | `core/building_dashboard.html` | 🔲 Deferred — layout skeleton only, no card content yet |

## Settings/Profile — planned work
The next stage adds real edit/save functionality to `core/settings_profile.html`, the page behind the "Settings" icon in the `base2.html` building-tab nav. The template currently renders every `Building` field as a static two-column table row, with a toolbar Edit button that does nothing. The plan:

- Add a `BuildingSettingsProfileForm` (or similar) in `core/forms.py` covering all editable fields, including the `photo` ImageField.
- Extend `building_settings_profile` in `core/views.py` to accept `POST`, validate via the new form, and save changes to the `Building` instance, keeping the existing `_user_can_access_object_client` permission check intact.
- Update `settings_profile.html` so the existing `.edit-btn` toggles an editable state (inline fields or a distinct edit form) and submits back to the same view.
- Follow the account-level `profile.html` / `accounts/forms.py` / `accounts/views.py` pattern as the closest existing reference for edit/save UX and file-upload handling.
- Reuse existing `.settings-profile-page` / `.profile-card` / `.profile-table` styles; avoid new CSS files unless unavoidable.

## Charts, Systems & Settings/Profile section — status
- **`building_charts`** — resolves the active building from `pk`, enforces client-access permission, renders `core/chart.html` with `building_tab="charts"`. ✅ Complete (layout-first).
- **`building_systems`** — same pattern, renders `core/systems.html` with `building_tab="systems"`. ✅ Complete (layout-first).
- **`building_settings_profile`** — same pattern, renders `core/settings_profile.html` with `building_tab="settings"`. 🔲 Read-only only; edit/save function is the current next task.
- **URL patterns** — `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, and `/buildings/<int:pk>/settings/profile/` are registered in `core/urls.py`.
- All three templates extend `base2.html`, and the `base2.html` building-tab nav links all three with correct `active` state highlighting — no `href="#"` placeholders remain in the nav.

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

## Building Dashboard — deferred state
`core/building_dashboard.html` (behind the first "Dashboard" icon in `base2.html`) still renders only an empty layout skeleton with five blank card sections (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts), per `Layout_Ref/07b_New_Dashboard.png`. This remains a separate, still-pending stage after the Settings/Profile function is completed.

## Files most relevant for the next step
- `myportal/templates/core/settings_profile.html` — add editable form markup/state alongside the existing read-only table.
- `myportal/core/views.py` — extend `building_settings_profile` to handle `POST`, validation, and save.
- `myportal/core/forms.py` — add the new Building profile edit form.
- `myportal/accounts/views.py` / `myportal/accounts/forms.py` / `myportal/templates/accounts/profile.html` — reference pattern for the existing working edit/save flow.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
