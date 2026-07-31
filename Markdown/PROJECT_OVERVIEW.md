# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections, and a common visual system in `static/css/app.css` / `app2.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse. Inside a building, `base2.html` provides the building-tab sub-nav with all 8 icons fully wired: **Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings**. Vault, Insights, and **Settings** are each exposed as **dropdown sub-navs** (multiple linked pages behind one icon).
The Profile (account-level), Client, Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, Charts, and Systems sections are all functionally/layout complete. **Settings is now a dropdown** with two live options: **"Profile"** (`core/settings_profile.html`, read-only, edit/save deferred) and **"Fake"** (`core/fake_build_report.html`, a complete drag-and-drop formula/report-builder prototype using a single-line chain track in its mid panel).

The **next active focus is a second, parallel prototype**: `core/fake_build_report2.html`, which must match `fake_build_report.html`'s functional scope exactly (CSV upload, column plates, operator/grouping/function/aggregate chips, per-row answers, CSV/PDF export) but replaces the mid panel's **single-line chain track** with an **open canvas where dragged items become freestanding nodes that the user links together with connection lines** (a node-graph / flow-diagram style formula builder). This is being built the same way `fake_build_report.html` was: as an isolated experiment, kept separate from the deferred Settings/Profile edit-save function. Buildings pages and the `building_dashboard.html` card content remain deferred to later stages as well.

## Existing structure relevant to the next step
- `myportal/templates/base2.html` — has the dropdown sub-nav pattern implemented for Vault (`vaultDropdownWrap`/`vaultDropdownToggle`/`vaultDropdownMenu`), Insights (`insightsDropdownWrap`/`insightsDropdownToggle`/`insightsDropdownMenu`), and now Settings (`settingsDropdownWrap`/`settingsDropdownToggle`/`settingsDropdownMenu`, linking to "Profile" and "Fake"), plus a shared `initDropdown(wrapId, toggleId, menuId)` JS helper. A third Settings link ("Fake 2") needs to be added for the new prototype.
- `myportal/templates/core/settings_profile.html` — read-only `.profile-table` of Building fields with a toolbar Edit button (`.edit-btn`) that has no behaviour; reached via the Settings dropdown's "Profile" option. Its edit/save function remains a separate, deferred task.
- `myportal/templates/core/fake_build_report.html` — **complete**: a drag-and-drop formula/report-builder prototype (CSV upload, column plates, operator/bracket/function/aggregate chips, a single horizontal chain-track builder, saved formulas, per-row answers, CSV/PDF export). Vanilla JS only, no drag-and-drop library or npm tooling.
- `myportal/templates/core/fake_build_report2.html` — **does not exist yet**; new template for the node/graph-based variant of the same builder (sample/fake content only).
- `myportal/core/views.py` — `building_settings_profile` and `building_settings_fake` views exist, both following the same permission-check pattern (`_user_can_access_object_client`). A new `building_settings_fake2` view needs to be added, following the same pattern.
- `myportal/core/urls.py` — the `# ── Settings ──` block has `buildings/<int:pk>/settings/profile/` and `buildings/<int:pk>/settings/fake/`; a new route (e.g. `buildings/<int:pk>/settings/fake2/`) needs to be added.
- `myportal/static/js/app.js` — general app JS; the drag-and-drop logic for both fake report pages lives inline in each template's `extra_js` block rather than here, to keep each prototype self-contained.
- `myportal/core/models.py` — the `Building` model already defines every field shown on the (unchanged, for now) Profile page — no migration expected from Settings/Fake-related work.

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
| **Settings → Profile** | `settings_profile.html` | 🔲 Read-only display, Edit button has no function — **deferred** |
| **Settings → Fake** | `fake_build_report.html` | ✅ Complete — single-line chain-track formula/report-builder prototype |
| **Settings → Fake 2** | `fake_build_report2.html` | 🔲 **Next (in progress)** — node-graph / connection-line variant of the same builder |
| Building Dashboard | `core/building_dashboard.html` | 🔲 Deferred — layout skeleton only, no card content yet |

## Settings section — current state
Settings is now a **dropdown sub-nav** in `base2.html`, matching the Vault and Insights pattern, exposing:
- **Profile** → `building_settings_profile` view / `core/settings_profile.html` — read-only; edit/save function remains a separate, deferred task (see below).
- **Fake** → `building_settings_fake` view / `core/fake_build_report.html` — **complete**. A standalone drag-and-drop prototype: CSV upload on the left produces draggable column "plates"; the mid panel offers chip palettes for operators (`+ − × ÷ ^ %`), grouping (brackets), functions (`ABS`/`ROUND`/`SQRT`), and aggregates (`SUM`/`AVG`/`MIN`/`MAX`/`COUNT`), all dragged into a single horizontal **chain track** that enforces term/operator alternation and supports nested bracket groups; formulas are named, saved, and listed; the right panel shows per-row answers per saved formula with CSV export and print-to-PDF export. Implemented entirely in vanilla JS (HTML5 drag-and-drop events) — no CDN library or npm/build step was needed, resolving the earlier open tooling question.

