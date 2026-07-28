# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) are still layout-only or sample-data driven and are **deferred** to a later stage.
The Groups pages (`groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html`) are **complete** — all four screens are queryset-backed, wired to real backend logic, client-scoped, and consistent with the shared BLENDY visual language.
The Users pages (`users.html`, `user_detail.html`) are **complete** — both screens are queryset-backed, wired to real backend logic (create, edit, group assignment, activate/deactivate), and consistent with the shared visual language.
The **`dashboard.html` functional review and update is complete** — the page is fully connected to real queryset-backed data and live summary logic.
The **sliding left panel** in `base.html` is **complete** — full open/close animation, overlay backdrop, keyboard dismissal, and tree expand/collapse behaviour are all implemented.
The **Django admin consistency** work is **complete** — `core/admin.py` is fully configured with `list_display`, `list_filter`, `search_fields`, `fieldsets`, `readonly_fields`, and display helpers for all models; `admin_custom.css` applies BLENDY design tokens to the admin shell; branding is set.
The **next active implementation stage is the Vault section** — specifically the two new HTML pages: `trend_log.html` (Trend Logs) and `objects.html` (Objects).

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional and client-scoped: `groups.html` is queryset-backed, `group_detail_view` handles create/edit with ownership guards, `group_saved.html` shows the confirmation screen with real group context, and `group_members.html` handles membership updates.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail_view` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows.
- Users pages are fully functional: `users.html` is queryset-backed showing full name, email, work phone, group badges, and action buttons; `user_detail_view` handles both create and edit flows with POST save, validation feedback, group assignment, and activate/deactivate toggling.
- `dashboard.html` is now fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- The sliding left panel in `base.html` is fully interactive: smooth CSS `transform: translateX()` open/close animation, overlay backdrop with click-to-close, Escape key dismissal, tree expand/collapse for the Client → Building hierarchy, and active state highlighting.
- **Django admin is now fully consistent with the frontend view**: `core/admin.py` has complete `ModelAdmin` classes for `Client`, `ClientGroup`, `Building`, `BuildingUser`, and `BuildingDatabase` with `list_display`, `list_filter`, `search_fields`, `fieldsets`, `readonly_fields`, computed display helpers, and `save_model` overrides. `static/css/admin_custom.css` overrides Django admin CSS variables with BLENDY design tokens. Admin branding (`site_header`, `site_title`, `index_title`) is set.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.

## What is not yet done — current target
**Vault section — Trend Logs and Objects pages.** These are two new HTML pages to be built within the existing BLENDY portal shell:

- **`trend_log.html`** — displays Trend Log records read from the building's linked SQLite database. Should show a filterable/searchable list of trend log entries (name, description, object reference, units, timestamps). Follows the same list-view pattern as `users.html` and `clients.html`.
- **`objects.html`** — displays BACnet or similar Objects associated with the selected building. Should show a filterable list of object records (object type, instance, name, description, present value, units). Follows the same list-view pattern as other entity list pages.

Both pages live inside the Vault section, which is a building-scoped data viewer reading directly from the per-building SQLite database via `BuildingDatabase`.

## Important implementation notes
- Both pages are **building-scoped** — the active building is resolved from the URL (`building_pk`) or the session, consistent with how the sliding panel resolves context.
- Data is read from the **linked SQLite database** (the `db_file` on the `BuildingDatabase` model) using a separate, read-only SQLite connection — not through Django ORM models, as the building database has its own schema.
- Use Django's `sqlite3` module (Python stdlib) to open the building database and run raw SELECT queries. Do not use Django models or migrations for the building database.
- Templates must extend `base.html` and use the existing BLENDY CSS tokens, card/table styles, breadcrumb, and page title slot — no new CSS files unless strictly necessary.
- Follow the exact same visual pattern as other list views: a top filter/search bar, a table card with sortable columns, pagination, and row-level action buttons where appropriate.
- URL patterns should follow the existing convention: `/vault/<int:building_pk>/trend-logs/` and `/vault/<int:building_pk>/objects/`.

## Relevant files for the next session
- `myportal/core/views.py` — add `trend_log_view` and `objects_view`.
- `myportal/core/urls.py` — add URL patterns for the two new views.
- `templates/vault/trend_log.html` — new template (or `templates/trend_log.html` depending on template organisation).
- `templates/vault/objects.html` — new template.
- `myportal/core/models.py` — reference `BuildingDatabase` to locate the SQLite file path.
- `static/css/app.css` — read-only reference for CSS tokens; do not modify.

## Next task
Work on **Vault — Trend Logs (`trend_log.html`) and Objects (`objects.html`) pages**.

This next step should include:
- Adding `trend_log_view` and `objects_view` to `core/views.py`, each opening the building's SQLite database with a raw `sqlite3` connection and querying the relevant table.
- Registering URL patterns in `core/urls.py` under `/vault/<building_pk>/`.
- Building `trend_log.html` and `objects.html` as list-view templates extending `base.html`, using the existing table card pattern.
- Handling the case where no `BuildingDatabase` is linked (show an empty-state card with a message).

## Constraints for the next edit
- Focus on Vault Trend Logs and Objects pages only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard, Left panel, Admin).
- Do not modify `static/css/app.css` or any existing admin files.
- Preserve all existing model registrations and view signatures.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the Vault section — Trend Logs (trend_log.html) and Objects (objects.html) pages.
Constraints:
- keep current Django structure and naming style
- read data from the per-building SQLite database using raw sqlite3 — no new Django models or migrations
- extend base.html; use existing BLENDY CSS tokens and table card pattern
- no modifications to app.css, admin files, or any already-completed views
- add trend_log_view and objects_view to core/views.py
- add URL patterns under /vault/<building_pk>/ in core/urls.py
Reference:
- users.html and clients.html for the list-view pattern to follow
- BuildingDatabase model for the db_file path
Please return complete updated files only.
```
