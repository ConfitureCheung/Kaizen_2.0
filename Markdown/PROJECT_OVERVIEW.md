# PROJECT OVERVIEW

## Current status (re-audited against actual code, Aug 2026)
The BLENDY Django project (`myportal`) includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, Charts/Systems/Settings sections, and a common visual system in `static/css/app.css` / `app2.css`.

**This revision corrects several stale claims in the previous version of this file** — a direct read of `core/views.py`, `core/urls.py`, `templates/base2.html`, and the templates themselves shows the project is further along than previously documented, but with real inconsistencies between backend (models/views) and frontend (templates) that are now the active focus. See "Known backend ↔ frontend inconsistencies" below.

The shared navigation includes a fully interactive sliding left panel in `base.html`, rendering a Client → Building tree. Inside a building, `base2.html` provides the building-tab sub-nav with all 8 icons wired: **Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings**. Vault, Insights, and Settings are each exposed as **dropdown sub-navs**.

## Corrected status vs. previous docs
- **`core/fake_build_report2.html` is COMPLETE, not "in progress."** The template (1,605 lines) implements a working node-graph/connection-line formula builder: draggable column plates, operator/bracket/function/aggregate palettes, a `<div id="frb2Canvas">` with an `<svg id="frb2Svg">` overlay for connection lines, freestanding node positioning, per-row evaluation, CSV export, and print-to-PDF export — all vanilla JS, no library, matching the original decision to stay library-free. The `building_settings_fake2` view exists in `core/views.py` (same permission-check pattern as `building_settings_fake`/`building_settings_profile`), the `buildings/<int:pk>/settings/fake2/` route exists in `core/urls.py`, and the "Fake 2" link exists in `settingsDropdownMenu` in `base2.html`. **This task is done — no further work needed on it.**
- **Buildings pages are NOT layout-only.** `buildings_view`, `building_detail_view`, `building_saved_view`, `building_delete_view`, and `building_report_view` are all implemented, `@login_required`, queryset-backed, and permission-checked. `building_detail_view` handles full create/edit via `POST` (validation, file upload for `photo`, `BuildingDatabase` linkage). `building_report_view` calls a live weather API using the building's lat/long. These are functional, not deferred.
- **`building_dashboard.html` is partially done, not "not started."** The Building Profile card is bound to real `selected_building` data (photo, address, etc.). The Insights and Energy Breakdown cards are still explicitly marked in template comments as **static placeholder text** — real data wiring for those two cards remains outstanding.
- **Settings → Profile remains read-only**, as previously documented — `building_settings_profile` does not accept `POST`, and the `.edit-btn` has no behavior. This is confirmed still deferred.

## Known backend ↔ frontend inconsistencies (this is the "make backend and frontend consistent" work)
Found by comparing `core/views.py` against `core/models.py` and the templates it renders:

### 1. Inconsistent permission/auth enforcement across building-tab views
- `building_charts`, `building_systems`, `building_settings_profile`, `building_settings_fake`, `building_settings_fake2` — the "gold standard" pattern: `@login_required` + `_user_can_access_object_client(...)` check + full `**_sidebar_ctx(request)` spread into context.
- `building_energy`, `building_reports` — have `@login_required` but are **missing** the `_user_can_access_object_client` permission check, and **omit** `_sidebar_ctx(request)` from their template context (only pass `selected_building`/`building_tab`).
- `vault_trend_logs`, `vault_objects`, `insight_management`, `create_insight_report`, `manage_rules`, `golden_standard_configuration`, `insight_subscription` — have **no `@login_required` decorator at all**, no permission check, and no `_sidebar_ctx(request)`. Any unauthenticated user hitting these URLs directly is not redirected to login, and any authenticated user from another client can view another client's building data.

This is a security-relevant inconsistency, not just cosmetic — Vault and Insight views should be brought up to the same pattern as Charts/Systems/Settings.

### 2. `core/templates/core/settings_profile.html` has real data-binding bugs
- A broken row: the `<tr>` opening tag before "Building Occupancy:" is missing — the row starts directly at `<td>Building Occupancy:</td>` (malformed table markup).
- "Country:" is **hardcoded to `"Hong Kong"`** instead of `{{ selected_building.get_country_display }}` — never reflects the actual `country` field.
- "Location ID:" is bound to `selected_building.pk` (the database primary key), while the model has a dedicated `code` field (`Building.code`) that is **never displayed anywhere in this template**. This looks like a field-mapping mistake, not an intentional design choice.
- "Weather Station(s):" renders an empty cell — there is no corresponding field on the `Building` model at all, so this row currently displays nothing by design gap, not by data absence.
- Leftover **hardcoded sample-data fallbacks** in `default:` filters: `selected_building.name|default:"Block T 伊利沙伯醫院日間醫療中心新翼"` and `selected_building.dashboard_chart|default:"Block T QE Average Cooling Load Report"` — these should be blank/generic defaults, not a specific sample building's data baked into the template.
- **Model fields that exist on `Building` but are never surfaced on the Settings/Profile page:** `currency`, `latitude`, `longitude`, `weather_unit_group`, `base_temp_cooling`, `base_temp_heating`, `building_database`, `is_active`, `created_at`, `updated_at`. Some of these (e.g. `currency`, lat/long, weather settings) are collected in `building_detail.html`'s form but have no read-only display counterpart on the Settings/Profile page.

