# TASK

## Current task
Build the **Insight section layout** — five new HTML pages:
`insight_management.html`, `create_insight_report.html`, `manage_rules.html`, `golden_standard_configuration.html`, `insight_subscription.html`.

## Immediate objective
Create five new layout-first pages for the Insight section using static/sample data. All pages must fit seamlessly into the existing BLENDY portal shell and visual language. Backend wiring (queryset-backed data, form POST handling, rule evaluation logic) is a **subsequent step** and is out of scope here.

Specific targets:

- **`insight_management.html`** — section landing page. Shows a list of insight reports as summary cards or table rows: report title, linked building, rule count, last run timestamp, and status badge (pending/complete/failed). Includes a prominent "Create New Report" CTA button. Follows the `clients.html` list-view pattern.
- **`create_insight_report.html`** — form page to create a new Insight Report. Fields: report name, linked building (dropdown), date range (from/to date pickers), rule sets to apply (multi-select or checkbox list). Follows the `user_detail.html` form card pattern.
- **`manage_rules.html`** — rule management list page. Columns: rule name, description, category, severity badge, active/inactive toggle. Includes an "Add Rule" button. Follows the `users.html` list-view pattern with an action column.
- **`golden_standard_configuration.html`** — configuration page for Golden Standard reference values. Organised by building or object type. Fields: parameter name, expected value, min/max threshold, unit. Follows a settings-page form card pattern.
- **`insight_subscription.html`** — subscription management page. Shows a table of subscriptions (report name, frequency, recipients, next delivery, active toggle). Includes controls to add/edit subscriptions. Follows the `groups.html` list-view pattern.

## Background from the previous step
Vault section is now complete:
- `trend_log_view` and `objects_view` are implemented in `core/views.py`, reading data from the per-building SQLite database via raw `sqlite3` connections.
- URL patterns `/vault/<int:building_pk>/trend-logs/` and `/vault/<int:building_pk>/objects/` are registered in `core/urls.py`.
- `trend_log.html` — filterable Trend Log list template extending `base2.html`.
- `objects.html` — split-panel Objects list/detail template extending `base2.html`.
- Both handle the no-database empty state correctly.

## Scope for the next coding round

**In scope:**
- `myportal/core/views.py` — add five Insight view stubs (login_required, render template with minimal static context).
- `myportal/core/urls.py` — add URL patterns under `/insight/`.
- `myportal/templates/core/insight_management.html` — new layout template.
- `myportal/templates/core/create_insight_report.html` — new layout template.
- `myportal/templates/core/manage_rules.html` — new layout template.
- `myportal/templates/core/golden_standard_configuration.html` — new layout template.
- `myportal/templates/core/insight_subscription.html` — new layout template.

**Out of scope for this round:**
- Any changes to `admin.py` files or `admin_custom.css`.
- Changes to `static/css/app.css` or `static/js/app.js`.
- New Django models or migrations.
- Real queryset-backed data or form POST handling.
- Refactoring of existing views, URLs, or forms.
- Buildings, Dashboard, Groups, Users, Clients, Profile, Vault pages.

## Starting point
- Review `base2.html` (used by `objects.html` and `trend_log.html`) and `base.html` for the correct shell to extend.
- Review `clients.html` and `users.html` for the list-view card + table pattern (for `insight_management.html`, `manage_rules.html`, `insight_subscription.html`).
- Review `user_detail.html` for the form card pattern (for `create_insight_report.html`).
- Review `objects.html` for the sub-navigation tab style used in the Vault section — the Insight section likely needs similar sub-nav tabs.
- Confirm the URL prefix to use (`/insight/`) and that it does not conflict with existing URL patterns in `core/urls.py`.

## Expected deliverables
1. Updated `core/views.py` with five Insight view stubs.
2. Updated `core/urls.py` with five new URL patterns under `/insight/`.
3. New `myportal/templates/core/insight_management.html`.
4. New `myportal/templates/core/create_insight_report.html`.
5. New `myportal/templates/core/manage_rules.html`.
6. New `myportal/templates/core/golden_standard_configuration.html`.
7. New `myportal/templates/core/insight_subscription.html`.

## Acceptance criteria
- All five pages render inside the shared BLENDY shell (navbar, breadcrumb, left panel) correctly.
- Static/sample data is used for all list rows and form field values — no real database queries required at this stage.
- Each page follows the correct visual pattern (list-view card+table or form card) consistent with existing pages.
- Sub-navigation tabs link between the five Insight pages, consistent with how Vault sub-nav links between `trend_log.html` and `objects.html`.
- URL patterns follow the convention `/insight/`, `/insight/create/`, `/insight/rules/`, `/insight/golden-standard/`, `/insight/subscriptions/`.
- No regressions in any existing pages.
- `app.css` and all admin files are untouched.
