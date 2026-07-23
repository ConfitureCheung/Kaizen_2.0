# TASK

## Current task
Build the functional part of the Buildings pages: `buildings.html`, `building_detail.html`, and `building_report.html`.

## Immediate objective
Wire real backend functionality into the three Buildings-related screens that are currently layout-only or sample-data driven.

This should include:
- Queryset-backed building list in `buildings.html`, filtered by client ownership.
- Real building detail data in `building_detail.html` with working create and edit form handling (POST save, validation feedback, redirect on success).
- Working report view in `building_report.html` rendering real data-backed charts or stats tied to the building's sensor or energy records.
- Django admin registration for `Building` records if not already present.
- Left panel context kept consistent after any Building create/edit/delete action.

## Background from the previous step
The project already uses a shared authenticated shell in `templates/base.html`, including a sliding left panel that renders a Client → Building tree from queryset-backed context.
The Client pages functional work — queryset-backed list, detail view with prefetched buildings and groups, and create/edit form handling — has been completed.
The `Building` model and its foreign key relationship to `Client` already exist in `core/models.py`.
The three Buildings template files and their URL routes already exist; only the view logic and template data-binding need to be made functional.

## Scope for the next coding round

**In scope:**
- `templates/core/buildings.html`
- `templates/core/building_detail.html`
- `templates/core/building_report.html`
- `core/views.py` — add or update `buildings_view`, `building_detail_view`, `building_report_view`
- `core/urls.py` — verify or update routes for `buildings`, `building_detail`, `building_report`
- `core/models.py` — reference only; add a small nullable field only if strictly necessary
- `core/admin.py` — register `Building` if not already done
- Small related updates to `static/css/app.css` and `static/js/app.js` only if required to support form behavior, chart rendering, or list interactivity

**Out of scope for this round:**
- Refactoring unrelated modules (Users, Groups, Clients, Profile).
- Replacing or redesigning the shared `base.html` shell or left panel.
- Broad permission-system changes.
- Redesigning the `Building` data model.
- Unrelated styling cleanup.

## Starting point
- `buildings_view`, `building_detail_view`, and `building_report_view` may already exist in `core/views.py` in a stub or layout-rendering form — confirm before writing from scratch.
- The project already has established CSS patterns for forms, cards, tables, save buttons, map placeholders, and chart wrappers that should be reused rather than replaced.
- The left panel in `base.html` already depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by the view context or a shared context processor.

## Expected deliverables
1. `buildings.html` renders a real queryset-backed list of `Building` records, scoped to accessible clients.
2. `building_detail.html` handles both create and edit flows: GET renders the form, POST validates and saves, success redirects to `building_report` or `buildings`.
3. `building_report.html` renders a single building's report with real data — at minimum showing building info and one or more charts or stat panels sourced from the database.
4. Django admin shows `Building` records.
5. Left panel stays consistent after any building write action.
6. No unrelated architecture refactor.

## Acceptance criteria
- A new `Building` record can be created through the `building_detail.html` form and appears immediately in the `buildings.html` list and in the left panel tree.
- An existing `Building` record can be edited through the same form and changes are persisted.
- `building_report.html` correctly shows the building's data from the database with at least one real chart or stat panel.
- Saved building data is visible in the Django admin panel.
- The implementation fits the existing BLENDY visual language and shared shell structure.
- Changes remain targeted and do not disturb unrelated modules.
