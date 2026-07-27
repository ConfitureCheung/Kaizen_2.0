# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) are still layout-only or sample-data driven and are **deferred** to a later stage.
The Groups pages (`groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html`) are **complete** — all four screens are queryset-backed, wired to real backend logic, and consistent with the shared BLENDY visual language.
The Users pages (`users.html`, `user_detail.html`) are **complete** — both screens are queryset-backed, wired to real backend logic (create, edit, group assignment, activate/deactivate), and consistent with the shared visual language.
The **`dashboard.html` functional review and update is complete** — the page is fully connected to real queryset-backed data and live summary logic.
The **sliding left panel** in `base.html` is now **complete** — full open/close animation, overlay backdrop, keyboard dismissal, and tree expand/collapse behaviour are all implemented.
The next active implementation stage is **Django admin consistency with the frontend view**.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional: `groups.html` is queryset-backed, `group_detail.html` handles create and edit flows with POST save and permission wiring, `group_saved.html` shows the confirmation screen with real group context, and `group_members.html` handles membership updates.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail.html` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows with POST save and redirect on success.
- Users pages are fully functional: `users.html` is queryset-backed showing full name, email, work phone, group badges, and action buttons; `user_detail.html` handles both create and edit flows with POST save, validation feedback, group assignment, and activate/deactivate toggling.
- `dashboard.html` is now fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip. Chart widgets are wired to context data.
- The sliding left panel in `base.html` is fully interactive: smooth CSS `transform: translateX()` open/close animation, overlay backdrop with click-to-close, Escape key dismissal, tree expand/collapse for the Client → Building hierarchy, and active state highlighting.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.

## What is not yet done — current target
**Django admin consistency with the frontend view.** The Django admin currently uses the default Django admin styling and default `ModelAdmin` configuration. The goal is to bring the admin UI into visual and behavioural alignment with the frontend so that admin users experience a coherent product.

Planned work:
- **Custom admin CSS** — create `static/css/admin_custom.css` to override Django admin CSS variables (primary colour, font stack, border radius, card/table styles) with BLENDY design tokens.
- **Admin branding** — set `AdminSite.site_header`, `site_title`, and `index_title` to the BLENDY product name.
- **`ModelAdmin` list display** — configure `list_display`, `list_filter`, `search_fields`, and `ordering` for all registered models to mirror the columns and filters visible in the frontend list views.
- **`ModelAdmin` fieldsets** — organise detail/edit forms in the admin to match the field groupings used in the frontend detail pages.
- **Read-only and display fields** — surface computed/derived fields (e.g. group member count, building count per client) in the admin list the same way they appear in the frontend.
- **Admin actions** — add bulk actions (e.g. activate/deactivate users) consistent with the per-row actions available in the frontend.
- **Custom admin templates (optional)** — override `templates/admin/base_site.html` to inject the BLENDY logo and colour scheme into the admin shell.

## Important implementation notes
- The primary file to edit is `myportal/core/admin.py`; also review `myportal/accounts/admin.py` for the custom user model.
- Create `static/css/admin_custom.css` for design token overrides. Reference it from a custom `templates/admin/base_site.html` using `{% block extrastyle %}` or Django admin’s `Media` class.
- Do not modify the existing `static/css/app.css` — admin styles should be isolated in their own file.
- Use `ModelAdmin.list_display`, `list_filter`, `search_fields`, `ordering`, `fieldsets`, `readonly_fields`, and `actions` as the primary extension points — no custom views needed.
- Check each frontend list view (`users.html`, `clients.html`, `groups.html`, `buildings.html`) for the exact columns, filters, and actions shown, and replicate those in the corresponding `ModelAdmin`.
- Preserve all existing admin registrations and do not remove any currently registered models.

## Relevant files for the next session
- `myportal/core/admin.py` — primary `ModelAdmin` configuration file.
- `myportal/accounts/admin.py` — custom user admin configuration.
- `static/css/admin_custom.css` — new file; BLENDY design token overrides for Django admin CSS variables.
- `templates/admin/base_site.html` — optional admin shell override for branding and CSS injection.
- `templates/` list views for reference: `users.html`, `clients.html`, `groups.html`, `buildings.html`.

## Next task
Work on **Django admin consistency with the frontend view**.

This next step should include:
- Reviewing `core/admin.py` and `accounts/admin.py` to audit current model registrations.
- Adding `list_display`, `list_filter`, `search_fields`, and `ordering` to each `ModelAdmin` to match the frontend list views.
- Adding `fieldsets` to each `ModelAdmin` to match the frontend detail page field groupings.
- Creating `static/css/admin_custom.css` with BLENDY colour and typography overrides.
- Setting admin site branding (`site_header`, `site_title`, `index_title`).
- Optionally creating `templates/admin/base_site.html` to inject the custom CSS and logo.

## Constraints for the next edit
- Focus on admin consistency only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard, Left panel).
- Do not modify `static/css/app.css`.
- Preserve all existing model registrations.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: bring Django admin into visual and behavioural consistency with the frontend view.
Constraints:
- keep current Django structure
- keep existing bulk style in app.css unchanged
- no unrelated refactor
- preserve all existing admin registrations
- only touch admin.py files, admin_custom.css, and optionally templates/admin/
Reference:
- frontend list views: users.html, clients.html, groups.html, buildings.html
- frontend detail views: user_detail.html, client_detail.html, group_detail.html, building_detail.html
Please return complete updated files only.
```
