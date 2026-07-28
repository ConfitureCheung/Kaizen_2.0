# TASK

## Current task
Implement **client-scoped group pages** so that groups belong to a specific client and are not accessible or visible to users operating under a different client.

## Immediate objective
Enforce a strict client-ownership boundary on the Group model and all related views, so that:
- A group is always associated with exactly one client (via a `ForeignKey` to `Client`).
- The groups list page only shows groups belonging to the currently active client context.
- Group detail, edit, and member management pages reject requests from users whose active client does not own that group (return 403 or redirect).
- Navigation (left panel tree and any group links) only surfaces groups under the correct client.

## Background from the previous step
The sliding left panel interactive function is now complete:
- Smooth CSS `transform: translateX()` open/close animation via the hamburger button.
- Overlay backdrop with click-to-close behaviour.
- Keyboard dismissal (`Escape` key).
- Tree expand/collapse for the Client → Building hierarchy inside the panel.
- Active state highlighting for the currently visited page item.

All CSS changes lived in `static/css/app.css` and all JS logic in `static/js/app.js`. The panel HTML structure and context dependencies in `base.html` were not changed.

## Scope for the next coding round

**In scope:**
- `myportal/core/models.py` — add a `client = ForeignKey(Client, on_delete=models.CASCADE, related_name='groups')` field to the `Group` model (or equivalent; confirm existing model name). Create and run the migration.
- `myportal/core/views.py` — update all Group-related views (`groups`, `group_detail`, `group_saved`, `group_members`) to filter querysets by the active client and to validate ownership before rendering or mutating.
- `myportal/templates/core/groups.html` — ensure the list only iterates over groups scoped to the current client.
- `myportal/templates/core/group_detail.html`, `group_saved.html`, `group_members.html` — add guard context so a user from a different client cannot see or interact with the page content.
- URL / permission helper (e.g. a `get_group_or_403` shortcut) — centralise the ownership check to avoid repeating it in every view.

**Out of scope for this round:**
- Changes to Building, User, Client, or Dashboard views.
- Modifying `static/css/app.css` or `static/js/app.js`.
- Django admin customisation.
- Redesigning the data model beyond the FK addition.

## Starting point
- Review `core/models.py` to confirm the current `Group` model definition and whether a client FK already exists.
- Review `core/views.py` to map all views that query or mutate `Group` objects — these all need the client-scoping filter added.
- Review `core/urls.py` to identify all Group-related URL patterns.
- Check how the active client context is currently resolved (session variable, URL parameter, or user profile FK) — use the same mechanism for the ownership check.
- Review `templates/core/groups.html` and related templates to understand current rendering so the scoping change does not break the UI.

## Expected deliverables
1. Migration file adding `client` FK to the `Group` model.
2. Updated `core/views.py` with client-scoped querysets and 403 guards on all Group views.
3. Updated Group templates reflecting the scoped data (no cross-client group links or entries visible).
4. A reusable ownership-check helper (function or mixin) to keep the guard logic DRY.
5. No unrelated architecture changes.

## Acceptance criteria
- A group created under Client A does not appear in the groups list when the user is operating under Client B.
- Directly navigating to a group URL belonging to Client A while operating as Client B returns a 403 or redirects gracefully.
- Group creation form automatically associates the new group with the currently active client (no manual client selection required by the user).
- Existing groups list, detail, and member management flows continue to work correctly for the owning client.
- No changes to unrelated modules (`app.css`, buildings, dashboard, left panel).
