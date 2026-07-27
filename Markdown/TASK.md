# TASK

## Current task
Review and update the functional part of `dashboard.html`.

## Immediate objective
Connect `dashboard.html` to real queryset-backed data and replace all sample/placeholder content with live template variables. The dashboard is the first screen a logged-in user sees, so it should surface the most useful at-a-glance information about the current state of the system.

This should include:
- Summary KPI cards showing live counts (active users, clients, buildings, groups).
- A recent activity feed showing the most recently created or updated records across key models.
- A Client → Building overview table or card list, consistent with the left panel hierarchy.
- An insight/alert strip surfacing flagged conditions (e.g. users with no group, buildings with no client assignment).
- Chart widgets wired to real data if chart infrastructure is already present in the project.

## Background from the previous step
The Users pages work is now complete:
- `users.html` is queryset-backed and shows full name, email, work phone, group badges, and action buttons.
- `user_detail.html` handles both create and edit flows with POST save, validation, group assignment, and activate/deactivate toggling.
- Django admin registration for the custom user model is in place.

The project already uses a shared authenticated shell in `templates/base.html`, including a sliding left panel that renders a Client → Building tree from queryset-backed context.
The Groups, Clients, and Users pages functional work has been completed and can be used as reference patterns for view context structure and template variable usage.
The CSS classes for common patterns (cards, tables, forms, banners, save buttons, action columns) are already defined in `static/css/app.css`.

## Scope for the next coding round

**In scope:**
- `templates/core/dashboard.html`
- `core/views.py` — update `dashboard_view` to supply real queryset context (KPI counts, recent records, alert flags, chart data)
- `core/urls.py` — verify route for `dashboard`
- Small related updates to `static/css/app.css` only if dashboard-specific layout classes are missing
- Small related updates to `static/js/app.js` only if chart initialisation or dashboard interactivity is needed

**Out of scope for this round:**
- Refactoring unrelated modules (Groups, Buildings, Clients, Profile, Users).
- Replacing or redesigning the shared `base.html` shell or left panel.
- Redesigning the data model.
- Unrelated styling cleanup.
- Functional wiring of Buildings pages (deferred).

## Starting point
- `dashboard_view` may already exist in `core/views.py` in a stub or layout-rendering form — confirm before writing from scratch.
- The project already has established CSS patterns for cards, tables, banners, and action columns that should be reused rather than replaced.
- The left panel in `base.html` depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by the updated `dashboard_view`.
- Check whether a chart library (e.g. Chart.js) is already loaded in `base.html` or `app.js` before adding new script references.

## Expected deliverables
1. `dashboard.html` renders live KPI counts sourced from real querysets.
2. `dashboard.html` shows a recent activity feed with actual record data.
3. `dashboard.html` shows a Client → Building summary consistent with the left panel.
4. `dashboard.html` displays an alert/insight strip for any flagged system conditions.
5. Any chart widgets are wired to data passed from `dashboard_view` context.
6. No unrelated architecture refactor.

## Acceptance criteria
- KPI card numbers update immediately when records are added or removed in the system.
- Recent activity feed shows real records, not hardcoded sample data.
- Alert strip shows only real flagged conditions; disappears when there are none.
- Charts (if present) render from context data, not hardcoded arrays.
- The implementation fits the existing BLENDY visual language and shared shell structure.
- Changes remain targeted and do not disturb unrelated modules.
