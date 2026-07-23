# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation now includes a functioning sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context.
The Profile page is functionally complete. The next focus is the **Client-related pages**.

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, global icon navigation, and the sliding left panel — all shared across authenticated pages.
- `core/views.py` already contains helper logic for allowed clients and queryset-backed pages that can be reused to provide shared navigation context.
- `core/urls.py` already defines the main application page routes, including `clients`, `client_detail`, and `client_saved`.
- `static/css/app.css` already defines the app's visual language for cards, forms, banners, tables, buttons, and responsive behavior.
- The data model supports a Client → Building hierarchy: `Building` has a foreign key to `Client`, and group/building-user relationships already exist.

## Client pages — current state
The three Client screens exist as layout-only or sample-data templates:
- **`clients.html`** — list view, not yet queryset-backed.
- **`client_detail.html`** — detail view, not yet pulling real data from the `Client` model.
- **`client_saved.html`** — create/edit form, not yet wired to POST handling or database save logic.

## Client pages — planned functional behavior
- `clients_view` should return all `Client` records accessible to the logged-in user, ordered consistently.
- `client_detail_view` should return a single client by primary key, with prefetched buildings and groups for efficient template rendering.
- `client_saved_view` should handle both create (no `pk`) and edit (with `pk`) flows: render the form on GET, validate and save on POST, and redirect to `client_detail` on success or re-render with errors on failure.
- Django admin should have `Client` registered so records are visible and manageable.

## Left panel consistency
The sliding left panel in `base.html` already renders clients and buildings from shared context.
Any create, edit, or delete action on a `Client` record must keep the left panel context up to date — this is already handled if the shared context processor or view context is called consistently on every authenticated page render.

## Files most relevant for the next step
- `templates/core/clients.html` for the client list UI.
- `templates/core/client_detail.html` for the client detail UI.
- `templates/core/client_saved.html` for the create/edit form UI.
- `core/views.py` — `clients_view`, `client_detail_view`, `client_saved_view`.
- `core/urls.py` — route verification for all three client URLs.
- `core/models.py` — `Client` model reference.
- `core/admin.py` — ensure `Client` is registered.
- `static/css/app.css` — reuse existing patterns; add only what is missing.
- `static/js/app.js` — add any client-specific interactivity.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
