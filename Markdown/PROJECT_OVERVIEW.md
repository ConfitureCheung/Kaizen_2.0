# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections, and a common visual system in `static/css/app.css` / `app2.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse. Inside a building, `base2.html` provides the building-tab sub-nav with all 8 icons fully wired: **Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings**. Vault and Insights are each exposed as **dropdown sub-navs** (multiple linked pages behind one icon); Settings is currently still a **single plain link** to `core/settings_profile.html`.
The Profile (account-level), Client, Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, Charts, and Systems sections are all functionally/layout complete. The **next active focus is an independent drag-and-drop prototype**: converting Settings into a dropdown sub-nav (like Vault/Insights) with two options — **"Profile"** (the existing `core/settings_profile.html`, relocated as-is) and **"Fake"** (a new `core/fake_build_report.html` page used to prototype building a report layout via drag-and-drop). This prototype is deliberately kept separate from the previously planned Settings/Profile edit-save function, which is now **deferred** — the project expects many more inner pages to be added behind each building-tab icon over time, so this drag-and-drop pattern is being proven out in isolation first. Buildings pages and the `building_dashboard.html` card content remain deferred to later stages as well.

## Existing structure relevant to the next step
- `myportal/templates/base2.html` — has the dropdown sub-nav pattern already implemented for Vault (`vaultDropdownWrap`/`vaultDropdownToggle`/`vaultDropdownMenu`) and Insights (`insightsDropdownWrap`/`insightsDropdownToggle`/`insightsDropdownMenu`), plus a shared `initDropdown(wrapId, toggleId, menuId)` JS helper. Settings (`building_settings_profile` link) still needs to be converted to this same pattern.
- `myportal/templates/core/settings_profile.html` — currently a read-only `.profile-table` of Building fields with a toolbar Edit button (`.edit-btn`) that has no behaviour; will be relocated under the new Settings dropdown as "Profile", unchanged for now. Its edit/save function remains a separate, deferred task.
- `myportal/templates/core/fake_build_report.html` — **does not exist yet**; new template to be created as the drag-and-drop report-builder prototype (sample/fake content only).
- `myportal/core/views.py` — `building_settings_profile` view currently only handles `GET`/render. A new `building_settings_fake` view needs to be added, following the same permission-check pattern (`_user_can_access_object_client`) as `building_settings_profile` / `building_charts` / `building_systems`.
- `myportal/core/urls.py` — the `# ── Settings ──` block currently has one route (`buildings/<int:pk>/settings/profile/`); a new route (e.g. `buildings/<int:pk>/settings/fake/`) needs to be added for the Fake page.
- `myportal/static/js/app.js` — likely home for the drag-and-drop wiring, pending the library/tooling decision (CDN `<script>` vs. an `npm`-managed build step).
- `myportal/core/models.py` — the `Building` model already defines every field shown on the (unchanged, for now) Profile page — no migration expected from this round of work.

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
| Vault | `trend_logs.html`, `objects.html` | ✅ Complete (dropdown sub-nav) |
| Insight | `insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html` | ✅ Complete (dropdown sub-nav, layout-first) |
| Energy | `energy.html` | ✅ Complete |
| Reports | `report.html` | ✅ Complete |
| Charts | `chart.html` | ✅ Complete (layout-first) |
| Systems | `systems.html` | ✅ Complete (layout-first) |
| **Settings → Profile** | `settings_profile.html` | 🔲 Read-only display, Edit button has no function — **deferred** (relocating into the new Settings dropdown, behaviour unchanged for now) |
| **Settings → Fake** | `fake_build_report.html` | 🔲 **Next (in progress)** — new standalone drag-and-drop report-builder prototype |
| Building Dashboard | `core/building_dashboard.html` | 🔲 Deferred — layout skeleton only, no card content yet |

## Settings section — planned work
Settings is being restructured from a single link into a **dropdown sub-nav**, matching the existing Vault and Insights pattern in `base2.html`. The plan:

- Convert the Settings entry in `base2.html` into a `dropdown-tab` (copy the `vaultDropdownWrap`/`insightsDropdownWrap` markup and register it with `initDropdown(...)`), exposing two links:
  - **Profile** → existing `building_settings_profile` view / `core/settings_profile.html`, relocated but functionally unchanged (still read-only; the edit/save function is a separate, deferred task — see below).
  - **Fake** → new `building_settings_fake` view / new `core/fake_build_report.html` template.
