# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) are still layout-only or sample-data driven and are **deferred** to a later stage.
The Groups pages (`groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html`) are now **complete** — all four screens are queryset-backed, wired to real backend logic, and consistent with the shared BLENDY visual language.
The next active implementation stage is the functional review and update of the **Users-related HTML pages**: `users.html` and `user_detail.html`.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional: `groups.html` is queryset-backed, `group_detail.html` handles create and edit flows with POST save and permission wiring, `group_saved.html` shows the confirmation screen with real group context, and `group_members.html` handles membership updates.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail.html` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows with POST save and redirect on success.
- The sliding left panel in `base.html` renders the Client → Building hierarchy from queryset-backed context and remains consistent after write actions.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.

## What is not yet done — current target
The two Users-related HTML pages need review and updates to ensure they are consistent, complete, and ready (or already wired) to backend logic:

- **`users.html`** — list view of all user accounts, should show full name, email, work phone, group membership, and action buttons (edit, deactivate/activate). May already be partially functional but needs review for consistency and completeness.
- **`user_detail.html`** — detail/edit form for a single user, including profile fields, group assignment, and active status toggle. Should handle both create (no `pk`) and edit (with `pk`) flows.

## Important implementation notes
- Reuse the existing custom user model in `accounts/models.py`; do not redesign the data model unless a small nullable field addition is strictly necessary.
- Keep all view logic inside `core/views.py` following the existing `allowed_clients` and queryset-backed patterns already present.
- Keep styling inside `static/css/app.css` conventions; reuse existing card, form, table, and button patterns already defined.
- Keep any interactivity inside `static/js/app.js`; do not introduce page-specific scripts unless unavoidable.
- Preserve the current project structure, naming style, and minimal-change workflow.
- The left panel in `base.html` depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by every authenticated view's context.

## Relevant files for the next session
- `templates/core/users.html`
- `templates/core/user_detail.html`
- `core/views.py` — add or update `users_view`, `user_detail_view`
- `core/urls.py` — verify routes for `users`, `user_detail`
- `accounts/models.py` — reference existing user model definitions
- `static/css/app.css` — reuse existing patterns; add only what is missing
- `static/js/app.js` — add any user-specific interactivity here

## Next task
Work on the **Users HTML pages**: `users.html` and `user_detail.html`.

This next step should include:
- Reviewing and updating the two Users templates so they are consistent with the shared visual language and shell.
- Ensuring `users.html` lists all user records with full name, email, phone, group badges, and action buttons.
- Ensuring `user_detail.html` handles both create and edit flows: GET renders the form, POST validates and saves, success redirects appropriately.
- Wiring any missing Django admin visibility for user-related models.
- Keeping the left panel context consistent after any user write action.

## Constraints for the next edit
- Focus on Users HTML functionality only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile).
- Preserve the shared `base.html` shell and left-panel behavior.
- Keep CSS in `static/css/app.css` and shared interaction logic in `static/js/app.js`.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: update and wire the functional part of the Users pages (users.html, user_detail.html).
Constraints:
- keep current Django structure
- keep existing bulk style
- no unrelated refactor
- preserve existing shared base.html shell and left panel
- only touch Users-related files unless a small shared CSS/JS/admin/model update is required
Relevant files:
- templates/core/users.html
- templates/core/user_detail.html
- core/views.py
- core/urls.py
- accounts/models.py
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
