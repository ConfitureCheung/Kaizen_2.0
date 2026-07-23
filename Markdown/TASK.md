# TASK

## Current task
Build the functional part of the Client pages: `clients.html`, `client_detail.html`, and `client_saved.html`.

## Immediate objective
Wire real backend functionality into the three Client-related screens that are currently layout-only or sample-data driven.

This should include:
- Queryset-backed client list in `clients.html`.
- Real client detail data (including buildings and groups) in `client_detail.html`.
- Working create and edit form handling in `client_saved.html` with POST save, validation feedback, and redirect on success.
- Django admin registration for `Client` records if not already present.
- Left panel context kept consistent after any Client create/edit action.

## Background from the previous step
The project already uses a shared authenticated shell in `templates/base.html`, including a sliding left panel that renders a Client → Building tree from queryset-backed context.
The Profile page functional work — save, avatar upload, admin visibility — has been completed.
The Client model and its relationships to `Building` and `ClientGroup` already exist in `core/models.py`.
The three Client template files and their URL routes already exist; only the view logic and template data-binding need to be made functional.

## Scope for the next coding round

**In scope:**
- `templates/core/clients.html`
- `templates/core/client_detail.html`
- `templates/core/client_saved.html`
- `core/views.py` — add or update `clients_view`, `client_detail_view`, `client_saved_view`
- `core/urls.py` — verify or update routes for `clients`, `client_detail`, `client_saved`
- `core/models.py` — reference only; add a small nullable field only if strictly necessary
- `core/admin.py` — register `Client` if not already done
- Small related updates to `static/css/app.css` and `static/js/app.js` only if required to support form behavior or list interactivity

**Out of scope for this round:**
- Refactoring unrelated modules (Users, Groups, Buildings, Profile).
- Replacing or redesigning the shared `base.html` shell or left panel.
- Broad permission-system changes.
- Redesigning the `Client` data model.
- Unrelated styling cleanup.

## Starting point
- `clients_view`, `client_detail_view`, and `client_saved_view` may already exist in `core/views.py` in a stub or layout-rendering form — confirm before writing from scratch.
- The project already has established CSS patterns for forms, cards, tables, save buttons, and validation banners that should be reused rather than replaced.
- The left panel in `base.html` already depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by the view context or a shared context processor.

## Expected deliverables
1. `clients.html` renders a real queryset-backed list of `Client` records.
2. `client_detail.html` renders a single client's full details with prefetched buildings and groups.
3. `client_saved.html` handles both create and edit flows: GET renders form, POST validates and saves, success redirects to `client_detail`.
4. Django admin shows `Client` records.
5. Left panel stays consistent after any client write action.
6. No unrelated architecture refactor.

## Acceptance criteria
- A new `Client` record can be created through the `client_saved.html` form and appears immediately in the `clients.html` list.
- An existing `Client` record can be edited through the same form and changes are persisted.
- `client_detail.html` correctly shows the client's buildings and groups from the database.
- Saved client data is visible in the Django admin panel.
- The implementation fits the existing BLENDY visual language and shared shell structure.
- Changes remain targeted and do not disturb unrelated modules.
