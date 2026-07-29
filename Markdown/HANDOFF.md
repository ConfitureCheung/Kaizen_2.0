# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, profile, and the Vault section.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) remain layout-only or sample-data driven and are **deferred** to a later stage.
The Groups pages (`groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html`) are **complete** — all four screens are queryset-backed, wired to real backend logic, client-scoped, and consistent with the shared BLENDY visual language.
The Users pages (`users.html`, `user_detail.html`) are **complete** — both screens are queryset-backed, wired to real backend logic (create, edit, group assignment, activate/deactivate), and consistent with the shared visual language.
The **`dashboard.html` functional review and update is complete** — the page is fully connected to real queryset-backed data and live summary logic.
The **sliding left panel** in `base.html` is **complete** — full open/close animation, overlay backdrop, keyboard dismissal, and tree expand/collapse behaviour are all implemented.
The **Django admin consistency** work is **complete** — `core/admin.py` is fully configured with `list_display`, `list_filter`, `search_fields`, `fieldsets`, `readonly_fields`, and display helpers for all models; `admin_custom.css` applies BLENDY design tokens to the admin shell; branding is set.
The **Vault section is complete** — both `trend_log.html` (Trend Logs) and `objects.html` (Objects) are built, wired to the per-building SQLite database via raw `sqlite3` connections, and rendering correctly inside the BLENDY shell.
The **next active implementation stage is the Insight section** — five new pages covering insight management, report creation, rule management, golden standard configuration, and subscription.

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
- **Vault section is complete**: `trend_log.html` and `objects.html` are both live, reading data from the building-linked SQLite database via raw `sqlite3` connections. Both extend `base.html` and follow the existing list-view visual pattern.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.

## What is not yet done — current target
**Insight section — five new HTML pages.** These pages introduce the analytics and rules engine layer of the BLENDY portal:

- **`insight_management.html`** — landing page for the Insight section. Shows a list/dashboard of existing insight reports with summary cards (title, building, rule count, last run, status). Entry point for creating a new report or managing existing ones.
- **`create_insight_report.html`** — form/wizard page to create a new Insight Report. Captures report name, linked building, date range, and selected rule sets to apply.
- **`manage_rules.html`** — rule management page. Lists all available insight rules (name, description, category, severity, active/inactive toggle). Allows adding, editing, or deactivating rules.
- **`golden_standard_configuration.html`** — configuration page for Golden Standard reference values. Allows setting expected/reference values (setpoints, thresholds, acceptable ranges) per building or object type, used as the benchmark for insight rule evaluation.
- **`insight_subscription.html`** — subscription management page. Lets users subscribe or unsubscribe to scheduled insight report deliveries (email/notification), configure frequency (daily/weekly/monthly), and manage recipient lists.

## Important implementation notes
- All five pages are **building-scoped or organisation-scoped** — resolve the active building or client context consistently with existing views.
- Templates must extend `base.html` or `base2.html` and use the existing BLENDY CSS tokens; no new CSS files unless strictly necessary.
- Follow the existing visual patterns: list views use the card + table pattern (see `users.html`, `clients.html`); forms use the existing form card pattern (see `user_detail.html`).
- URL patterns should follow the existing convention: `/insight/`, `/insight/create/`, `/insight/rules/`, `/insight/golden-standard/`, `/insight/subscription/`.
- Start with layout-first (static/sample data) pages for this stage; backend wiring is a subsequent step.

## Relevant files for the next session
- `myportal/core/views.py` — add five Insight view stubs.
- `myportal/core/urls.py` — add URL patterns for the five Insight pages.
- `myportal/templates/core/insight_management.html` — new template.
- `myportal/templates/core/create_insight_report.html` — new template.
- `myportal/templates/core/manage_rules.html` — new template.
- `myportal/templates/core/golden_standard_configuration.html` — new template.
- `myportal/templates/core/insight_subscription.html` — new template.
- `static/css/app.css` — read-only reference for CSS tokens; do not modify.

## Next task
Work on **Insight section layout** — five new HTML pages:
`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`.

This next step should include:
- Building all five templates extending `base.html`/`base2.html`, using static/sample data for layout validation.
- Adding five view stubs to `core/views.py`.
- Registering URL patterns in `core/urls.py` under `/insight/`.
- Ensuring the Insight nav item in the sidebar/navigation routes to `insight_management.html` as the section home.

## Constraints for the next edit
- Focus on Insight section layout pages only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard, Vault, Left panel, Admin).
- Do not modify `static/css/app.css` or any existing admin files.
- Preserve all existing model registrations and view signatures.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the Insight section layout — five new HTML pages:
  insight_management.html, create_insight_report.html, manage_rules.html,
  golden_standard_configuration.html, insight_subscription.html.
Constraints:
- layout-first using static/sample data; backend wiring is a later step
- extend base.html or base2.html; use existing BLENDY CSS tokens
- follow the list-view card+table pattern for management/list pages
- follow the form card pattern for create/config/subscription pages
- add five view stubs to core/views.py
- add URL patterns under /insight/ in core/urls.py
- no modifications to app.css, admin files, or any already-completed views
Reference:
- users.html and clients.html for the list-view pattern
- user_detail.html for the form/card pattern
- objects.html for the split-panel pattern (if needed for manage_rules)
Please return complete updated files only.
```
