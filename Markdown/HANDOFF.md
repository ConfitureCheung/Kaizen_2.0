# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) are still layout-only or sample-data driven and are **deferred** to a later stage.
The Groups pages (`groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html`) are **complete** — all four screens are queryset-backed, wired to real backend logic, and consistent with the shared BLENDY visual language.
The Users pages (`users.html`, `user_detail.html`) are now **complete** — both screens are queryset-backed, wired to real backend logic (create, edit, group assignment, activate/deactivate), and consistent with the shared visual language.
The next active implementation stage is the **functional review and update of `dashboard.html`**.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional: `groups.html` is queryset-backed, `group_detail.html` handles create and edit flows with POST save and permission wiring, `group_saved.html` shows the confirmation screen with real group context, and `group_members.html` handles membership updates.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail.html` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows with POST save and redirect on success.
- The sliding left panel in `base.html` renders the Client → Building hierarchy from queryset-backed context and remains consistent after write actions.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.
- Users pages are fully functional: `users.html` is queryset-backed showing full name, email, work phone, group badges, and action buttons; `user_detail.html` handles both create and edit flows with POST save, validation feedback, group assignment, and activate/deactivate toggling. Django admin registration for the custom user model is in place.

## What is not yet done — current target
`dashboard.html` needs a full functional review and update. The page currently exists as a partial layout or sample-data screen and needs to be connected to real queryset-backed data and live summary logic.

Planned functional behaviour for the dashboard includes:
- **Summary KPI cards** — total counts for active users, clients, buildings, and groups pulled from live querysets.
- **Recent activity feed** — a short list of the most recently created or updated records across key models.
- **Client → Building overview** — a summary table or card list showing clients with their building counts, consistent with the left panel hierarchy.
- **Insight/alert strip** — surface any flagged conditions (e.g. users with no group, buildings with no client assignment) as actionable inline notices.
- **Charts (if applicable)** — data visualisations such as insight counts by building or user activity trends, using the existing chart library already referenced in the project.

## Important implementation notes
- Reuse the existing custom user model in `accounts/models.py`; do not redesign the data model.
- Keep all view logic inside `core/views.py` following the existing `allowed_clients` and queryset-backed patterns already present.
- Keep styling inside `static/css/app.css` conventions; reuse existing card, form, table, and button patterns already defined.
- Keep any interactivity inside `static/js/app.js`; do not introduce page-specific scripts unless unavoidable.
- Preserve the current project structure, naming style, and minimal-change workflow.
- The left panel in `base.html` depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by every authenticated view's context.

## Relevant files for the next session
- `templates/core/dashboard.html`
- `core/views.py` — update `dashboard_view` to supply real queryset context
- `core/urls.py` — verify route for `dashboard`
- `static/css/app.css` — add only what is missing for dashboard-specific layout
- `static/js/app.js` — add chart initialisation or dashboard interactivity if needed

## Next task
Work on the **functional aspect of `dashboard.html`**.

This next step should include:
- Reviewing the current `dashboard.html` layout and identifying which sections are still sample-data or placeholder.
- Updating `dashboard_view` in `core/views.py` to supply real queryset-backed counts, recent records, and any other data the template needs.
- Replacing all sample/placeholder data in `dashboard.html` with live template variables.
- Adding any missing CSS classes to `static/css/app.css` for dashboard-specific widgets (KPI cards, activity feed rows, alert strip).
- Wiring any chart instances to real data passed from the view context.

## Constraints for the next edit
- Focus on `dashboard.html` functionality only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users).
- Preserve the shared `base.html` shell and left-panel behaviour.
- Keep CSS in `static/css/app.css` and shared interaction logic in `static/js/app.js`.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: update and wire the functional part of dashboard.html.
Constraints:
- keep current Django structure
- keep existing bulk style
- no unrelated refactor
- preserve existing shared base.html shell and left panel
- only touch dashboard-related files unless a small shared CSS/JS/admin/model update is required
Relevant files:
- templates/core/dashboard.html
- core/views.py
- core/urls.py
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
