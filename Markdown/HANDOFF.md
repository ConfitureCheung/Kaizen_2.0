# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, Vault, Insight, Energy & Report, and Charts/Systems/Settings sections.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) remain layout-only or sample-data driven and are **deferred** to a later stage.
The Groups, Users, Dashboard, left panel, Django admin, Vault, Insight, Energy & Report, and Charts/Systems sections are all **layout/route complete** — all eight building-tab icons in `base2.html` (Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings) point to real routes with `active` state highlighting; none are `href="#"` placeholders.

**Settings is now a working dropdown sub-nav** (`settingsDropdownWrap` / `settingsDropdownToggle` / `settingsDropdownMenu` in `base2.html`, registered with `initDropdown(...)`), matching the Vault/Insights pattern, with two live links:
- **"Profile"** → `building_settings_profile` / `core/settings_profile.html` — unchanged, still read-only, Edit button still non-functional. That edit/save work remains **deferred**.
- **"Fake"** → `building_settings_fake` / `core/fake_build_report.html` — **complete**. This is a standalone, sample-data-only drag-and-drop formula/report builder: a CSV is uploaded on the left, its columns become draggable "plates", and operator/bracket/function/aggregate chips are dragged into a **single horizontal chain track** (a "one-liner" — the formula is assembled left-to-right as a flat, alternating term/operator strip, including nested bracket groups) to build a formula that is evaluated per row, with results shown and exportable (CSV / print-to-PDF) in the right panel. No JS library or npm tooling was introduced — it's built with vanilla HTML5 drag-and-drop events (`dragstart`/`dragover`/`drop`) directly in the template's `extra_js` block, which fully resolved the earlier open question about CDN vs. npm-managed drag-and-drop tooling.

The **next active implementation stage is a second, parallel prototype**: `core/fake_build_report2.html`. It must satisfy **exactly the same functional requirements** as `fake_build_report.html` (CSV upload → column plates on the left; operator/grouping/function/aggregate chips; a way to assemble a formula from them; per-row answers + CSV/PDF export on the right) — but the **mid panel gets a different interaction model**. Instead of dragging chips/columns into a single-line chain track, the new version should let the user **drag items onto an open panel/canvas where they land as freestanding nodes, and then link nodes together by drawing connection lines between them** — i.e. a small node-graph / flow-diagram style formula builder, rather than a flat left-to-right strip. This is treated the same way `fake_build_report.html` was: an **isolated experiment**, reached via its own new entry in the existing Settings dropdown, not wired into real building/report data.
The `building_dashboard.html` content work (five empty placeholder cards) documented previously remains a separate, still-pending stage and has **not** been started.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups, Clients, and Users pages are fully functional (client-scoped where relevant).
- Account-level Profile page (`accounts/profile.html`) save flow, avatar upload, and Django admin visibility are implemented — this is the reference pattern to follow for any future settings_profile.html save flow.
- `dashboard.html` (app-level dashboard, not building-scoped) is fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- The sliding left panel in `base.html` is fully interactive.
- **Django admin is fully consistent with the frontend view**.
- **Vault section is complete**: `trend_logs.html` and `objects.html` are both live, reading data from the building-linked SQLite database via raw `sqlite3` connections. Vault is exposed via a **dropdown sub-nav** in `base2.html` (`vaultDropdownWrap` / `vaultDropdownToggle` / `vaultDropdownMenu`).
- **Insight section is complete (layout-first)**: all five pages (`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`) extend `base2.html`, using static/sample data and sub-navigation tabs, exposed via `insightsDropdownWrap`.
- **Energy & Report section is complete**: `energy.html` (`building_energy` view) and `report.html` (`building_reports` view), both extending `base2.html` and wired into the building-tab sub-nav.
- **Charts and Systems are complete (layout-first)**: `building_charts` renders `core/chart.html`, `building_systems` renders `core/systems.html`.
- **Settings/Profile page exists but is read-only**: `building_settings_profile` view (`/buildings/<pk>/settings/profile/`) resolves the building via `pk`, enforces `_user_can_access_object_client`, and renders `core/settings_profile.html` with `selected_building`/`selected_client`/`building_tab="settings"`, displaying all Building model fields as a static two-column table with a toolbar Edit button that has no behaviour yet. This edit/save work remains deferred (see below).
- **Settings dropdown is complete**: the plain Settings `<a>` link in `base2.html` was converted into a `dropdown-tab` (`settingsDropdownWrap`/`settingsDropdownToggle`/`settingsDropdownMenu`) exactly mirroring the Vault/Insights markup and `initDropdown(...)` JS, exposing "Profile" and "Fake".
- **`core/fake_build_report.html` is complete**: reached via `building_settings_fake` (`/buildings/<pk>/settings/fake/`, same permission-check pattern as the other building-tab views). Left panel: CSV upload + numeric/text column detection + draggable column "plates". Mid panel: chip palettes for operators (`+ − × ÷ ^ %`), grouping (bracket), functions (`ABS`/`ROUND`/`SQRT`), and aggregates (`SUM`/`AVG`/`MIN`/`MAX`/`COUNT`), all dragged into a single **chain track** that enforces strict term/operator alternation, supports nested bracket groups, and lets functions wrap a column/aggregate/group by dropping onto it. Formulas can be named (auto-generated from the chain display), saved, and removed. Right panel: per-row computed answers for every saved formula, plus CSV export and print-to-PDF export (via a hidden print-only table and `window.print()`). All logic is vanilla JS in the template's `extra_js` block — no drag-and-drop library, no npm/build step was needed.

