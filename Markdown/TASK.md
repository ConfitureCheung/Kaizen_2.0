# TASK

## Current task
Update and wire the functional part of the Groups HTML pages: `groups.html`, `group_detail.html`, `group_saved.html`, and `group_members.html`.

## Immediate objective
Ensure all four Groups-related screens are consistent with the shared BLENDY visual language, and wire real backend functionality into any screen that is still layout-only or not fully connected to live queryset data.

This should include:
- Queryset-backed group list in `groups.html`, showing group name, member count, and action buttons.
- Real group detail data in `group_detail.html` with working create and edit form handling (POST save, permission flag saving, validation feedback, redirect to `group_saved` on success).
- Working confirmation screen in `group_saved.html` rendering real group context (name, permission summary, current members).
- Working member-selection screen in `group_members.html` with user checkboxes pre-filled from current membership and a POST action to update membership.
- Django admin registration for group-related models if not already present.

## Background from the previous step
The project already uses a shared authenticated shell in `templates/base.html`, including a sliding left panel that renders a Client → Building tree from queryset-backed context.
The Client pages functional work — queryset-backed list, detail view, and create/edit form handling — has been completed and can be used as a reference pattern.
The CSS classes for groups pages (`.groups-page`, `.groups-table`, `.group-form`, `.group-perms-table`, `.group-perms-row`, `.group-global-perms`, `.group-members-page`, etc.) are already defined in `static/css/app.css`.
The Groups template files and their URL routes already exist; the focus is reviewing, completing, and wiring them.

## Scope for the next coding round

**In scope:**
- `templates/core/groups.html`
- `templates/core/group_detail.html`
- `templates/core/group_saved.html`
- `templates/core/group_members.html`
- `core/views.py` — add or update `groups_view`, `group_detail_view`, `group_saved_view`, `group_members_view`
- `core/urls.py` — verify or update routes for `groups`, `group_detail`, `group_saved`, `group_members`
- `core/models.py` — reference only; add a small nullable field only if strictly necessary
- `core/admin.py` — register group model if not already done
- Small related updates to `static/css/app.css` and `static/js/app.js` only if required to support form behavior or list interactivity

**Out of scope for this round:**
- Refactoring unrelated modules (Users, Buildings, Clients, Profile).
- Replacing or redesigning the shared `base.html` shell or left panel.
- Broad permission-system changes beyond what is already modelled.
- Redesigning the group or permission data model.
- Unrelated styling cleanup.

## Starting point
- `groups_view`, `group_detail_view`, `group_saved_view`, and `group_members_view` may already exist in `core/views.py` in a stub or layout-rendering form — confirm before writing from scratch.
- The project already has established CSS patterns for forms, cards, tables, banners, save buttons, and action columns that should be reused rather than replaced.
- The left panel in `base.html` depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by every authenticated view's context.

## Expected deliverables
1. `groups.html` renders a real queryset-backed list of `Group` records with name, member count, and edit/delete actions.
2. `group_detail.html` handles both create and edit flows: GET renders the form with global permission flags and per-page permission rows, POST validates and saves, success redirects to `group_saved`.
3. `group_saved.html` renders the saved group’s name, permission summary, and current members list with a success banner.
4. `group_members.html` renders all users as a checkbox table pre-filled from current membership, and handles POST to update group membership.
5. Django admin shows group records.
6. No unrelated architecture refactor.

## Acceptance criteria
- A new `Group` can be created through `group_detail.html` and appears immediately in the `groups.html` list.
- An existing `Group` can be edited through the same form and changes are persisted.
- `group_saved.html` correctly shows the group’s data from the database.
- `group_members.html` correctly updates group membership on POST.
- Saved group data is visible in the Django admin panel.
- The implementation fits the existing BLENDY visual language and shared shell structure.
- Changes remain targeted and do not disturb unrelated modules.
