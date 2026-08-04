# TASK

## Current task
Build **`core/fake_build_report2.html`**, a second standalone drag-and-drop formula/report-builder prototype, matching the **exact same functional requirements** as the now-complete `core/fake_build_report.html`, but with a **different mid-panel layout**: instead of dragging items into a single horizontal "one-liner" chain track, this version drags items into an **open panel/canvas and links them together with connection lines** (a node-graph / flow-diagram style builder).

This is treated as an **independent trial task**, the same way `fake_build_report.html` was — deliberately decoupled from the deferred Settings/Profile edit-save function (see "Deferred work" below), and without modifying the existing, working `fake_build_report.html`.

## Immediate objective
1. **Functional parity with `fake_build_report.html`**:
   - Left panel: CSV upload, header/column detection (numeric vs. text), draggable column "plates".
   - Draggable primitives: operators (`+ − × ÷ ^ %`), grouping (bracket), functions (`ABS`/`ROUND`/`SQRT`), aggregates (`SUM`/`AVG`/`MIN`/`MAX`/`COUNT`).
   - Ability to assemble one or more formulas from these primitives, save them, and list saved formulas.
   - Right panel: per-row computed answers for each saved formula, plus CSV export and print-to-PDF export.
2. **New mid-panel interaction — canvas + connection lines**: replace the single-line chain track with an open drop area where each dragged item (column, operator, bracket, function, aggregate) becomes a **freestanding node** positioned wherever it's dropped. The user then **draws a connection line from one node to another** to indicate how they combine into a formula (e.g. column node → operator node → column node to express `ColA + ColB`). Removing a node or a connection should update the resulting formula/graph accordingly.
3. **Navigation**: add a **"Fake 2"** link to the existing `settingsDropdownMenu` in `base2.html` (alongside "Profile" and "Fake"), following the exact dropdown-link markup already used there, plus a new `building_settings_fake2` view and `buildings/<int:pk>/settings/fake2/` URL, mirroring `building_settings_fake` / `buildings/<int:pk>/settings/fake/`.
4. **Implementation approach for nodes + connection lines**: default to staying library-free — absolutely positioned, draggable node `div`s plus an `<svg>` overlay whose `<line>`/`<path>` elements are recalculated whenever a connected node moves. Only consider a small graph/diagram library (e.g. jsPlumb, LeaderLine) if hand-rolled SVG positioning proves genuinely unworkable, and document that decision explicitly if made.

## Background from the previous step
The Settings dropdown restructuring and the first prototype are now complete:
- `base2.html`'s Settings entry is a working dropdown (`settingsDropdownWrap`/`settingsDropdownToggle`/`settingsDropdownMenu`), matching the Vault (`vaultDropdownWrap`) and Insights (`insightsDropdownWrap`) pattern, with "Profile" and "Fake" links.
- `building_settings_profile` and `building_settings_fake` view functions exist in `core/views.py`, each `@login_required`, resolving the building via `pk` and enforcing `_user_can_access_object_client`.
- URL patterns `/buildings/<int:pk>/settings/profile/` and `/buildings/<int:pk>/settings/fake/` are registered in `core/urls.py`.
- **`core/fake_build_report.html` is complete**: a working drag-and-drop formula/report builder using a single horizontal chain track in its mid panel (CSV → column plates → operator/bracket/function/aggregate chips → chain track → saved formulas → per-row answers → CSV/PDF export). Built entirely in vanilla JS (no drag-and-drop library, no npm/build tooling) — this settles the tooling question raised in the previous round in favor of a library-free approach.
- `settings_profile.html` still renders a static `.profile-table` of Building fields with a toolbar Edit button with no behaviour yet. **Its edit/save function remains deferred** (see "Deferred work" below).
- `building_dashboard.html` (five empty placeholder cards) is a **separate, still-pending** stage and is explicitly out of scope for this round.

## Scope for the next coding round

**In scope:**
- `myportal/templates/core/fake_build_report2.html` — new template, the node/graph-based report-builder prototype (sample/fake content only), matching `fake_build_report.html`'s functional scope.
- `myportal/templates/base2.html` — add a "Fake 2" link to the existing `settingsDropdownMenu`.
- `myportal/core/views.py` — add a new `building_settings_fake2` view, following the `building_settings_fake`/`building_settings_profile` pattern (permission check, `selected_building`/`selected_client`/`building_tab` context).
- `myportal/core/urls.py` — add a new route (e.g. `buildings/<int:pk>/settings/fake2/` → `building_settings_fake2`) under the `# ── Settings ──` block.
- Node-canvas + connection-line JS wiring — vanilla JS + SVG overlay by default, reusing `fake_build_report.html`'s CSV parsing / aggregate computation / CSV-PDF export logic where practical.

