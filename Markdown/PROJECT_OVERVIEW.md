# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a functioning sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context.
The Profile page, Client pages, Groups pages, and **Users pages are all functionally complete**. The **next active focus is `dashboard.html`**. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, global icon navigation, and the sliding left panel — all shared across authenticated pages.
- `core/views.py` already contains helper logic for allowed clients and queryset-backed pages that can be reused to supply dashboard context.
- `core/urls.py` already defines the main application page routes, including `dashboard`.
- `static/css/app.css` already defines the app’s visual language for cards, forms, banners, tables, buttons, and responsive behaviour.
- The data model supports the custom user model in `accounts/models.py`.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard | `dashboard.html` | 🔄 In progress |

## Dashboard page — current state
`dashboard.html` currently exists as a partial layout or sample-data screen. It needs to be connected to real queryset-backed data and live summary logic.

## Dashboard page — planned functional behaviour
- **Summary KPI cards** — total counts for active users, clients, buildings, and groups pulled from live querysets.
- **Recent activity feed** — a short list of the most recently created or updated records across key models.
- **Client → Building overview** — a summary table or card list showing clients with their building counts, consistent with the left panel hierarchy.
- **Insight/alert strip** — surface any flagged conditions (e.g. users with no group, buildings with no client assignment) as actionable inline notices.
- **Charts (if applicable)** — data visualisations such as insight counts by building or user activity trends, using the existing chart library already referenced in the project.

## Users pages — completed state
Both Users screens are now fully functional:
- **`users.html`** — queryset-backed list view showing full name, email, work phone, group badges, and action buttons (edit, activate/deactivate).
- **`user_detail.html`** — handles both create (no `pk`) and edit (with `pk`) flows with POST save, validation feedback, group assignment, and active status toggling. Django admin registration for the custom user model is in place.

## Groups pages — completed state
All four Groups screens are fully functional:
- **`groups.html`** — queryset-backed list view with group name, member count, and action buttons.
- **`group_detail.html`** — handles create and edit flows with POST save, permission flag saving, and redirect to `group_saved`.
- **`group_saved.html`** — confirmation screen showing real group context (name, permissions, members).
- **`group_members.html`** — member-selection screen with checkbox table and POST membership update.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred until after the Dashboard work is complete:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `templates/core/dashboard.html` — dashboard UI.
- `core/views.py` — update `dashboard_view` to supply real queryset context.
- `core/urls.py` — route verification for dashboard URL.
- `static/css/app.css` — add only what is missing for dashboard-specific layout.
- `static/js/app.js` — add chart initialisation or dashboard interactivity if needed.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
