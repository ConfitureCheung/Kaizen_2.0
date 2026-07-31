# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) remain layout-only or sample-data driven and are **deferred** to a later stage.
The Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, and Charts/Systems sections are all **layout/route complete** — all eight building-tab icons in `base2.html` (Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings) point to real routes with `active` state highlighting; none are `href="#"` placeholders.
Settings is currently a **single plain link** (`building_settings_profile` → `core/settings_profile.html`, a read-only profile table with a toolbar Edit button that has no behaviour yet). The previously planned "make settings_profile.html editable" work is **deferred and decoupled** for now (see below) in favour of a more pressing, independent trial task.

The **next active implementation stage is a standalone drag-and-drop prototype**: `core/fake_build_report.html`, reached through a **new "Settings" dropdown sub-nav** (built the same way as the existing Vault and Insights dropdowns). This is deliberately treated as an **isolated experiment**, not part of the Settings/Profile edit-save chain — the plan is to eventually add many more inner pages under each building-tab icon (Vault, Insights, Energy, Reports, Charts, Systems, Settings), and the relationships between all of them would get complicated fast if this prototype were tangled into the existing Profile work. Building it standalone first lets the drag-and-drop pattern (and the JS/tooling decisions behind it) get proven out before being reused elsewhere.
The `building_dashboard.html` content work (five empty placeholder cards) documented previously remains a separate, still-pending stage and has **not** been started.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups, Clients, and Users pages are fully functional (client-scoped where relevant).
- Account-level Profile page (`accounts/profile.html`) save flow, avatar upload, and Django admin visibility are implemented — this is the reference pattern to follow for any future settings_profile.html save flow.
- `dashboard.html` (app-level dashboard, not building-scoped) is fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- The sliding left panel in `base.html` is fully interactive.
- **Django admin is fully consistent with the frontend view**.
- **Vault section is complete**: `trend_logs.html` and `objects.html` are both live, reading data from the building-linked SQLite database via raw `sqlite3` connections. Vault is exposed via a **dropdown sub-nav** in `base2.html` (`vaultDropdownWrap` / `vaultDropdownToggle` / `vaultDropdownMenu`) — this is the pattern the new Settings dropdown will copy.
- **Insight section is complete (layout-first)**: all five pages (`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`) extend `base2.html`, using static/sample data and sub-navigation tabs. Insights also uses the same dropdown sub-nav pattern (`insightsDropdownWrap` / `insightsDropdownToggle` / `insightsDropdownMenu`).
- **Energy & Report section is complete**: `energy.html` (`building_energy` view) and `report.html` (`building_reports` view), both extending `base2.html` and wired into the building-tab sub-nav.
- **Charts and Systems are complete (layout-first)**: `building_charts` renders `core/chart.html`, `building_systems` renders `core/systems.html`.
- **Settings/Profile page exists but is read-only, and is not yet in a dropdown**: `building_settings_profile` view (`/buildings/<pk>/settings/profile/`) resolves the building via `pk`, enforces `_user_can_access_object_client`, and renders `core/settings_profile.html` with `selected_building`/`selected_client`/`building_tab="settings"`. The template displays all Building model fields (name, code/location id, country, state, city, postal, address, timezone, phone, fax, technical contact name/phone/email, building type, gross floor area, occupancy, energy_star_id, dashboard_chart) as a static two-column table. The `Building` model (`core/models.py`) already has all of these fields defined, so no schema/migration work is expected whenever the edit/save function is eventually picked back up.

## What is not yet done — current target
**Settings dropdown restructuring + `core/fake_build_report.html` drag-and-drop prototype.** This is now the active target, and it is intentionally split from the (deferred) Settings/Profile edit-save work:

1. **Convert Settings into a dropdown sub-nav in `base2.html`**, mirroring the existing `vaultDropdownWrap`/`insightsDropdownWrap` markup and `initDropdown(...)` JS calls. The dropdown should expose two options:
   - **"Profile"** → the existing `building_settings_profile` view / `core/settings_profile.html` (relocated under the dropdown, behaviour unchanged for now — still read-only, Edit button still has no function; that work stays deferred).
   - **"Fake"** → a new view (e.g. `building_settings_fake`) and new URL (e.g. `buildings/<int:pk>/settings/fake/`) rendering the new `core/fake_build_report.html` template.
2. **Build `core/fake_build_report.html` as a standalone drag-and-drop prototype** whose purpose is to explore building a **report layout via drag-and-drop** (dragging report elements/blocks into a canvas to assemble a report) — not to be wired into real building/report data yet. It should extend `base2.html` like the other building-tab pages, with `building_tab="settings"` (or a dedicated sub-tab flag) so the sidebar/nav states stay correct.
3. **Decide on the drag-and-drop implementation approach**, which is still open:
   - A client-side JS drag-and-drop library is needed (candidates: SortableJS, interact.js, GridStack.js).
   - Whether that library is pulled in via a simple CDN `<script>` tag (no Node.js needed), or via `npm`/a `package.json` with a bundler/build step, is **not yet decided** — to be settled in the next session based on how much build tooling the user wants to introduce into this otherwise Node-free Django project.
   - The user's stated purpose for drag-and-drop here is specifically to prototype **report building** (arranging report content/blocks), so the chosen library should be evaluated against that use case, not just generic list reordering.

