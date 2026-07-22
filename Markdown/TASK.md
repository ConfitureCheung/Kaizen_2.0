# TASK

## Current task
Build the Groups-related HTML pages for the BLENDY Django project using the current shared layout and styling approach.[file:53]

## Objective
Create or refine the Groups UI so it matches the existing pattern already used for Users, Clients, and Buildings pages: a shared `base.html` shell, a top-right page action button, a main content card, and layout/styling controlled primarily from `static/css/app.css`.[file:53]

## Scope
This task is currently frontend/layout focused.

In scope:
- `templates/core/groups.html`.[file:53]
- Any new Group detail/add template if needed to support the same flow used on Users, Clients, and Buildings pages.[file:53]
- Small related updates to `core/urls.py`, `core/views.py`, `templates/base.html`, and `static/css/app.css` only if required to support Groups page navigation and layout.[file:53]

Out of scope for this round:
- Full create/edit/delete backend logic.
- Model refactors.
- Permission redesign.
- Unrelated restyling of Users, Buildings, Clients, Dashboard, or Profile pages.

## Starting point
- `groups_view` already exists in `core/views.py` and passes filtered `ClientGroup` queryset data into `core/groups.html`.[file:53]
- `core/urls.py` already includes `path("groups/", views.groups_view, name="groups")`.[file:53]
- `base.html` already includes a Groups nav item and active-state logic for `groups`.[file:53]
- The current codebase already has good visual references in `users.html`, `user_detail.html`, `buildings.html`, and `client_detail.html` for table layouts, add-page layouts, action buttons, and form spacing.[file:53]

## Expected deliverables
1. A polished `groups.html` page aligned with existing BLENDY page patterns.[file:53]
2. If needed, a matching Group add/detail page template following the same UI language as existing add pages.[file:53]
3. Only the minimum related updates needed in URLs, views, nav highlighting, and CSS.[file:53]
4. No fake extra architecture changes outside the Groups flow.

## UI guidance
- Keep Groups nav visually consistent with the existing icon-nav system in `base.html`.[file:53]
- Reuse existing button patterns such as `primary-action-btn`, `save-btn`, `cancel-btn`, `icon-btn`, and content-card/table structures where appropriate.[file:53]
- Follow the same static-first / layout-first approach already used across the project.[file:53]
- Prefer table layout for list view if the Groups page is analogous to Users and Buildings.[file:53]
- Keep responsive behavior aligned with the existing CSS pattern, including horizontal scroll on tables for narrower widths when needed.[file:53]

## Suggested relevant files for next AI enquiry
- `core/views.py`
- `core/urls.py`
- `templates/base.html`
- `templates/core/groups.html`
- `static/css/app.css`
- Any new file such as `templates/core/group_detail.html` if created

## Acceptance criteria
- Groups page renders under the current authenticated shell without breaking existing pages.[file:53]
- Groups-related pages use the BLENDY visual language already established in the project.[file:53]
- Navigation highlighting is correct for all Groups-related pages after the update.[file:53]
- Changes stay targeted and do not introduce unrelated refactoring.[cite:1]
