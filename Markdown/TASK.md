# TASK

## Current task
**Backend ↔ frontend consistency pass.** The previous task (`core/fake_build_report2.html`, the node-graph formula-builder prototype) is confirmed **complete** — template, view, URL, and nav link all exist and work. This task shifts focus to auditing and fixing places where `core/views.py` (backend) and the templates it renders (frontend) have drifted apart, found by direct inspection of the current code.

## Background: what closed out the previous round
- `core/fake_build_report2.html` (1,605 lines) implements the full node-canvas + SVG connection-line formula builder: CSV upload, draggable column plates, operator/bracket/function/aggregate palettes, freestanding nodes on `#frb2Canvas`, connections drawn via `#frb2Svg`, per-row evaluation, saved formulas, CSV export, and print-to-PDF export. Vanilla JS + SVG only — no library was needed, confirming the original default assumption.
- `building_settings_fake2` view exists in `core/views.py`, matching the `building_settings_fake` / `building_settings_profile` permission-check pattern (`@login_required`... actually note: `building_settings_fake`/`building_settings_fake2` currently have **no** `@login_required` decorator either — verify this during the audit below, since it wasn't flagged in the original plan).
- `buildings/<int:pk>/settings/fake2/` route exists in `core/urls.py`.
- `settingsDropdownMenu` in `base2.html` has a live "Fake 2" link alongside "Profile" and "Fake".

**No further work is needed on fake_build_report2.html, its view, its URL, or its nav link.**

## Immediate objective: fix three concrete inconsistency classes

### 1. Normalize permission/auth enforcement across building-tab views
Audit confirmed these views do **not** follow the same pattern as `building_charts`/`building_systems`/`building_settings_profile` (`@login_required` + `_user_can_access_object_client(request, building.client_id)` + `**_sidebar_ctx(request)` in context):
- `vault_trend_logs`, `vault_objects` — no `@login_required`, no permission check, no `_sidebar_ctx`.
- `insight_management`, `create_insight_report`, `manage_rules`, `golden_standard_configuration`, `insight_subscription` — same gaps.
- `building_energy`, `building_reports` — have `@login_required` but are missing the `_user_can_access_object_client` check and `_sidebar_ctx`.
- **Also verify** `building_settings_fake` and `building_settings_fake2` — during this audit these did not show a `@login_required` decorator in the current file; confirm and add if missing, since they render pages reachable by pk in the URL just like the others.

**Fix:** bring all of the above in line with the Charts/Systems/Settings pattern — add `@login_required`, add the `_user_can_access_object_client` check (raise `PermissionDenied` on failure), and spread `**_sidebar_ctx(request)` into the render context so the left panel renders correctly on every building-tab page.

### 2. Fix data-binding bugs in `core/templates/core/settings_profile.html`
Confirmed by reading the template line-by-line:
- Missing `<tr>` opening tag directly before the "Building Occupancy:" row — malformed table markup.
- "Country:" row is hardcoded to the literal text `Hong Kong`, not bound to `selected_building.country`/`get_country_display`.
- "Location ID:" row is bound to `selected_building.pk` — the model's actual `code` field (`Building.code`) is never rendered anywhere on this page. Decide: should "Location ID" show `code` instead, or should a separate `code` row be added, keeping `pk` if that's intentional?
- "Weather Station(s):" has no data source — there's no matching model field; decide whether to remove the row, add a model field, or leave it clearly marked as not-yet-implemented rather than silently blank.
- `default:` fallbacks contain leftover sample data (`"Block T 伊利沙伯醫院日間醫療中心新翼"` for name, `"Block T QE Average Cooling Load Report"` for dashboard_chart) instead of generic/blank fallbacks — replace with `default:""` or a neutral placeholder.
- Fields that exist on `Building` but have no row on this page at all: `currency`, `latitude`, `longitude`, `weather_unit_group`, `base_temp_cooling`, `base_temp_heating`, `building_database`, `is_active`, `created_at`, `updated_at`. Several of these (currency, lat/long, weather unit group) are already collected via `building_detail.html`'s form — decide which of these should get a corresponding read-only row here for full backend/frontend parity, versus which are intentionally internal-only.

**Fix:** repair the markup, correct/confirm each field binding, remove hardcoded sample fallbacks, and add rows (or explicitly document exclusion) for the currently-missing model fields.

### 3. Move hardcoded secrets into environment config
`WEATHER_API_KEY` and `GOOGLE_MAPS_API_KEY` are hardcoded string literals at the top of `core/views.py`, despite `myportal/.env` already existing in the project for exactly this purpose.

**Fix:** move both keys into `.env`, read them via `django-environ`/`os.environ`/whatever pattern `config/settings.py` already uses for other secrets, and update `core/views.py` to reference the settings value instead of a literal.

## Scope for this round

**In scope:**
- `myportal/core/views.py` — permission/decorator normalization on `vault_trend_logs`, `vault_objects`, the 5 insight views, `building_energy`, `building_reports`; verify and fix `building_settings_fake`/`building_settings_fake2` decorators; move `WEATHER_API_KEY`/`GOOGLE_MAPS_API_KEY` to settings/env.
- `myportal/templates/core/settings_profile.html` — markup fix + field-binding corrections + fallback cleanup + missing-field decision.
- `myportal/config/settings.py` and `myportal/.env` — add the two API key settings, read from env.

**Out of scope for this round:**
- Any changes to `fake_build_report.html` or `fake_build_report2.html` — both are done, don't touch them.
- Implementing the Settings/Profile **edit-save** function (form class, `POST` handling) — still a separate, deferred task; this round only fixes the *read-only display* bindings.
- `building_dashboard.html`'s remaining static placeholder cards (Insights, Energy Breakdown) — separate future stage.
- Buildings pages (`buildings.html`, `building_detail.html`, `building_saved.html`, `building_report.html`) — these were previously mis-documented as "deferred" but are actually already functional; leave them alone this round unless the audit surfaces a specific bug in them.
- Groups, Users, Clients, account-level Profile, Charts, Systems — already consistent, no changes needed.
- Any changes to `admin.py` files, `admin_custom.css`, or new Django models/migrations.

## Deferred work (unchanged, kept for reference)
- **Settings/Profile edit-save function**: make `.edit-btn` toggle an editable form covering all `Building` fields (including `photo`), submitting via `POST` to `building_settings_profile`, validated and saved — following the `accounts/profile.html` + `accounts/forms.py` + `accounts/views.py` pattern. Do this only *after* the read-only field-binding fixes above, so the edit form and the display are both correct against the same field list.
- **`building_dashboard.html`**: wire the Insights and Energy Breakdown cards to real data once a data source/query is defined for them.

## Starting point
- Re-read `core/views.py` top-to-bottom for every `building_*`/`vault_*`/`insight_*` function and note which ones deviate from the `@login_required` + `_user_can_access_object_client` + `_sidebar_ctx` pattern (list above is a starting checklist, confirm against the live file since line numbers will shift).
- Re-read `core/templates/core/settings_profile.html` fully and cross-reference every `selected_building.<field>` reference against the `Building` model field list in `core/models.py`.
- Check `config/settings.py` for the existing pattern used to load other secrets from `.env` (e.g. `SECRET_KEY`, DB credentials) and mirror that pattern for the two API keys.

## Expected deliverables
1. Updated `core/views.py` with consistent `@login_required` + permission-check + `_sidebar_ctx` usage across all building-tab views, and API keys sourced from settings/env instead of hardcoded.
2. Updated `core/templates/core/settings_profile.html` with the markup bug fixed, correct field bindings, cleaned-up fallbacks, and a resolved decision on the currently-missing model fields (either added as new rows or explicitly left out with a one-line note in the template/comment for future reference).
3. Updated `config/settings.py` / `.env` with `WEATHER_API_KEY` and `GOOGLE_MAPS_API_KEY` as environment-driven settings.
4. `Markdown/HANDOFF.md`, `Markdown/PROJECT_OVERVIEW.md`, `Markdown/TASK.md` kept in sync as this consistency pass progresses.

## Acceptance criteria
- All building-tab views (`vault_trend_logs`, `vault_objects`, the 5 insight views, `building_energy`, `building_reports`, and confirmed `building_settings_fake`/`fake2`) require login, enforce `_user_can_access_object_client`, and pass full sidebar context — matching Charts/Systems/Settings.
- `settings_profile.html` renders valid HTML (no missing `<tr>`), every displayed value is bound to its correct model field (no hardcoded "Hong Kong", no mislabeled `pk`-as-code), and no sample building data remains in `default:` fallbacks.
- `WEATHER_API_KEY` and `GOOGLE_MAPS_API_KEY` no longer appear as literals in `core/views.py`.
- No regressions in `fake_build_report.html`, `fake_build_report2.html`, Buildings, Groups, Users, Clients, app-level Dashboard, Charts, or Systems.
- `app.css`/`app2.css` structural rules and all admin files remain untouched.
