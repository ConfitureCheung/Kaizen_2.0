# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a functioning sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context.
The Profile page and Client pages are functionally complete. The **next active focus is the Groups-related HTML pages**. Buildings pages are deferred to a later stage.

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, global icon navigation, and the sliding left panel — all shared across authenticated pages.
- `core/views.py` already contains helper logic for allowed clients and queryset-backed pages that can be reused to provide shared navigation context.
- `core/urls.py` already defines the main application page routes, including `groups`, `group_detail`, `group_saved`, and `group_members`.
- `static/css/app.css` already defines the app’s visual language for cards, forms, banners, tables, buttons, groups pages, and responsive behavior.
- The data model supports group → user membership: the `Group` (or custom group) model and permission flags already exist in `core/models.py`.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | 🔄 In progress |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard | `dashboard.html` | 🔲 Partial / layout |

## Groups pages — current state
The four Groups screens exist and have CSS classes defined, but may not yet be fully wired to live queryset data:
- **`groups.html`** — list view, may not yet be queryset-backed.
- **`group_detail.html`** — detail/form view, may not yet handle POST save or validation feedback.
- **`group_saved.html`** — confirmation screen after save, may not yet receive real group context.
- **`group_members.html`** — member-selection screen, may not yet save membership changes.

## Groups pages — planned functional behavior
- `groups_view` should return all `Group` records, ordered consistently, with member count annotations if useful.
- `group_detail_view` should handle both create (no `pk`) and edit (with `pk`) flows: render the form on GET, validate and save on POST (including permission flags and per-page permission rows), and redirect to `group_saved` on success.
- `group_saved_view` should return the saved group with its permission summary and a list of current members.
- `group_members_view` should render all users with checkboxes pre-filled for current members and handle POST to update group membership.
- Django admin should have the group model registered so records are visible and manageable.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred until after the Groups work is complete:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `templates/core/groups.html` — group list UI.
- `templates/core/group_detail.html` — group detail/edit form UI.
- `templates/core/group_saved.html` — group save confirmation UI.
- `templates/core/group_members.html` — member selection UI.
- `core/views.py` — `groups_view`, `group_detail_view`, `group_saved_view`, `group_members_view`.
- `core/urls.py` — route verification for all four group URLs.
- `core/models.py` — group and permission model reference.
- `core/admin.py` — ensure group model is registered.
- `static/css/app.css` — reuse existing patterns; add only what is missing.
- `static/js/app.js` — add any group-specific interactivity.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