### 3. Hardcoded secrets/config inconsistent with `.env` usage
`WEATHER_API_KEY` and `GOOGLE_MAPS_API_KEY` are hardcoded as string literals at the top of `core/views.py`, even though the project already has a `myportal/.env` file for this purpose. Worth moving these into environment variables for consistency with the rest of the config approach (and before this project goes anywhere near a public repo/deployment).

## Existing structure relevant to the next step
- `myportal/templates/base2.html` — dropdown sub-nav pattern implemented for Vault, Insights, and Settings (with "Profile", "Fake", "Fake 2" all live), plus shared `initDropdown(wrapId, toggleId, menuId)` JS helper.
- `myportal/templates/core/settings_profile.html` — read-only `.profile-table` of Building fields with a non-functional Edit button; **now confirmed to have the field-mapping/markup bugs listed above**, on top of the previously-known deferred edit/save work.
- `myportal/templates/core/fake_build_report.html` / `fake_build_report2.html` — **both complete.**
- `myportal/core/views.py` — see permission-consistency findings above; `_sidebar_ctx`, `_require_active_client`, `_user_can_access_object_client` are the shared helpers that should be applied uniformly.
- `myportal/core/urls.py` — all Settings/Vault/Insight/Energy/Reports/Charts/Systems routes registered; no changes needed here for the consistency pass (route names/shapes are fine — it's the *view bodies* that are inconsistent).
- `myportal/core/models.py` — `Building` model is the source of truth; several fields are collected in `building_detail.html` but not shown back on `settings_profile.html`.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile (account-level) | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional + client-scoped |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_saved.html`, `building_report.html` | ✅ Functional (list, create/edit form with POST + validation + photo upload, delete, live-weather report) |
| Dashboard (app-level) | `dashboard.html` | ✅ Functional |
| Building Dashboard | `core/building_dashboard.html` | 🟡 Partially wired — Building Profile card uses real data; Insights & Energy Breakdown cards are still static placeholder text |
| Left panel | Sliding panel in `base.html` | ✅ Functional |
| Django admin | `core/admin.py`, `accounts/admin.py`, `admin_custom.css` | ✅ Complete |
| Vault | `trend_logs.html`, `objects.html` | 🟡 Functional but **missing `@login_required` + permission check** (see inconsistencies) |
| Insight | 5 pages under `insights/` | 🟡 Layout-first + sample data, **missing `@login_required` + permission check** |
| Energy | `energy.html` | 🟡 Functional but missing the `_user_can_access_object_client` check other building-tab views have |
| Reports | `report.html` | 🟡 Same gap as Energy |
| Charts | `chart.html` | ✅ Complete (layout-first, correct permission pattern) |
| Systems | `systems.html` | ✅ Complete (layout-first, correct permission pattern) |
| **Settings → Profile** | `settings_profile.html` | 🔲 Read-only display **with data-binding bugs** (see above), Edit button non-functional — deferred |
| **Settings → Fake** | `fake_build_report.html` | ✅ Complete — single-line chain-track formula/report-builder prototype |
| **Settings → Fake 2** | `fake_build_report2.html` | ✅ **Complete** — node-graph / connection-line variant, fully wired (view + URL + nav link) |

## Active focus: backend ↔ frontend consistency pass
With both Settings/Fake prototypes done, the next stage is a consistency audit and fix pass across the app, targeting the three issue classes found above:
1. **Normalize permission/auth enforcement** on all building-tab views (Vault, Insight, Energy, Reports) to match the Charts/Systems/Settings pattern: `@login_required`, `_user_can_access_object_client(...)` check, and `**_sidebar_ctx(request)` in context.
2. **Fix `settings_profile.html`'s data bindings**: repair the broken `<tr>`, bind Country to the real field, decide whether "Location ID" should show `code` instead of `pk` (or add a separate `code` row), remove hardcoded sample-data fallbacks, and either add rows for the currently-missing model fields or confirm intentionally omitting them.
3. **Move hardcoded API keys** (`WEATHER_API_KEY`, `GOOGLE_MAPS_API_KEY`) into `.env` / Django settings, matching the project's existing `.env` convention.

Buildings pages, `building_dashboard.html`'s remaining static cards (Insights, Energy Breakdown), and the Settings/Profile edit-save feature remain separate, still-pending stages beyond this consistency pass.

## Django admin — completed state
Django admin is fully consistent with the frontend portal view:
- **`core/admin.py`** — complete `ModelAdmin` classes for all core models.
- **`static/css/admin_custom.css`** — BLENDY design token overrides applied to Django admin CSS variables.
- **Admin branding** — `site_header`, `site_title`, and `index_title` are set to the BLENDY product name.

## Project guardrails
- Keep changes targeted; fix one inconsistency category at a time and verify no regressions.
- Avoid unrelated refactors — don't touch `fake_build_report.html`, `fake_build_report2.html`, Groups, Users, Clients, account-level Profile, Charts, Systems, or Django admin while doing the consistency pass.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
