# TASK

## Current task
Review and update the functional part of the Users HTML pages: `users.html` and `user_detail.html`.

## Immediate objective
Ensure both Users-related screens are consistent with the shared BLENDY visual language, and wire real backend functionality into any screen that is still layout-only or not fully connected to live queryset data.

This should include:
- Queryset-backed user list in `users.html`, showing full name, email, work phone, group badges, and action buttons (edit, activate/deactivate).
- Real user detail data in `user_detail.html` with working create and edit form handling (POST save, group assignment, active status toggle, validation feedback, redirect on success).
- Django admin registration for the custom user model if not already present.

## Background from the previous step
The project already uses a shared authenticated shell in `templates/base.html`, including a sliding left panel that renders a Client → Building tree from queryset-backed context.
The Groups pages functional work — queryset-backed list, detail view, create/edit form handling, member selection, and permission wiring — has been completed and can be used as a reference pattern.
The CSS classes for common patterns (cards, tables, forms, banners, save buttons, action columns) are already defined in `static/css/app.css`.
The Users template files and their URL routes already exist; the focus is reviewing, completing, and wiring them.

## Scope for the next coding round

**In scope:**
- `templates/core/users.html`
- `templates/core/user_detail.html`
- `core/views.py` — add or update `users_view`, `user_detail_view`
- `core/urls.py` — verify or update routes for `users`, `user_detail`
- `accounts/models.py` — reference only; add a small nullable field only if strictly necessary
- `core/admin.py` — register custom user model if not already done
- Small related updates to `static/css/app.css` and `static/js/app.js` only if required to support form behavior or list interactivity

**Out of scope for this round:**
- Refactoring unrelated modules (Groups, Buildings, Clients, Profile).
- Replacing or redesigning the shared `base.html` shell or left panel.
- Broad user permission system changes beyond group assignment.
- Redesigning the user data model.
- Unrelated styling cleanup.

## Starting point
- `users_view` and `user_detail_view` may already exist in `core/views.py` in a stub or layout-rendering form — confirm before writing from scratch.
- The project already has established CSS patterns for forms, cards, tables, banners, save buttons, and action columns that should be reused rather than replaced.
- The left panel in `base.html` depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by every authenticated view’s context.

## Expected deliverables
1. `users.html` renders a real queryset-backed list of user records with full name, email, work phone, group badges, and edit/status-toggle actions.
2. `user_detail.html` handles both create and edit flows: GET renders the form with current field values and group assignment, POST validates and saves, success redirects appropriately.
3. Django admin shows custom user records.
4. No unrelated architecture refactor.

## Acceptance criteria
- A new user can be created through `user_detail.html` and appears immediately in the `users.html` list.
- An existing user can be edited through the same form and changes are persisted.
- Group assignment on a user is reflected in the group’s member list.
- Saved user data is visible in the Django admin panel.
- The implementation fits the existing BLENDY visual language and shared shell structure.
- Changes remain targeted and do not disturb unrelated modules.
