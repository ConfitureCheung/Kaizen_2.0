# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Profile page functional work (save, avatar upload, admin visibility) has been completed and is no longer the active focus.
The next implementation stage is the functional part of the **Client-related pages**: `clients.html`, `client_detail.html`, and `client_saved.html`.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Users pages are functional with `users.html` and `user_detail.html`.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Buildings pages are laid out with list/detail/report screens.
- Groups area is implemented as a list/detail/member-selection style flow.
- Clients pages are already laid out with `clients.html`, `client_detail.html`, and `client_saved.html` — but they are currently **layout-only or sample-data driven**.
- The sliding left panel is already in `base.html`, showing the Client → Building hierarchy from queryset-backed context.

## What is not yet done — current target
The three Client-related pages need real backend functionality:

- **`clients.html`** — should list all `Client` records from the database owned by or accessible to the logged-in user. Currently renders with static or placeholder data.
- **`client_detail.html`** — should display a single client's full details, including its associated buildings and groups, pulled from real querysets.
- **`client_saved.html`** — should handle both the **create** and **edit** flows for a `Client` record, saving form data to the database and redirecting correctly on success.

## Important implementation notes
- Reuse the existing `Client` model in `core/models.py`; do not redesign the data model unless a small nullable field addition is strictly necessary.
- Keep all view logic inside `core/views.py` following the existing `allowed_clients` and queryset-backed patterns already present.
- Keep styling inside `static/css/app.css` conventions; reuse existing card, form, table, and button patterns.
- Keep any interactivity inside `static/js/app.js`; do not introduce page-specific scripts unless unavoidable.
- The left panel in `base.html` already renders clients and buildings from context — any new client save/delete action should keep that context consistent.
- Preserve the current project structure, naming style, and minimal-change workflow.

## Relevant files for the next session
- `templates/core/clients.html`
- `templates/core/client_detail.html`
- `templates/core/client_saved.html`
- `core/views.py` — add or update `clients_view`, `client_detail_view`, `client_saved_view`
- `core/urls.py` — verify routes for `clients`, `client_detail`, `client_saved`
- `core/models.py` — reference `Client` model definition
- `static/css/app.css` — reuse existing patterns; add only what is missing
- `static/js/app.js` — add any client-specific interactivity here

## Next task
Work on the functional part of the **Client pages**: `clients.html`, `client_detail.html`, and `client_saved.html`.

This next step should include:
- Listing all accessible `Client` records in `clients.html` with real queryset data.
- Displaying a single client's full details (name, buildings, groups) in `client_detail.html`.
- Implementing create and edit form handling in `client_saved.html` with proper POST save, validation feedback, and redirect on success.
- Wiring Django admin visibility for `Client` records if not already registered.
- Keeping the left panel context consistent after any create/edit action.

## Constraints for the next edit
- Focus on Client functionality only.
- Do not refactor unrelated modules (Users, Groups, Buildings, Profile).
- Preserve the shared `base.html` shell and left-panel behavior.
- Keep CSS in `static/css/app.css` and shared interaction logic in `static/js/app.js`.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the functional part of the Client pages (clients.html, client_detail.html, client_saved.html).
Constraints:
- keep current Django structure
- keep existing bulky style
- no unrelated refactor
- preserve existing shared base.html shell and left panel
- only touch Client-related files unless a small shared CSS/JS/admin/model update is required
Relevant files:
- templates/core/clients.html
- templates/core/client_detail.html
- templates/core/client_saved.html
- core/views.py
- core/urls.py
- core/models.py
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
