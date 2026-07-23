# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Client pages functional work (`clients.html`, `client_detail.html`, `client_saved.html`) has been completed and is no longer the active focus.
The next implementation stage is the functional part of the **Buildings-related pages**: `buildings.html`, `building_detail.html`, and `building_report.html`.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Users pages are functional with `users.html` and `user_detail.html`.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Groups area is implemented as a list/detail/member-selection style flow.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail.html` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows with POST save and redirect on success.
- The sliding left panel in `base.html` renders the Client → Building hierarchy from queryset-backed context and remains consistent after Client write actions.
- Buildings pages are laid out with list/detail/report screens — but they are currently **layout-only or sample-data driven**.

## What is not yet done — current target
The three Buildings-related pages need real backend functionality:

- **`buildings.html`** — should list all `Building` records accessible to the logged-in user, grouped or filtered by `Client`. Currently renders with static or placeholder data.
- **`building_detail.html`** — should display a single building's full details (name, address, client, floors, sensors, etc.) pulled from real querysets, and handle both create and edit flows via POST.
- **`building_report.html`** — should display a reporting view for a single building, including charts/stats pulled from real queryset data (e.g. energy readings, sensor summaries, or similar time-series data tied to the building).

## Important implementation notes
- Reuse the existing `Building` model in `core/models.py`; do not redesign the data model unless a small nullable field addition is strictly necessary.
- Keep all view logic inside `core/views.py` following the existing `allowed_clients` and queryset-backed patterns already present.
- Keep styling inside `static/css/app.css` conventions; reuse existing card, form, table, and button patterns.
- Keep any interactivity inside `static/js/app.js`; do not introduce page-specific scripts unless unavoidable.
- The left panel in `base.html` already renders clients and buildings from context — any new building save/delete action should keep that context consistent.
- Preserve the current project structure, naming style, and minimal-change workflow.

## Relevant files for the next session
- `templates/core/buildings.html`
- `templates/core/building_detail.html`
- `templates/core/building_report.html`
- `core/views.py` — add or update `buildings_view`, `building_detail_view`, `building_report_view`
- `core/urls.py` — verify routes for `buildings`, `building_detail`, `building_report`
- `core/models.py` — reference `Building` model definition
- `static/css/app.css` — reuse existing patterns; add only what is missing
- `static/js/app.js` — add any building-specific interactivity here

## Next task
Work on the functional part of the **Buildings pages**: `buildings.html`, `building_detail.html`, and `building_report.html`.

This next step should include:
- Listing all accessible `Building` records in `buildings.html` with real queryset data, filtered/grouped by client.
- Displaying a single building's full details in `building_detail.html` with working create and edit form handling (POST save, validation feedback, redirect on success).
- Rendering a real data-backed report in `building_report.html` with charts or stats tied to the building's sensor or energy data.
- Wiring Django admin visibility for `Building` records if not already registered.
- Keeping the left panel context consistent after any create/edit/delete action.

## Constraints for the next edit
- Focus on Buildings functionality only.
- Do not refactor unrelated modules (Users, Groups, Clients, Profile).
- Preserve the shared `base.html` shell and left-panel behavior.
- Keep CSS in `static/css/app.css` and shared interaction logic in `static/js/app.js`.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the functional part of the Buildings pages (buildings.html, building_detail.html, building_report.html).
Constraints:
- keep current Django structure
- keep existing bulky style
- no unrelated refactor
- preserve existing shared base.html shell and left panel
- only touch Buildings-related files unless a small shared CSS/JS/admin/model update is required
Relevant files:
- templates/core/buildings.html
- templates/core/building_detail.html
- templates/core/building_report.html
- core/views.py
- core/urls.py
- core/models.py
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
