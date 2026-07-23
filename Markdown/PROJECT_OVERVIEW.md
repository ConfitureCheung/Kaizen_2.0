# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation now includes a functioning sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context.
The Profile page and Client pages are functionally complete. The next focus is the **Buildings-related pages**.

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, global icon navigation, and the sliding left panel — all shared across authenticated pages.
- `core/views.py` already contains helper logic for allowed clients and queryset-backed pages that can be reused to provide shared navigation context.
- `core/urls.py` already defines the main application page routes, including `buildings`, `building_detail`, and `building_report`.
- `static/css/app.css` already defines the app's visual language for cards, forms, banners, tables, buttons, and responsive behavior.
- The data model supports a Client → Building hierarchy: `Building` has a foreign key to `Client`, and group/building-user relationships already exist.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_members.html` | ✅ Functional |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only |
| Dashboard | `dashboard.html` | 🔲 Partial / layout |

## Buildings pages — current state
The three Buildings screens exist as layout-only or sample-data templates:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Buildings pages — planned functional behavior
- `buildings_view` should return all `Building` records accessible to the logged-in user, filtered by client ownership, ordered consistently.
- `building_detail_view` should handle both create (no `pk`) and edit (with `pk`) flows: render the form on GET, validate and save on POST, and redirect to `building_report` or `buildings` on success.
- `building_report_view` should return a single building by primary key with prefetched sensor/energy data or related readings for chart rendering.
- Django admin should have `Building` registered so records are visible and manageable.

## Left panel consistency
The sliding left panel in `base.html` already renders clients and buildings from shared context.
Any create, edit, or delete action on a `Building` record must keep the left panel context up to date — this is already handled if the shared context processor or view context is called consistently on every authenticated page render.

## Files most relevant for the next step
- `templates/core/buildings.html` for the building list UI.
- `templates/core/building_detail.html` for the building detail/edit form UI.
- `templates/core/building_report.html` for the building report and chart UI.
- `core/views.py` — `buildings_view`, `building_detail_view`, `building_report_view`.
- `core/urls.py` — route verification for all three building URLs.
- `core/models.py` — `Building` model reference.
- `core/admin.py` — ensure `Building` is registered.
- `static/css/app.css` — reuse existing patterns; add only what is missing.
- `static/js/app.js` — add any building-specific interactivity.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