### Settings → Fake 2 (next prototype, in progress)
A second prototype, `core/fake_build_report2.html`, is being built with the **same functional requirements** as Fake (CSV upload, column plates, operator/grouping/function/aggregate chips, saved formulas, per-row answers, CSV/PDF export), but with a different mid-panel interaction:
- Instead of a single-line chain track, the mid panel becomes an **open canvas/panel**. Dragging a column, operator, bracket, function, or aggregate onto it creates a **freestanding node** at the drop position (not constrained to one line).
- The user **draws connection lines between nodes** to link them together (e.g. connecting a column node → an operator node → a second column node to express `ColA + ColB`), building the formula as a small node-graph / flow-diagram rather than a flat strip.
- Implementation is expected to reuse `fake_build_report.html`'s CSV parsing, numeric-column detection, aggregate computation, and CSV/PDF export logic, adding only the new node-positioning and SVG-based connection-line rendering on top.
- Default approach is to stay library-free (vanilla JS + an SVG overlay for the lines), consistent with the choice made for `fake_build_report.html`, unless the connection-line math proves genuinely unworkable by hand.
- This is being treated as its own **independent trial task**, exposed via a new "Fake 2" link added to the existing `settingsDropdownMenu`, alongside "Profile" and "Fake" — not wired into real building/report data.

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
- **`building_settings_profile`** — same pattern, renders `core/settings_profile.html` with `building_tab="settings"`. 🔲 Read-only only; edit/save function deferred.
- **`building_settings_fake`** — same pattern, renders `core/fake_build_report.html`. ✅ Complete — single-line chain-track formula/report-builder prototype.
- **`building_settings_fake2`** — **new, to be added**; same permission-check pattern, renders `core/fake_build_report2.html`. 🔲 Next task (node-graph/connection-line report-builder prototype).
- **URL patterns** — `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, `/buildings/<int:pk>/settings/profile/`, and `/buildings/<int:pk>/settings/fake/` are registered in `core/urls.py`; a new `/buildings/<int:pk>/settings/fake2/` pattern is to be added.
- `chart.html` and `systems.html` extend `base2.html` with correct `active` state highlighting under their own single-link icons. Settings is a dropdown (like Vault/Insights) hosting "Profile" and "Fake", soon to add "Fake 2".

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
- All five templates extend `base2.html`, use static/sample data, and share consistent sub-navigation tabs, exposed via the `insightsDropdownWrap` dropdown in `base2.html`.

## Vault section — completed state
The Vault section is fully implemented:
- **`vault_trend_logs`** — resolves the active building from `pk`, opens the linked SQLite database with raw `sqlite3`, queries the Trend Log table, and passes rows to the template.
- **`vault_objects`** — same pattern, queries the Objects table.
- **`trend_logs.html`** — list-view template extending `base2.html`.
- **`objects.html`** — split-panel list/detail template extending `base2.html`.
- **URL patterns** — `/buildings/<int:pk>/vault/trend-logs/` and `/buildings/<int:pk>/vault/objects/` are registered in `core/urls.py`.
- Exposed via the `vaultDropdownWrap` dropdown in `base2.html`.

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
`core/building_dashboard.html` (behind the first "Dashboard" icon in `base2.html`) still renders only an empty layout skeleton with five blank card sections (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts), per `Layout_Ref/07b_New_Dashboard.png`. This remains a separate, still-pending stage, after the Settings/Fake 2 prototype and the (deferred) Settings/Profile edit-save function are completed.

## Files most relevant for the next step
- `myportal/templates/base2.html` — add a "Fake 2" link to the existing `settingsDropdownMenu`, alongside "Profile" and "Fake".
- `myportal/templates/core/fake_build_report2.html` — new template for the node/graph-based report-builder prototype.
- `myportal/core/views.py` — add the new `building_settings_fake2` view.
- `myportal/core/urls.py` — add the new `buildings/<int:pk>/settings/fake2/` route.
- `myportal/templates/core/fake_build_report.html` — reference implementation to reuse CSV/aggregate/export logic from.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Keep each Settings/Fake prototype (and the deferred Settings/Profile edit-save work) decoupled from one another.
- Ask for complete updated files for touched files only when using AI help.
