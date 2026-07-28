# TASK

## Current task
Bring the **Django admin** into visual and behavioural consistency with the frontend portal view.

## Immediate objective
The Django admin currently uses default Django admin styling and default `ModelAdmin` configuration. The goal is to make the admin UI a coherent extension of the BLENDY product so that admin users do not experience a jarring switch between two distinct visual and structural systems.

Specific targets:
- **Custom admin CSS** — override Django admin CSS variables (primary colour, font stack, border radius, card/table styles) with BLENDY design tokens in a new `static/css/admin_custom.css` file.
- **Admin branding** — set `AdminSite.site_header`, `site_title`, and `index_title` to the BLENDY product name.
- **`ModelAdmin` list display** — configure `list_display`, `list_filter`, `search_fields`, and `ordering` for all registered models to mirror the columns and filters shown in the frontend list views.
- **`ModelAdmin` fieldsets** — organise detail/edit forms in the admin to match the field groupings in the frontend detail pages.
- **Read-only and display fields** — surface computed/derived fields (e.g. group member count, building count per client) the same way they appear on the frontend.
- **Admin actions** — add bulk actions (e.g. activate/deactivate users) consistent with the per-row actions on the frontend.
- **Custom admin templates (optional)** — override `templates/admin/base_site.html` to inject the BLENDY logo and colour scheme into the admin shell using `{% block extrastyle %}`.

## Background from the previous step
The client-scoped group pages are now complete and production-ready:
- `ClientGroup` model carries a `ForeignKey` to `Client`.
- All Group views (`groups_view`, `group_detail_view`, `group_saved_view`, `group_members_view`, `group_delete_view`) filter querysets by the active client and enforce 403 guards.
- Helper functions `get_active_client` and `get_allowed_client_ids` in `core/sidebar.py` are used as the single source-of-truth for client resolution.
- Group templates iterate only over groups scoped to the active client.

## Scope for the next coding round

**In scope:**
- `myportal/core/admin.py` — primary file for `ModelAdmin` list display, fieldsets, read-only fields, search, filters, ordering, and bulk actions for `Client`, `Building`, `ClientGroup`, `BuildingUser`, `BuildingDatabase`.
- `myportal/accounts/admin.py` — custom user admin configuration for the `CustomUser` model (list display, search, filters, fieldsets).
- `static/css/admin_custom.css` — new file; BLENDY design token overrides for Django admin CSS variables.
- `templates/admin/base_site.html` — optional override for admin shell branding and CSS injection.

**Out of scope for this round:**
- Any frontend template changes (`users.html`, `clients.html`, `groups.html`, `buildings.html`, etc.).
- Changes to `static/css/app.css` or `static/js/app.js`.
- Model changes or new migrations.
- Refactoring of views, URLs, or forms.

## Starting point
- Review `core/admin.py` and `accounts/admin.py` to audit current model registrations and identify gaps.
- Reference each frontend list view for exact columns and filters to replicate:
  - `users.html` → `BuildingUserAdmin`
  - `clients.html` → `ClientAdmin`
  - `groups.html` → `ClientGroupAdmin`
  - `buildings.html` → `BuildingAdmin`
- Reference each frontend detail page for field groupings to replicate as `fieldsets`:
  - `user_detail.html`, `client_detail.html`, `group_detail.html`, `building_detail.html`
- Check `static/css/app.css` for the BLENDY colour variables to port into `admin_custom.css`.

## Expected deliverables
1. Updated `core/admin.py` with fully configured `ModelAdmin` classes for all core models.
2. Updated `accounts/admin.py` with a fully configured `CustomUserAdmin`.
3. New `static/css/admin_custom.css` with BLENDY colour and typography overrides.
4. Optional `templates/admin/base_site.html` for branding injection.
5. No changes to any other files.

## Acceptance criteria
- Django admin list pages for Users, Clients, Groups, and Buildings show the same columns and filters as the corresponding frontend list pages.
- Django admin detail pages group fields in the same logical sections as the frontend detail forms.
- Admin colour scheme (primary, link, header) visually matches the BLENDY design tokens.
- Admin site header reads "BLENDY" (or the current product name in `site_header`).
- Existing model registrations are all preserved — nothing is removed.
- `app.css` is untouched.