**Out of scope for this round:**
- Any changes to the existing, working `core/fake_build_report.html`.
- Implementing the Settings/Profile edit-save function (form class, `POST` handling, editable fields) — this is **deferred** and will be picked back up as its own task later (see below).
- Any changes to `admin.py` files or `admin_custom.css`.
- Structural changes to `static/css/app.css` / `app2.css` (small additive/scoped styles for the new canvas/nodes/connection lines only if unavoidable).
- New Django models or migrations.
- `core/building_dashboard.html` and its view — remains a separate future stage.
- Buildings, app-level Dashboard, Groups, Users, Clients, account-level Profile, Vault, Insight, Energy, Reports, Charts, or Systems pages.

## Deferred work: Settings/Profile edit-save function
Kept for reference, not part of this round: make the existing `.edit-btn` on `settings_profile.html` toggle an editable form (name, code, country, state, city, postal, address, timezone, building_phone, building_fax, tech_contact_name/phone/email, building_type, gross_floor_area, occupancy, energy_star_id, dashboard_chart, photo) that submits to `building_settings_profile` via `POST`, validates, and saves to the `Building` model — following the account-level `accounts/profile.html` + `accounts/forms.py` + `accounts/views.py` pattern. All fields already exist on the `Building` model in `core/models.py`; no migration expected when this is picked back up.

## Starting point
- Review `myportal/templates/core/fake_build_report.html` in full — its CSV parsing (`parseCSV`), numeric-column detection, chip palettes, chain-track builder, aggregate computation (`computeAggregate`), and CSV/PDF export logic (`exportCsvBtn`/`exportPdfBtn`) are the functional baseline `fake_build_report2.html` must match, and much of this logic can likely be reused/adapted as-is.
- Review `myportal/templates/base2.html`'s `settingsDropdownMenu` markup to confirm exactly how to add the third "Fake 2" link.
- Review `myportal/core/views.py`'s `building_settings_fake` and `building_settings_profile` for the view pattern (permission check, context variables) to follow for the new `building_settings_fake2` view.
- Review `myportal/core/urls.py`'s `# ── Settings ──` block to see where to add the new `fake2` route.
- Design the node/connection data model (node types: column, operator, bracket/group, function, aggregate; connections between them) and decide how a connected graph maps to an evaluable formula before writing `fake_build_report2.html`'s JS.

## Expected deliverables
1. New `myportal/templates/core/fake_build_report2.html` implementing a working node-canvas + connection-line prototype with the same functional scope as `fake_build_report.html` (sample/fake data, no real save/persist logic required beyond in-memory state).
2. Updated `myportal/templates/base2.html` with a "Fake 2" link added to the Settings dropdown.
3. New `myportal/core/views.py` function `building_settings_fake2` (and corresponding URL in `core/urls.py`).
4. A documented decision on the node-positioning/connection-line implementation approach (vanilla JS + SVG vs. a library), including rationale.

## Acceptance criteria
- The Settings dropdown in `base2.html` gains a working "Fake 2" option (alongside "Profile" and "Fake"), with correct `active` state highlighting.
- Clicking "Fake 2" opens `fake_build_report2.html`, where a CSV can be uploaded, columns/operators/brackets/functions/aggregates can be dragged onto an open canvas as nodes, and nodes can be linked together with connection lines to form a formula.
- The resulting node-graph formula(s) can be evaluated per row and saved, with per-row answers shown and exportable to CSV and PDF, matching `fake_build_report.html`'s output capabilities.
- The existing `_user_can_access_object_client` permission check is enforced on the new `building_settings_fake2` view, consistent with other building-tab views.
- No regressions in any existing pages, including the existing `fake_build_report.html`, Vault, Insight, Energy, Reports, Charts, and Settings/Profile.
- `app.css` and all admin files are untouched (aside from any minor, additive, clearly-scoped CSS if genuinely unavoidable).
- `building_dashboard.html` and the Settings/Profile edit-save function are left unchanged in this round.
