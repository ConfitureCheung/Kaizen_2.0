# TASK

## Current task
Restructure the **Settings icon** in the `base2.html` building-tab nav into a **dropdown sub-nav** (matching the existing Vault and Insights dropdowns), and build a new standalone page, **`core/fake_build_report.html`**, as a **drag-and-drop report-builder prototype** behind a new "Fake" option in that dropdown.

This is treated as an **independent trial task**, deliberately decoupled from the previously planned Settings/Profile edit-save function (see "Deferred work" below). The project expects many more inner pages to be added behind each building-tab icon over time (Vault, Insights, Energy, Reports, Charts, Systems, Settings), and the relationships between them would get complicated fast — so this drag-and-drop pattern is being proven out on its own first, before being reused elsewhere.

## Immediate objective
1. **Settings dropdown**: convert the current plain `<a>` Settings link in `base2.html` into a `dropdown-tab`, copying the exact markup/JS pattern already used for Vault (`vaultDropdownWrap` / `vaultDropdownToggle` / `vaultDropdownMenu`) and Insights (`insightsDropdownWrap` / `insightsDropdownToggle` / `insightsDropdownMenu`), including registering it with the shared `initDropdown(wrapId, toggleId, menuId)` JS helper already defined in `base2.html`. The dropdown should expose two links:
   - **"Profile"** → the existing `building_settings_profile` view / `core/settings_profile.html`, relocated under the dropdown with **no behaviour change** (still read-only, Edit button still non-functional).
   - **"Fake"** → a new `building_settings_fake` view (same `_user_can_access_object_client` permission pattern as `building_settings_profile`/`building_charts`/`building_systems`) at a new URL (e.g. `buildings/<int:pk>/settings/fake/`), rendering the new `core/fake_build_report.html` template.
2. **`core/fake_build_report.html` prototype**: build a page extending `base2.html` with a drag-and-drop canvas/area for assembling **report** content out of draggable blocks/elements, using sample/fake data only (not wired to real building or report data yet). This is purely to prototype the interaction pattern.
3. **Drag-and-drop tooling decision**: pick a client-side JS drag-and-drop library suited to building a report layout (candidates: SortableJS, interact.js, GridStack.js) and decide whether it's loaded via a simple CDN `<script>` tag, or via `npm`/a `package.json` with a bundler/build step. The user isn't sure yet whether a separate Node.js dev server/build process is actually needed for this Django project — evaluate the simplest option that satisfies the drag-and-drop requirement first, and only introduce npm/build tooling if a CDN-based library can't meet the need.

## Background from the previous step
Charts, Systems, and the (unwired) Settings link are in place, and Vault/Insights already demonstrate the target dropdown sub-nav pattern:
- `building_charts`, `building_systems`, and `building_settings_profile` view functions are implemented in `core/views.py`, each `@login_required`, resolving the building via `pk` and enforcing `_user_can_access_object_client`.
- URL patterns `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, and `/buildings/<int:pk>/settings/profile/` are registered in `core/urls.py`.
- `chart.html`, `systems.html`, and `settings_profile.html` are built as templates extending `base2.html`, wired into the building-tab sub-nav with `building_tab` active-state highlighting.
- `settings_profile.html` currently renders a static `.profile-table` of all Building fields with default/fallback sample values shown when a field is blank, plus a toolbar Edit button with no behaviour yet. **Its edit/save function is now deferred** (see "Deferred work" below) rather than being the current focus.
- Vault (`vaultDropdownWrap`) and Insights (`insightsDropdownWrap`) in `base2.html` already implement the dropdown sub-nav pattern this task will copy for Settings.
- `building_dashboard.html` (five empty placeholder cards) is a **separate, still-pending** stage and is explicitly out of scope for this round.

## Scope for the next coding round

**In scope:**
- `myportal/templates/base2.html` — convert the Settings entry into a dropdown-tab with "Profile" and "Fake" links, following the Vault/Insights pattern exactly.
- `myportal/core/views.py` — add a new `building_settings_fake` view, following the `building_settings_profile`/`building_charts`/`building_systems` pattern (permission check, `selected_building`/`selected_client`/`building_tab` context).
- `myportal/core/urls.py` — add a new route (e.g. `buildings/<int:pk>/settings/fake/` → `building_settings_fake`) under the `# ── Settings ──` block.
- `myportal/templates/core/fake_build_report.html` — new template, the drag-and-drop report-builder prototype (sample/fake content only).
- Drag-and-drop JS wiring — either an added CDN `<script>` reference in the template, or (if npm tooling is chosen) a scoped `package.json`/build step for the front-end assets, kept isolated from the rest of the Django project's workflow.