## Important implementation notes
- Treat this as an **independent trial task** — do not entangle it with the Settings/Profile edit-save plan, and do not assume its patterns/decisions must be reused as-is elsewhere yet. It exists to prove out a drag-and-drop approach that will likely inform many future inner pages across the other building-tab icons (Vault, Insights, Energy, Reports, Charts, Systems), which are expected to grow into more complex, multi-page sections over time.
- Follow the existing dropdown pattern exactly (`building-tab dropdown-tab`, `building-tab-button`, `building-tab-dropdown`, `building-tab-dropdown-link` classes, plus the `initDropdown(wrapId, toggleId, menuId)` JS helper already defined in `base2.html`) so Settings behaves identically to Vault/Insights.
- `core/settings_profile.html`'s existing `.settings-profile-page` / `.profile-card` / `.profile-table` / `.edit-btn` styling should be left untouched — only its entry point in the nav changes (moves under the new dropdown as "Profile").
- Keep `fake_build_report.html` clearly labelled/scoped as a prototype (e.g. sample/fake data only) so it's obvious it isn't a finished, data-backed report page yet.
- `building_dashboard.html` (five placeholder cards: Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts) remains a **separate, still-pending** stage — do not work on it in this round.

## Relevant files for the next session
- `myportal/templates/base2.html` — convert the plain Settings `<a>` link into a dropdown-tab (`Profile` / `Fake` options), following the existing Vault/Insights dropdown markup and JS.
- `myportal/templates/core/fake_build_report.html` — **new file**, the drag-and-drop report-builder prototype page.
- `myportal/core/views.py` — add a new `building_settings_fake` view (same permission-check pattern as `building_settings_profile`, `building_charts`, `building_systems`).
- `myportal/core/urls.py` — add a new URL pattern under the `# ── Settings ──` section, e.g. `buildings/<int:pk>/settings/fake/` → `building_settings_fake`.
- `myportal/static/js/app.js` (or a new scoped JS file/CDN script) — home for the drag-and-drop logic, once the library/tooling decision is made.
- `myportal/templates/core/settings_profile.html` — unchanged in this round aside from now being reached via the new dropdown's "Profile" option.
- `Markdown/HANDOFF.md`, `Markdown/PROJECT_OVERVIEW.md`, `Markdown/TASK.md` — keep in sync as this prototype task and the deferred Profile edit-save task both evolve.

## Next task
Work on **restructuring the Settings icon into a dropdown ("Profile" / "Fake")** and **building `core/fake_build_report.html`** as an independent drag-and-drop report-builder prototype — following the Vault/Insights dropdown pattern for navigation, and deciding on a JS drag-and-drop library plus whether Node.js/npm tooling is warranted for this project.

This next step should include:
- Reviewing `base2.html`'s existing `vaultDropdownWrap`/`insightsDropdownWrap` markup and `initDropdown(...)` JS to confirm the dropdown pattern to replicate for Settings.
- Adding the new `building_settings_fake` view and URL, following the `building_settings_profile`/`building_charts`/`building_systems` pattern (permission check, `selected_building`/`selected_client`/`building_tab` context).
- Creating `core/fake_build_report.html` extending `base2.html`, with a drag-and-drop canvas/area for assembling report blocks (sample/fake content only for now).
- Choosing and wiring in a drag-and-drop JS library (CDN vs. npm-managed), documenting the decision and rationale.
- Relocating the existing Profile link under the new Settings dropdown without changing its behaviour.

## Constraints for the next edit
- Focus only on: the Settings dropdown restructuring in `base2.html`, the new `fake_build_report.html` prototype, its view/URL, and whatever minimal JS/library wiring the drag-and-drop needs.
- Do **not** implement the Settings/Profile edit-save function in this round — that work is deferred and will be picked back up as its own task later.
- Do not start work on `building_dashboard.html` in this round — it remains a separate future stage.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Users, app-level Dashboard, Vault, Insight, Energy, Reports, Charts, Systems, Left panel, Admin).
- Do not modify `static/css/app.css`/`app2.css` structurally (adding small scoped styles for the new dropdown/prototype is acceptable if unavoidable) or any existing admin files.
- If Node.js/npm tooling is introduced, keep it clearly scoped/documented (e.g. a dedicated `package.json` for front-end drag-and-drop assets) so it doesn't disrupt the existing Django `runserver` workflow.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: restructure the Settings icon in base2.html into a dropdown
sub-nav (like the existing Vault/Insights dropdowns), with two options:
"Profile" (the existing building_settings_profile / settings_profile.html,
relocated but otherwise unchanged) and "Fake" (a new
core/fake_build_report.html prototype page).
Then build core/fake_build_report.html as a standalone drag-and-drop
report-builder prototype (sample/fake content, not wired to real data yet).

Constraints:
- follow the exact dropdown markup/JS pattern already used for Vault
  (vaultDropdownWrap/vaultDropdownToggle/vaultDropdownMenu) and Insights
  (insightsDropdownWrap/insightsDropdownToggle/insightsDropdownMenu) in base2.html
- add a new building_settings_fake view in core/views.py following the
  same permission-check pattern as building_settings_profile
- add a new URL (e.g. buildings/<int:pk>/settings/fake/) in core/urls.py
- this is an independent trial task — do not implement the
  Settings/Profile edit-save function in this round
- do not touch building_dashboard.html in this round
- propose a drag-and-drop JS approach (CDN library vs. npm-managed with a
  build step) suited to assembling report blocks, and explain the tradeoff
- no modifications to app.css structurally, admin files, or already-completed views
Reference:
- templates/base2.html for the existing Vault/Insights dropdown pattern
- core/views.py's building_settings_profile / building_charts / building_systems
  for the view pattern to follow
- core/urls.py for the Settings section URL block to extend
Please return complete updated files only.
```