- Build `core/fake_build_report.html` as a **standalone drag-and-drop prototype** for assembling a report out of draggable blocks/elements. It uses sample/fake data and is explicitly not wired into real building/report data yet — its purpose is to prove out a drag-and-drop UX pattern that can later be reused across other inner pages behind the remaining building-tab icons.
- Decide on the drag-and-drop implementation: a client-side JS library is required (e.g. SortableJS, interact.js, GridStack.js); whether it's loaded via a CDN `<script>` tag or via `npm`/a `package.json` with a bundler is **not yet decided** and should be settled alongside this work.
- This task is intentionally **decoupled** from the Settings/Profile edit-save plan below, to keep the drag-and-drop experiment isolated while the project's inner-page structure (one icon → many pages) keeps growing in complexity.

### Settings → Profile edit/save function (deferred)
The previously planned edit/save function for `core/settings_profile.html` is **not part of the current round** but remains a known future task:
- Add a `BuildingSettingsProfileForm` (or similar) in `core/forms.py` covering all editable fields, including the `photo` ImageField.
- Extend `building_settings_profile` in `core/views.py` to accept `POST`, validate via the new form, and save changes to the `Building` instance, keeping the existing `_user_can_access_object_client` permission check intact.
- Update `settings_profile.html` so the existing `.edit-btn` toggles an editable state (inline fields or a distinct edit form) and submits back to the same view.
- Follow the account-level `profile.html` / `accounts/forms.py` / `accounts/views.py` pattern as the closest existing reference for edit/save UX and file-upload handling.
- Reuse existing `.settings-profile-page` / `.profile-card` / `.profile-table` styles; avoid new CSS files unless unavoidable.

## Charts, Systems & Settings section — status
- **`building_charts`** — resolves the active building from `pk`, enforces client-access permission, renders `core/chart.html` with `building_tab="charts"`. ✅ Complete (layout-first).
- **`building_systems`** — same pattern, renders `core/systems.html` with `building_tab="systems"`. ✅ Complete (layout-first).
- **`building_settings_profile`** — same pattern, renders `core/settings_profile.html` with `building_tab="settings"`. 🔲 Read-only only; edit/save function deferred. To be relocated under the new Settings dropdown as "Profile".
- **`building_settings_fake`** — **new, to be added**; same permission-check pattern, renders `core/fake_build_report.html`. 🔲 Next task (drag-and-drop report-builder prototype).
- **URL patterns** — `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, and `/buildings/<int:pk>/settings/profile/` are registered in `core/urls.py`; a new `/buildings/<int:pk>/settings/fake/` pattern is to be added.
- `chart.html` and `systems.html` extend `base2.html` with correct `active` state highlighting under their own single-link icons. Settings is being upgraded from a single link to a dropdown (like Vault/Insights) to host both "Profile" and "Fake".

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
- All five templates extend `base2.html`, use static/sample data, and share consistent sub-navigation tabs, exposed via the `insightsDropdownWrap` dropdown in `base2.html` — the reference pattern the new Settings dropdown will copy.

## Vault section — completed state
The Vault section is fully implemented:
- **`vault_trend_logs`** — resolves the active building from `pk`, opens the linked SQLite database with raw `sqlite3`, queries the Trend Log table, and passes rows to the template.
- **`vault_objects`** — same pattern, queries the Objects table.
- **`trend_logs.html`** — list-view template extending `base2.html`.
- **`objects.html`** — split-panel list/detail template extending `base2.html`.
- **URL patterns** — `/buildings/<int:pk>/vault/trend-logs/` and `/buildings/<int:pk>/vault/objects/` are registered in `core/urls.py`.
- Exposed via the `vaultDropdownWrap` dropdown in `base2.html` — the other reference pattern the new Settings dropdown will copy.

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
`core/building_dashboard.html` (behind the first "Dashboard" icon in `base2.html`) still renders only an empty layout skeleton with five blank card sections (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts), per `Layout_Ref/07b_New_Dashboard.png`. This remains a separate, still-pending stage, after both the Settings/Fake prototype and the (deferred) Settings/Profile edit-save function are completed.

## Files most relevant for the next step
- `myportal/templates/base2.html` — convert the Settings link into a dropdown-tab (Profile / Fake), copying the existing Vault/Insights dropdown markup and JS.
- `myportal/templates/core/fake_build_report.html` — new template for the drag-and-drop report-builder prototype.
- `myportal/core/views.py` — add the new `building_settings_fake` view.
- `myportal/core/urls.py` — add the new `buildings/<int:pk>/settings/fake/` route.
- `myportal/static/js/app.js` (or a new scoped JS/CDN include) — drag-and-drop wiring, once the library/tooling decision is made.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Keep the Settings/Fake drag-and-drop prototype decoupled from the deferred Settings/Profile edit-save work.
- Ask for complete updated files for touched files only when using AI help.
