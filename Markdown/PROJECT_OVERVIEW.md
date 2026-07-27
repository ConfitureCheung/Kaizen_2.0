# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a functioning sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context.
The Profile page, Client pages, Groups pages, Users pages, and **Dashboard are all functionally complete**. The **next active focus is the sliding left panel interactive function**. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, global icon navigation, and the sliding left panel — all shared across authenticated pages.
- `static/css/app.css` already defines the app's visual language for cards, forms, banners, tables, buttons, and responsive behaviour.
- `static/js/app.js` already contains shared interaction logic that can be extended for the panel.
- The panel HTML structure and Client → Building tree rendering already exist in `base.html`; only JS and CSS work is needed.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard | `dashboard.html` | ✅ Functional |

## Sliding left panel — current state
The panel HTML structure in `base.html` and the Client → Building tree data rendering are already in place. The panel is rendered from queryset-backed context (`sidebar_clients`, `sidebar_profile`). What is missing is the full interactive behaviour: smooth open/close animation, overlay backdrop, keyboard dismissal, and tree expand/collapse.

## Sliding left panel — planned functional behaviour
- **Open/close toggle** — hamburger button triggers a smooth CSS slide-in/out animation.
- **Overlay backdrop** — a semi-transparent overlay appears behind the panel when open; clicking it closes the panel.
- **Keyboard dismissal** — pressing `Escape` closes the panel.
- **Tree expand/collapse** — clients in the panel can be expanded or collapsed to reveal their buildings.
- **Active state highlighting** — the currently active page item is highlighted in the tree.
- **Persistent state (optional)** — open/closed state optionally preserved across page navigation.

## Dashboard page — completed state
`dashboard.html` is now fully connected to real queryset-backed data:
- **Summary KPI cards** — live counts for active users, clients, buildings, and groups.
- **Recent activity feed** — most recently created or updated records across key models.
- **Client → Building overview** — summary table consistent with the left panel hierarchy.
- **Insight/alert strip** — flagged conditions (users with no group, buildings with no client assignment).
- **Chart widgets** — data visualisations wired to context data from `dashboard_view`.

## Users pages — completed state
Both Users screens are fully functional:
- **`users.html`** — queryset-backed list view showing full name, email, work phone, group badges, and action buttons (edit, activate/deactivate).
- **`user_detail.html`** — handles both create (no `pk`) and edit (with `pk`) flows with POST save, validation feedback, group assignment, and active status toggling.

## Groups pages — completed state
All four Groups screens are fully functional:
- **`groups.html`** — queryset-backed list view with group name, member count, and action buttons.
- **`group_detail.html`** — handles create and edit flows with POST save, permission flag saving, and redirect to `group_saved`.
- **`group_saved.html`** — confirmation screen showing real group context (name, permissions, members).
- **`group_members.html`** — member-selection screen with checkbox table and POST membership update.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred until after the sliding left panel work is complete:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `templates/base.html` — panel HTML structure, hamburger button, overlay element.
- `static/css/app.css` — panel slide animation, overlay styles, tree expand/collapse transitions.
- `static/js/app.js` — open/close toggle, overlay click handler, Escape key handler, tree expand/collapse logic.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
