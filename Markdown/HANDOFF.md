# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) are still layout-only or sample-data driven and are **deferred** to a later stage.
The next active implementation stage is the functional part of the **Groups-related HTML pages**: `groups.html`, `group_detail.html`, `group_saved.html`, and `group_members.html`.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Users pages are functional with `users.html` and `user_detail.html`.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail.html` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows with POST save and redirect on success.
- The sliding left panel in `base.html` renders the Client → Building hierarchy from queryset-backed context and remains consistent after Client write actions.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.

## What is not yet done — current target
The four Groups-related HTML pages need review and updates to ensure they are consistent, complete, and ready to wire to backend logic:

- **`groups.html`** — list view of all groups, should show group name, member count, and permissions summary. Currently may be layout-only or partially functional.
- **`group_detail.html`** — detail/edit form for a single group, including group name, global permissions flags, and per-page permission rows. Should handle both create (no `pk`) and edit (with `pk`) flows.
- **`group_saved.html`** — confirmation/summary screen after a group is saved, showing group name and a summary of assigned permissions.
- **`group_members.html`** — member selection screen for a group, showing a list of available users with checkboxes to add or remove them from the group.

## Important implementation notes
- Reuse the existing `Group` (or custom group) model in `core/models.py`; do not redesign the data model unless a small nullable field addition is strictly necessary.
- Keep all view logic inside `core/views.py` following the existing `allowed_clients` and queryset-backed patterns already present.
- Keep styling inside `static/css/app.css` conventions; reuse existing card, form, table, and button patterns (`.groups-page`, `.group-form`, `.group-perms-table`, `.group-perms-row` etc. are already defined).
- Keep any interactivity inside `static/js/app.js`; do not introduce page-specific scripts unless unavoidable.
- Preserve the current project structure, naming style, and minimal-change workflow.

## Relevant files for the next session
- `templates/core/groups.html`
- `templates/core/group_detail.html`
- `templates/core/group_saved.html`
- `templates/core/group_members.html`
- `core/views.py` — add or update `groups_view`, `group_detail_view`, `group_saved_view`, `group_members_view`
- `core/urls.py` — verify routes for `groups`, `group_detail`, `group_saved`, `group_members`
- `core/models.py` — reference existing group/permission model definitions
- `static/css/app.css` — reuse existing patterns; add only what is missing
- `static/js/app.js` — add any group-specific interactivity here

## Next task
Work on the **Groups HTML pages**: `groups.html`, `group_detail.html`, `group_saved.html`, and `group_members.html`.

This next step should include:
- Reviewing and updating the four Groups templates so they are consistent with the shared visual language and shell.
- Ensuring `groups.html` lists all group records with name, member count, and action buttons.
- Ensuring `group_detail.html` handles both create and edit flows: GET renders the form, POST validates and saves, success redirects to `group_saved`.
- Ensuring `group_saved.html` shows a success banner, the group's summary info, and a link back to the group list.
- Ensuring `group_members.html` shows a user-selection table with checkboxes and a save action.
- Wiring any missing Django admin visibility for group-related models.
- Keeping the left panel context consistent after any group write action.

## Constraints for the next edit
- Focus on Groups HTML functionality only.
- Do not refactor unrelated modules (Users, Buildings, Clients, Profile).
- Preserve the shared `base.html` shell and left-panel behavior.
- Keep CSS in `static/css/app.css` and shared interaction logic in `static/js/app.js`.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: update and wire the functional part of the Groups pages (groups.html, group_detail.html, group_saved.html, group_members.html).
Constraints:
- keep current Django structure
- keep existing bulk style
- no unrelated refactor
- preserve existing shared base.html shell and left panel
- only touch Groups-related files unless a small shared CSS/JS/admin/model update is required
Relevant files:
- templates/core/groups.html
- templates/core/group_detail.html
- templates/core/group_saved.html
- templates/core/group_members.html
- core/views.py
- core/urls.py
- core/models.py
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