## What is not yet done — current target
**`core/fake_build_report2.html` — a node/graph-based variant of the formula builder.** This is now the active target, and it is intentionally treated the same way `fake_build_report.html` was: an independent, sample-data-only trial, decoupled from the deferred Settings/Profile edit-save work.

1. **Functional parity with `fake_build_report.html`**: same left panel (CSV upload, column detection, draggable plates), same categories of draggable primitives in the mid panel (operators, grouping, functions, aggregates), same overall goal (build one or more formulas, evaluate them per row, list saved formulas, show per-row answers, export to CSV/PDF) — reusing the existing CSV parsing, aggregate computation, and export logic where possible rather than rewriting it from scratch.
2. **New mid-panel interaction model — canvas + connection lines**: instead of the existing horizontal chain track, the mid panel becomes an open drop area (a "panel"/canvas) onto which columns, operators, brackets, functions, and aggregates are dragged and dropped as **freestanding, freely positioned nodes** (not constrained to a single line). The user then **draws a connection line from one node to another** to indicate how they combine (e.g. connect a column node to an operator node, and that operator node to a second column node, to express `ColA + ColB`). Removing a node or a connection should update the resulting formula/graph accordingly.
3. **Open implementation questions to settle before/while building this**:
   - How nodes are positioned/dragged on the canvas: absolute-positioned `div`s moved via `mousedown`/`mousemove`/`mouseup` (or native HTML5 drag events) is the natural continuation of the vanilla-JS approach already used in `fake_build_report.html`.
   - How connection lines are drawn and kept in sync with node positions: the simplest option is an `<svg>` overlay sized to the canvas, with a `<line>` or `<path>` element per connection whose endpoints are recalculated whenever either connected node moves. A small drag-from-anchor-point interaction (e.g. a connector "dot" on each node) is the usual pattern for starting/ending a connection.
   - Whether a small graph/diagram library (e.g. jsPlumb, LeaderLine, Plain Draggable + custom SVG) is worth adding via CDN, or whether hand-rolled SVG + vanilla JS positioning (consistent with the no-library choice made for `fake_build_report.html`) is sufficient — default assumption is to **stay library-free unless the connection-line math becomes unwieldy**, to keep this project Node/npm-free.
   - How a connected node graph maps back to an evaluable formula/expression (e.g. requiring a single connected chain with no branching for v1, versus supporting simple tree-shaped graphs where a node can have multiple incoming connections).

## Important implementation notes
- Treat `fake_build_report2.html` as an **independent trial task**, just like `fake_build_report.html` was — do not entangle it with the Settings/Profile edit-save plan, and do not assume its patterns must be reused elsewhere yet.
- Reuse rather than duplicate logic where it makes sense: CSV parsing (`parseCSV`), numeric-column detection, aggregate computation (`computeAggregate`), and the CSV/PDF export pattern from `fake_build_report.html` are good candidates to copy/adapt rather than reinvent.
- Follow the existing dropdown pattern exactly if/when a new "Fake 2" entry is added to the Settings dropdown (`building-tab dropdown-tab`, `building-tab-button`, `building-tab-dropdown`, `building-tab-dropdown-link` classes, plus `initDropdown(wrapId, toggleId, menuId)`), so it behaves identically to the existing Profile/Fake links.
- Keep `fake_build_report2.html` clearly labelled/scoped as a prototype (sample/fake data only), same as `fake_build_report.html`.
- `building_dashboard.html` (five placeholder cards) remains a **separate, still-pending** stage — do not work on it in this round.
- The Settings/Profile edit-save function remains **deferred** and is not part of this round.

