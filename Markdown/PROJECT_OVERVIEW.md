# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a functioning sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context.
The Profile page, Client pages, and Groups pages are functionally complete. The **next active focus is the Users-related HTML pages**: `users.html` and `user_detail.html`. Buildings pages are deferred to a later stage.

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, global icon navigation, and the sliding left panel — all shared across authenticated pages.
- `core/views.py` already contains helper logic for allowed clients and queryset-backed pages that can be reused to provide shared navigation context.
- `core/urls.py` already defines the main application page routes, including `users` and `user_detail`.
- `static/css/app.css` already defines the app’s visual language for cards, forms, banners, tables, buttons, and responsive behavior.
- The data model supports the custom user model in `accounts/models.py`.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | 🔄 In progress |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard | `dashboard.html` | 🔲 Partial / layout |

## Users pages — current state
The two Users screens exist and may already have some functional wiring, but need review and updates for consistency and completeness:
- **`users.html`** — list view of all user accounts; should be queryset-backed showing full name, email, work phone, group badges, and action buttons.
- **`user_detail.html`** — detail/edit form for a single user; should handle both create (no `pk`) and edit (with `pk`) flows with POST save, validation feedback, and group assignment.

## Users pages — planned functional behavior
- `users_view` should return all user records ordered consistently (e.g., by full name), with group membership prefetched for display.
- `user_detail_view` should handle both create (no `pk`) and edit (with `pk`) flows: render the form on GET, validate and save on POST (including group assignment and active status toggle), and redirect appropriately on success.
- Django admin should have the custom user model registered so records are visible and manageable.

## Groups pages — completed state
All four Groups screens are now fully functional:
- **`groups.html`** — queryset-backed list view with group name, member count, and action buttons.
- **`group_detail.html`** — handles create and edit flows with POST save, permission flag saving, and redirect to `group_saved`.
- **`group_saved.html`** — confirmation screen showing real group context (name, permissions, members).
- **`group_members.html`** — member-selection screen with checkbox table and POST membership update.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred until after the Users work is complete:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `templates/core/users.html` — user list UI.
- `templates/core/user_detail.html` — user detail/edit form UI.
- `core/views.py` — `users_view`, `user_detail_view`.
- `core/urls.py` — route verification for user URLs.
- `accounts/models.py` — custom user model reference.
- `core/admin.py` — ensure custom user model is registered.
- `static/css/app.css` — reuse existing patterns; add only what is missing.
- `static/js/app.js` — add any user-specific interactivity.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
