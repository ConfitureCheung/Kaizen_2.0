# PROJECT OVERVIEW

## Current status
The BLENDY Django project includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.
The shared navigation includes a fully interactive sliding left panel in `base.html` triggered by the hamburger button, rendering a Client → Building tree from queryset-backed context, with smooth CSS slide animation, overlay backdrop, keyboard dismissal, and tree expand/collapse.
The Profile page, Client pages, Groups pages (now fully client-scoped), Users pages, Dashboard, and **sliding left panel are all functionally complete**. The **next active focus is Django admin consistency with the frontend view**. Buildings pages remain deferred to a later stage.

## Existing structure relevant to the next step
- `myportal/core/admin.py` — registers models with the Django admin site; the main file to customise for consistency.
- `myportal/accounts/admin.py` — registers the custom user model with the Django admin site.
- `templates/` — the existing frontend visual language (cards, forms, tables, colour tokens) is the reference target for admin styling.
- `static/css/app.css` already defines the app's visual language; a new `static/css/admin_custom.css` file will carry the same design tokens targeted at Django admin CSS variables.
- Django's built-in admin can be overridden using a custom `AdminSite`, `ModelAdmin` subclasses, and a `templates/admin/` override directory.

## Completed pages
| Page area | Pages | Status |
|---|---|---|
| Auth | Login / Logout | ✅ Functional |
| Profile | `profile.html` | ✅ Functional |
| Users | `users.html`, `user_detail.html` | ✅ Functional |
| Groups | `groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html` | ✅ Functional + client-scoped |
| Clients | `clients.html`, `client_detail.html`, `client_saved.html` | ✅ Functional |
| Buildings | `buildings.html`, `building_detail.html`, `building_report.html` | 🔲 Layout-only (deferred) |
| Dashboard | `dashboard.html` | ✅ Functional |
| Left panel | Sliding panel in `base.html` | ✅ Functional |
| Django admin | `core/admin.py`, `accounts/admin.py` | 🔲 Default (in progress) |

## Django admin consistency — planned work
The goal is to bring the Django admin UI into visual and behavioural alignment with the frontend view, so that admin users experience a coherent product rather than switching between two distinct visual systems.

Planned work includes:

- **Custom admin CSS** — override Django admin colour variables and typography to match the BLENDY design tokens (primary colour, font stack, border radius, card/table styles) via a new `static/css/admin_custom.css`.
- **`ModelAdmin` list display** — configure `list_display`, `list_filter`, `search_fields`, and `ordering` for all registered models to mirror the columns and filters visible in the frontend list views.
- **`ModelAdmin` fieldsets** — organise detail/edit forms in the admin to match the field groupings used in the frontend detail pages.
- **Read-only and display fields** — surface computed or derived fields (e.g. group member count, building count per client) in the admin list the same way they appear in the frontend.
- **Admin actions** — add bulk actions (e.g. activate/deactivate users) consistent with the per-row actions available in the frontend.
- **Admin branding** — set `AdminSite.site_header`, `site_title`, and `index_title` to match the BLENDY product name.
- **Custom admin templates (optional)** — override `templates/admin/base_site.html` to inject the BLENDY logo and colour scheme into the admin shell using `{% block extrastyle %}`.

## Groups pages — completed state (now client-scoped)
All four Groups screens are fully functional and client-scoped:
- **`groups.html`** — queryset-backed list view filtered to the active client; shows group name, member count, and action buttons.
- **`group_detail.html`** — handles create and edit flows with POST save, permission flag saving, client ownership guard (403 if mismatch), and redirect to `group_saved`.
- **`group_saved.html`** — confirmation screen showing real group context (name, permissions, members) with ownership guard.
- **`group_members.html`** — member-selection screen with checkbox table and POST membership update; enforces client ownership.
- The `ClientGroup` model carries a `ForeignKey` to `Client`; all Group views resolve the active client via `get_active_client` / `get_allowed_client_ids` helpers in `core/sidebar.py`.

## Sliding left panel — completed state
The full interactive behaviour has been implemented:
- **Open/close toggle** — hamburger button triggers a smooth CSS `transform: translateX()` slide-in/out animation.
- **Overlay backdrop** — semi-transparent overlay appears behind the panel when open; clicking it closes the panel.
- **Keyboard dismissal** — pressing `Escape` closes the panel.
- **Tree expand/collapse** — client rows in the panel expand and collapse to show/hide their buildings.
- **Active state highlighting** — the currently visited page's building or client is visually highlighted in the tree.

## Dashboard page — completed state
`dashboard.html` is fully connected to real queryset-backed data:
- **Summary KPI cards** — live counts for active users, clients, buildings, and groups.
- **Recent activity feed** — most recently created or updated records across key models.
- **Client → Building overview** — summary table consistent with the left panel hierarchy.
- **Insight/alert strip** — flagged conditions (users with no group, buildings with no client assignment).
- **Chart widgets** — data visualisations wired to context data from `dashboard_view`.

## Users pages — completed state
Both Users screens are fully functional:
- **`users.html`** — queryset-backed list view showing full name, email, work phone, group badges, and action buttons (edit, activate/deactivate).
- **`user_detail.html`** — handles both create (no `pk`) and edit (with `pk`) flows with POST save, validation feedback, group assignment, and active status toggling.

## Buildings pages — deferred state
The three Buildings screens remain layout-only or sample-data driven. Their functional wiring is intentionally deferred:
- **`buildings.html`** — list view, not yet queryset-backed.
- **`building_detail.html`** — detail/form view, not yet wired to POST handling or database save logic.
- **`building_report.html`** — report view, not yet pulling real data or rendering live charts.

## Files most relevant for the next step
- `myportal/core/admin.py` — primary file for `ModelAdmin` list display, fieldsets, and actions.
- `myportal/accounts/admin.py` — custom user admin configuration.
- `static/css/admin_custom.css` — new file for BLENDY design token overrides targeting Django admin CSS variables.
- `templates/admin/base_site.html` — optional override for admin shell branding.

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.
- Reuse the shared shell and CSS language already present in the project.
- Ask for complete updated files for touched files only when using AI help.