## Relevant files for the next session
- `myportal/templates/base2.html` — add a third link ("Fake 2") to the existing `settingsDropdownMenu`, alongside "Profile" and "Fake".
- `myportal/templates/core/fake_build_report2.html` — **new file**, the node/graph-based report-builder prototype page.
- `myportal/core/views.py` — add a new `building_settings_fake2` view, following the exact pattern of `building_settings_fake` / `building_settings_profile` (permission check via `_user_can_access_object_client`, `selected_building`/`selected_client`/`building_tab="settings"` context).
- `myportal/core/urls.py` — add a new URL pattern under the `# ── Settings ──` section, e.g. `buildings/<int:pk>/settings/fake2/` → `building_settings_fake2`.
- `myportal/templates/core/fake_build_report.html` — reference implementation for CSV parsing, column plates, chip palettes, aggregate computation, and CSV/PDF export logic to reuse/adapt.
- `Markdown/HANDOFF.md`, `Markdown/PROJECT_OVERVIEW.md`, `Markdown/TASK.md` — keep in sync as this new prototype task evolves.

## Next task
Build **`core/fake_build_report2.html`** as a second, standalone formula/report-builder prototype with the same functional scope as `fake_build_report.html`, but with a **node-canvas + connection-line mid panel** instead of a single-line chain track.

This next step should include:
- Reviewing `fake_build_report.html` in full (left panel CSV/column logic, chip palettes, aggregate/expression evaluation, right panel answers/export) to confirm exactly what functional parity means.
- Designing the canvas/node data model (node types: column, operator, bracket/group, function, aggregate; connections between nodes) and how it maps to an evaluable expression.
- Implementing draggable nodes on an open canvas panel and an SVG (or similar) overlay for connection lines that stay in sync as nodes move.
- Adding the `building_settings_fake2` view/URL and a "Fake 2" link in the Settings dropdown, following the existing Profile/Fake pattern.
- Reusing the CSV upload/parsing, aggregate computation, and CSV/PDF export logic from `fake_build_report.html` wherever practical.

## Constraints for the next edit
- Focus only on: `fake_build_report2.html`, its optional view/URL/nav wiring, and whatever minimal JS the node-canvas + connection-line interaction needs.
- Do **not** implement the Settings/Profile edit-save function in this round — that work is deferred.
- Do not start work on `building_dashboard.html` in this round.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Users, app-level Dashboard, Vault, Insight, Energy, Reports, Charts, Systems, Left panel, Admin) or modify the existing, working `fake_build_report.html`.
- Do not modify `static/css/app.css`/`app2.css` structurally (small scoped styles for the new canvas/nodes/connection lines are acceptable if unavoidable) or any admin files.
- Default to staying library-free (vanilla JS + SVG) unless the connection-line/node-graph interaction genuinely requires a library — document the decision either way.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build core/fake_build_report2.html, a second standalone
drag-and-drop formula/report-builder prototype, reached via a new "Fake 2"
option in the existing Settings dropdown in base2.html (alongside "Profile"
and "Fake").

It must have the same functional scope as the existing
core/fake_build_report.html: CSV upload with draggable column plates on the
left, chip palettes for operators (+ - * / ^ %), grouping (brackets),
functions (ABS/ROUND/SQRT), and aggregates (SUM/AVG/MIN/MAX/COUNT), the
ability to build and save one or more formulas evaluated per row, and a
right panel showing per-row answers with CSV and PDF export.

The difference is the mid panel: instead of dragging chips/columns into a
single horizontal chain track (a "one-liner"), this version should let the
user drag items onto an open canvas/panel where they land as freestanding
nodes, then draw connection lines between nodes to link them together into
a formula (a small node-graph / flow-diagram style builder).

Constraints:
- reuse the CSV parsing, numeric-column detection, aggregate computation,
  and CSV/PDF export logic from core/fake_build_report.html rather than
  rewriting it from scratch
- add a new building_settings_fake2 view in core/views.py following the
  same permission-check pattern as building_settings_fake /
  building_settings_profile
- add a new URL (e.g. buildings/<int:pk>/settings/fake2/) in core/urls.py
- add a "Fake 2" link to the existing settingsDropdownMenu in base2.html
- this is an independent trial task — do not touch fake_build_report.html,
  settings_profile.html, or the deferred Settings/Profile edit-save work
- do not touch building_dashboard.html in this round
- default to vanilla JS + an SVG overlay for the node canvas and connection
  lines; only introduce a library (e.g. jsPlumb, LeaderLine) if hand-rolled
  SVG positioning proves genuinely unworkable, and document the choice
- no modifications to app.css structurally, admin files, or already-
  completed views
Reference:
- templates/core/fake_build_report.html for the CSV/column/chip/aggregate/
  export logic to reuse
- templates/base2.html for the existing settingsDropdownWrap/
  settingsDropdownToggle/settingsDropdownMenu pattern to extend
- core/views.py's building_settings_fake / building_settings_profile for
  the view pattern to follow
- core/urls.py's "# ── Settings ──" block for where to add the new route
Please return complete updated files only.
```
