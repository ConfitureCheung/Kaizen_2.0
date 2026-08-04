# HANDOFF

## Current status
The BLENDY Django project has its main structure in place: `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings.

**Correction to earlier handoff notes:** re-reading the live code shows the project is further along than previously written up, and the previous "next task" is finished:

- **`core/fake_build_report2.html` (the node-graph formula-builder prototype) is DONE.** It's a full 1,605-line template with a canvas-based mid panel: draggable column plates on the left, operator/bracket/function/aggregate palettes, a `#frb2Canvas` drop area where dragged items land as freestanding nodes, an `#frb2Svg` SVG overlay drawing connection lines between nodes, per-row formula evaluation, saved formulas, CSV export, and print-to-PDF export — all vanilla JS/SVG, no library, confirming the original default plan. The `building_settings_fake2` view, the `buildings/<int:pk>/settings/fake2/` URL, and the "Fake 2" link in `settingsDropdownMenu` (`base2.html`) are all in place and wired correctly. **Nothing further is needed here.**
- **Buildings pages are not layout-only.** `buildings_view`, `building_detail_view` (full create/edit form with `POST` handling, validation, photo upload, `BuildingDatabase` linkage), `building_saved_view`, `building_delete_view`, and `building_report_view` (live weather API call using the building's coordinates) are all implemented and working.
- **`building_dashboard.html` is partially wired**, not untouched: the Building Profile card renders real `selected_building` data; the Insights and Energy Breakdown cards are explicitly commented in the template as static placeholder text, still pending real data.
- **Settings → Profile is still read-only** as before — confirmed unchanged, `.edit-btn` has no behavior, and the view doesn't accept `POST`.

## New focus: backend ↔ frontend consistency pass
The user's stated next step is to make the Django backend (`core/views.py`, `core/models.py`) consistent with the website frontend (templates). Auditing the current code turned up three concrete, fixable issue classes — these are now the active task (see `TASK.md` for full detail):

1. **Inconsistent auth/permission enforcement across building-tab views.**
   - Solid pattern (`@login_required` + `_user_can_access_object_client` + `**_sidebar_ctx(request)`): `building_charts`, `building_systems`, `building_settings_profile`.
   - Missing the permission check + sidebar context (but has `@login_required`): `building_energy`, `building_reports`.
   - Missing `@login_required` entirely, no permission check, no sidebar context: `vault_trend_logs`, `vault_objects`, `insight_management`, `create_insight_report`, `manage_rules`, `golden_standard_configuration`, `insight_subscription`.
   - Also missing `@login_required`: `building_settings_fake`, `building_settings_fake2` — worth fixing even though these are otherwise "done" prototypes, since they're reachable by any unauthenticated request to their URL.

2. **`settings_profile.html` has real field-binding bugs**, not just missing features:
   - A malformed table row (missing `<tr>` before "Building Occupancy:").
   - "Country:" hardcoded to the string `Hong Kong` instead of bound to the actual `country` field.
   - "Location ID:" shows `selected_building.pk` while the model's dedicated `code` field is never displayed anywhere on the page.
   - "Weather Station(s):" has no backing model field at all.
   - Leftover hardcoded sample-data fallbacks (a specific building's Chinese name, a specific chart name) baked into `default:` filters instead of blank/neutral defaults.
   - Several real `Building` model fields (`currency`, `latitude`, `longitude`, `weather_unit_group`, `base_temp_cooling`, `base_temp_heating`, `building_database`, `is_active`, `created_at`, `updated_at`) are collected elsewhere (e.g. `building_detail.html`'s form) but never shown back on this read-only page.

3. **Hardcoded secrets**: `WEATHER_API_KEY` and `GOOGLE_MAPS_API_KEY` are literal strings at the top of `core/views.py`, despite a `myportal/.env` file already existing in the project for this purpose.

## What is already done
- Custom auth model, login/logout flow, shared authenticated shell (`base.html`) with sliding left panel (Client → Building tree).
- Groups, Clients, Users pages — fully functional, client-scoped.
- Account-level Profile (`accounts/profile.html`) — save flow, avatar upload, Django admin visibility — this remains the reference pattern for any future settings_profile.html save flow.
- `dashboard.html` (app-level) — fully functional, queryset-backed KPIs, activity feed, alerts.
- **Django admin is fully consistent with the frontend.**
- **Vault, Insight, Energy, Reports, Charts, Systems** — all functionally present (Vault/Insight are layout-first + sample data for some sub-pages), but see the permission-consistency gaps above.
- **Settings dropdown** — complete, with three working links: Profile (read-only), Fake (complete), Fake 2 (complete).
- **Buildings** (list, create/edit, delete, live-weather report) — functional, queryset- and form-backed.
- **`building_dashboard.html`** — Building Profile card is real-data; Insights/Energy Breakdown cards remain placeholder.

## What is not yet done — current target
**Backend ↔ frontend consistency fixes**, in three parts (see `TASK.md` for the full checklist and acceptance criteria):
1. Normalize `@login_required` + `_user_can_access_object_client` + `_sidebar_ctx` usage across `vault_trend_logs`, `vault_objects`, the 5 insight views, `building_energy`, `building_reports`, and add the missing `@login_required` to `building_settings_fake`/`building_settings_fake2`.
2. Fix `core/templates/core/settings_profile.html`: repair the broken `<tr>`, correct the Country/Location ID bindings, remove hardcoded sample-data fallbacks, and decide on adding rows for the currently-unsurfaced model fields.
3. Move `WEATHER_API_KEY` and `GOOGLE_MAPS_API_KEY` out of `core/views.py` and into `.env`/`config/settings.py`.

## Important implementation notes
- Do **not** touch `fake_build_report.html` or `fake_build_report2.html` — both are complete and working.
- Do **not** start the Settings/Profile edit-save function yet — fix the read-only field bindings first so the eventual edit form is built against a correct field list, not the current buggy one.
- Do **not** touch `building_dashboard.html`'s remaining placeholder cards (Insights, Energy Breakdown) in this round — separate future stage.
- Buildings pages, Groups, Users, Clients, account-level Profile, Charts, Systems, and Django admin are already in good shape — leave them alone unless the consistency audit surfaces a specific, concrete bug in them.
- Keep `app.css`/`app2.css` structural rules and all admin files untouched.

## Relevant files for the next session
- `myportal/core/views.py` — apply the permission/decorator normalization; relocate the two hardcoded API keys.
- `myportal/templates/core/settings_profile.html` — fix markup + field bindings + fallbacks; decide on missing-field rows.
- `myportal/config/settings.py`, `myportal/.env` — add `WEATHER_API_KEY` / `GOOGLE_MAPS_API_KEY` as env-driven settings, following whatever pattern is already used there for other secrets.
- `myportal/core/models.py` — source of truth for the `Building` field list used to check `settings_profile.html`'s completeness.
- `Markdown/HANDOFF.md`, `Markdown/PROJECT_OVERVIEW.md`, `Markdown/TASK.md` — keep in sync as this consistency pass progresses.

## Next task
Carry out the **backend ↔ frontend consistency pass** described above and in `TASK.md`: normalize permission/auth handling across building-tab views, fix the `settings_profile.html` data-binding bugs, and move hardcoded API keys into environment config.

This next step should include:
- Re-verifying the current decorator/permission-check state of every `building_*`/`vault_*`/`insight_*` view against the checklist above (line numbers will have shifted since this audit).
- Applying the `@login_required` + `_user_can_access_object_client` + `_sidebar_ctx` pattern uniformly, without changing the URLs, template names, or `building_tab` values already in use.
- Walking through `settings_profile.html` line by line against `Building`'s field list in `core/models.py` and fixing each binding issue found.
- Adding `WEATHER_API_KEY`/`GOOGLE_MAPS_API_KEY` to `.env` and reading them via `config/settings.py`, then updating `core/views.py` to reference `settings.WEATHER_API_KEY` / `settings.GOOGLE_MAPS_API_KEY` instead of literals.

## Constraints for the next edit
- Focus only on: `core/views.py` (permission normalization + API key relocation), `templates/core/settings_profile.html` (field-binding fixes), `config/settings.py` + `.env` (new env-driven settings).
- Do **not** implement the Settings/Profile edit-save function in this round.
- Do not start or resume work on `building_dashboard.html`'s remaining placeholder cards.
- Do not modify `fake_build_report.html`, `fake_build_report2.html`, Buildings, Groups, Users, Clients, account-level Profile, Charts, Systems, Django admin, or `app.css`/`app2.css` structurally.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: backend <-> frontend consistency pass on the BLENDY Django
project. Two prior prototype tasks (fake_build_report.html and
fake_build_report2.html) are both complete and must not be touched.

Fix these three issue classes:

1. Permission/auth normalization in core/views.py:
   - vault_trend_logs, vault_objects, insight_management,
     create_insight_report, manage_rules, golden_standard_configuration,
     insight_subscription currently have NO @login_required decorator, no
     _user_can_access_object_client(request, building.client_id) check, and
     don't spread **_sidebar_ctx(request) into their render context.
   - building_energy and building_reports have @login_required but are
     missing the _user_can_access_object_client check and _sidebar_ctx.
   - building_settings_fake and building_settings_fake2 are missing
     @login_required.
   Bring all of these in line with the pattern already used by
   building_charts / building_systems / building_settings_profile:
   @login_required, then get_object_or_404, then
   _user_can_access_object_client check (raise PermissionDenied on
   failure), then render with **_sidebar_ctx(request) plus the existing
   context keys. Do not change URL names, template names, or building_tab
   values.

2. Fix templates/core/settings_profile.html:
   - There's a missing <tr> opening tag right before the "Building
     Occupancy:" row - fix the malformed table markup.
   - "Country:" is hardcoded to the literal "Hong Kong" - bind it to
     {{ selected_building.get_country_display }} instead.
   - "Location ID:" shows {{ selected_building.pk }} but the Building model
     has a separate `code` field that's never shown anywhere on this page -
     add a row for `code` (keep or relabel the pk row as you see fit, just
     make sure `code` is visible somewhere).
   - Remove the hardcoded sample-data fallbacks in the `default:` filters
     for `name` and `dashboard_chart` (currently a specific building's
     Chinese name and a specific chart name) - use `default:""` instead.
   - Building model fields with no row on this page at all: currency,
     latitude, longitude, weather_unit_group, base_temp_cooling,
     base_temp_heating, building_database, is_active, created_at,
     updated_at. Add read-only rows for currency, latitude/longitude, and
     weather_unit_group/base_temp_cooling/base_temp_heating (these are
     already collected in building_detail.html's form), following the
     existing .profile-table row markup pattern. Leave is_active,
     building_database, created_at, updated_at out unless you think they
     add clear value.

3. Move hardcoded secrets: WEATHER_API_KEY and GOOGLE_MAPS_API_KEY are
   literal strings at the top of core/views.py. Move them into myportal/.env
   and read them in config/settings.py using whatever pattern is already
   used there for other secrets, then update core/views.py to reference
   settings.WEATHER_API_KEY / settings.GOOGLE_MAPS_API_KEY.

Constraints:
- do not touch fake_build_report.html or fake_build_report2.html
- do not implement the Settings/Profile edit-save function (the .edit-btn
  staying non-functional is fine for this round)
- do not touch building_dashboard.html
- do not touch Buildings, Groups, Users, Clients, account-level Profile,
  Charts, Systems, or Django admin files
- do not modify app.css/app2.css structurally
Please return complete updated files only for core/views.py,
templates/core/settings_profile.html, config/settings.py, and .env.
```