**Out of scope for this round:**
- Implementing the Settings/Profile edit-save function (form class, `POST` handling, editable fields) — this is **deferred** and will be picked back up as its own task later (see below).
- Any changes to `admin.py` files or `admin_custom.css`.
- Structural changes to `static/css/app.css` / `app2.css` (small additive/scoped styles for the new dropdown/prototype only if unavoidable).
- New Django models or migrations.
- `core/building_dashboard.html` and its view — remains a separate future stage.
- Buildings, app-level Dashboard, Groups, Users, Clients, account-level Profile, Vault, Insight, Energy, Reports, Charts, or Systems pages.

## Deferred work: Settings/Profile edit-save function
Kept for reference, not part of this round: make the existing `.edit-btn` on `settings_profile.html` toggle an editable form (name, code, country, state, city, postal, address, timezone, building_phone, building_fax, tech_contact_name/phone/email, building_type, gross_floor_area, occupancy, energy_star_id, dashboard_chart, photo) that submits to `building_settings_profile` via `POST`, validates, and saves to the `Building` model — following the account-level `accounts/profile.html` + `accounts/forms.py` + `accounts/views.py` pattern. All fields already exist on the `Building` model in `core/models.py`; no migration expected when this is picked back up.

## Starting point
- Review `myportal/templates/base2.html`'s existing `vaultDropdownWrap`/`insightsDropdownWrap` markup and the `initDropdown(...)` JS function to confirm the exact dropdown pattern to replicate for Settings.
- Review `myportal/core/views.py`'s `building_settings_profile`, `building_charts`, and `building_systems` for the view pattern (permission check, context variables) to follow for the new `building_settings_fake` view.
- Review `myportal/core/urls.py`'s `# ── Settings ──` block to see where to add the new `fake` route.
- Decide on the drag-and-drop library/tooling approach (CDN vs. npm) before writing `fake_build_report.html`'s JS.

## Expected deliverables
1. Updated `myportal/templates/base2.html` with Settings converted into a working dropdown ("Profile" / "Fake"), matching the Vault/Insights pattern.
2. New `myportal/core/views.py` function `building_settings_fake` (and corresponding URL in `core/urls.py`).
3. New `myportal/templates/core/fake_build_report.html` implementing a working drag-and-drop prototype for assembling report blocks (sample/fake data).
4. A documented decision on the drag-and-drop library and whether Node.js/npm tooling is introduced, including setup instructions if so.

## Acceptance criteria
- The Settings icon in `base2.html` opens a dropdown (like Vault/Insights) with "Profile" and "Fake" options, each linking to the correct page with correct `active` state highlighting.
- Clicking "Profile" behaves exactly as `settings_profile.html` does today (read-only, no regression).
- Clicking "Fake" opens `fake_build_report.html`, where report blocks/elements can be dragged and dropped within the canvas area (sample/fake data is acceptable; no real save/persist logic required yet).
- The existing `_user_can_access_object_client` permission check is enforced on the new `building_settings_fake` view, consistent with other building-tab views.
- No regressions in any existing pages, including Vault, Insight, Energy, Reports, Charts, and the (relocated but otherwise unchanged) Settings/Profile page.
- `app.css` and all admin files are untouched (aside from any minor, additive, clearly-scoped CSS if genuinely unavoidable).
- `building_dashboard.html` and the Settings/Profile edit-save function are left unchanged in this round.
