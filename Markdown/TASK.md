# TASK

## Current task
Bring the **Django admin** into visual and behavioural consistency with the frontend view.

## Immediate objective
Align the Django admin UI with the BLENDY frontend so that admin users see the same columns, filters, field groupings, and actions as the frontend views, and experience the same visual language (colours, typography, border radius, table styles).

This should include:
- `list_display`, `list_filter`, `search_fields`, and `ordering` on every `ModelAdmin` mirroring the frontend list view columns and filters.
- `fieldsets` on every `ModelAdmin` mirroring the frontend detail page field groupings.
- Read-only / computed display fields (e.g. group member count, building count per client) surfaced in the admin list.
- Bulk admin actions (e.g. activate/deactivate users) consistent with the per-row actions in the frontend.
- Custom admin CSS (`static/css/admin_custom.css`) overriding Django admin colour variables and typography with BLENDY design tokens.
- Admin site branding: `site_header`, `site_title`, and `index_title` set to the BLENDY product name.
- (Optional) `templates/admin/base_site.html` override to inject the BLENDY logo and custom CSS into the admin shell.

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
- `myportal/core/admin.py` — add `list_display`, `list_filter`, `search_fields`, `ordering`, `fieldsets`, `readonly_fields`, and `actions` to all registered model admins.
- `myportal/accounts/admin.py` — configure the custom user `ModelAdmin` with the same consistency.
- `static/css/admin_custom.css` — new file; CSS variable overrides targeting Django admin’s built-in CSS custom properties.
- `templates/admin/base_site.html` — optional; override to inject BLENDY branding and the custom CSS file.

**Out of scope for this round:**
- Refactoring unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard, Left panel).
- Modifying `static/css/app.css`.
- Adding new backend routes or view logic outside of admin.
- Redesigning the data model.
- Functional wiring of Buildings pages (still deferred).

## Starting point
- Review `core/admin.py` and `accounts/admin.py` to audit which models are currently registered and what (if any) `ModelAdmin` customisation already exists.
- Review each frontend list view (`users.html`, `clients.html`, `groups.html`, `buildings.html`) for the exact columns and filters shown — replicate these in the corresponding `ModelAdmin.list_display` and `list_filter`.
- Review each frontend detail view (`user_detail.html`, `client_detail.html`, `group_detail.html`, `building_detail.html`) for field groupings — replicate these in `fieldsets`.
- Check `static/css/app.css` for existing design tokens (primary colour, font, border radius) to use as the source of truth for `admin_custom.css`.
- Django admin overridable CSS variables are in `django/contrib/admin/static/admin/css/base.css` — target these with `:root` overrides in `admin_custom.css`.

## Expected deliverables
1. `core/admin.py` with `list_display`, `list_filter`, `search_fields`, `ordering`, `fieldsets`, `readonly_fields`, and bulk `actions` for all models.
2. `accounts/admin.py` with consistent custom user admin configuration.
3. `static/css/admin_custom.css` with BLENDY colour, font, and border-radius overrides for the Django admin.
4. (Optional) `templates/admin/base_site.html` injecting the custom CSS and BLENDY site header.
5. No unrelated architecture changes.

## Acceptance criteria
- Admin list views show the same columns and filters as the corresponding frontend list pages.
- Admin detail/form views group fields in the same way as the frontend detail pages.
- Bulk activate/deactivate action available on the Users admin list.
- Django admin primary colour, font, and border radius visually match the BLENDY frontend.
- Admin site header reads BLENDY (or the project display name).
- Changes remain targeted and do not disturb unrelated modules or `app.css`.
