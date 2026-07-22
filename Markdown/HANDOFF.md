# HANDOFF

## Current status
The BLENDY Django project already has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.[cite:8][cite:17]
The project is still in a layout-first stage: several pages are already built as HTML/CSS screens, while some backend actions remain scaffold-only or sample-data based.[cite:16][cite:20]
Groups UI is now no longer just a placeholder list page; it includes a Groups list screen, an add/edit-style screen, a saved/detail-style screen, and a select-members screen aligned to the existing BLENDY page shell approach.[cite:10][cite:11][cite:20]

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.[cite:8][cite:10]
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, and icon-based main navigation.[cite:10]
- Users pages are already laid out with `users.html` and `user_detail.html`, and the Users nav active state already handles both list and detail pages.[cite:11][cite:12]
- Clients pages are already laid out with list/detail/saved screens.[cite:11][cite:13]
- Buildings pages are already laid out with list/detail/report screens.[cite:11][cite:16]
- `groups_view` and the `/groups/` route already exist, and they already pass filtered `ClientGroup` data to the template layer.[cite:16][cite:17]
- The Groups area has now been expanded conceptually to include these templates: `groups.html`, `group_detail.html`, `group_saved.html`, and `group_members.html`.[cite:11]
- The Groups nav item should remain highlighted for all Groups-related pages, not only the `/groups/` list route, so the `base.html` active-state logic should include `group_detail`, `group_saved`, and `group_members` as well as `groups`.[cite:10]
- A UX improvement has been identified for `/groups/add/`: when no client exists yet, the page should show a friendly warning and guidance to create a client first, instead of raising a database integrity error caused by `ClientGroup.client` being required.[cite:15][cite:21]

## Important implementation notes
- Use the existing shared page shell in `base.html`; do not create a separate standalone layout for Groups pages.[cite:10]
- Keep styling inside the established `static/css/app.css` conventions instead of introducing a disconnected CSS approach.[cite:20]
- Preserve the current project structure, naming style, and minimal-change workflow.[cite:8][cite:10]
- The project currently mixes real queryset pages and static sample pages, so Groups should continue following the same pragmatic approach: build the HTML accurately first, then wire more behavior later if needed.[cite:16][cite:20]
- `ClientGroup` has a required foreign key to `Client`, and `Building` also belongs to `Client`; this matters for both error handling and the next navigation-tree feature.[cite:15]

## What changed in the Groups flow
- Groups should follow the same visual language as Users and Buildings: a top-right action button, a main card with table rows, row-level icon actions, and shared button classes such as `primary-action-btn`, `icon-btn`, `primary-btn`, and `secondary-btn`.[cite:12][cite:20]
- The Groups flow now includes a detail/add form with a group name field, broad permission toggles, and page-level permission rows to match the provided layout references.[cite:20]
- The saved/detail screen should include a success banner, action buttons for editing and selecting members, a permissions summary area, and a members table.[cite:20]
- The select-members screen should show available users in a table with checkboxes and save/cancel actions.[cite:12][cite:20]
- If no client is available for the current user, the add-group page should render a warning banner with a link or instruction to create a client first instead of attempting to save and crashing.[cite:15][cite:21]

## Next task
Build the sliding left panel triggered by the top-left hamburger button in the shared header.[cite:10]
When clicked, it should open a left-side panel showing a structure tree. The planned structure is:
- Profile as top tier.
- Client as second tier.
- Under each client, show the corresponding buildings as third tier.[cite:15]

## Recommended interpretation for the tree
Because `Building` belongs to `Client`, and `Profile` currently exists as a standalone page route, the cleanest implementation is a navigation tree where Profile is a root-level navigation item and Clients form an expandable branch containing their buildings.[cite:15][cite:17]
If the visual requirement is to show Profile as the single top-tier root for the whole tree, treat that as a navigation wrapper rather than a data-model parent-child relationship.[cite:15][cite:17]

## Likely next pieces
- Add sidebar markup container into `templates/base.html` near the existing topbar and page shell.[cite:10]
- Extend `static/css/app.css` with left-panel layout, overlay, slide animation, nested tree styles, and compact responsive behavior.[cite:20]
- Update `static/js/app.js` so the hamburger button opens and closes the panel.[cite:10][cite:18]
- Add queryset/context support so the panel can render accessible clients and their buildings for the logged-in user.[cite:15][cite:16]
- Keep the current page routes intact; the sidebar should be additive rather than a refactor of the top icon navigation.[cite:10][cite:17]

## Relevant files for the next session
- `core/views.py`.[cite:14][cite:16]
- `core/urls.py`.[cite:16][cite:17]
- `templates/base.html`.[cite:9][cite:10]
- `templates/core/groups.html`.[cite:11]
- `templates/core/group_detail.html`.
- `templates/core/group_saved.html`.
- `templates/core/group_members.html`.
- `static/css/app.css`.[cite:19][cite:20]
- `static/js/app.js`.[cite:18]

## Constraints for the next edit
- Keep the edit focused on the shared left panel and the minimum related wiring required to support it.[cite:10][cite:20]
- Do not refactor unrelated modules.[cite:16]
- Preserve existing backend queryset logic unless a small sidebar-specific adjustment is necessary.[cite:16]
- Keep the same bulky but organized project style and return complete updated files for affected code when requesting AI help.[cite:8][cite:10]
- Preserve the existing top icon navigation unless there is a deliberate decision later to replace it.[cite:10]

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the sliding left panel from the top-left hamburger button.
Constraints:
- keep current Django structure
- keep existing bulky style
- no unrelated refactor
- preserve existing shared base.html shell
- keep current top icon navigation
- only touch sidebar-related files unless a small queryset/nav/CSS/JS update is required
Relevant files:
- templates/base.html
- static/css/app.css
- static/js/app.js
- core/views.py
Please return complete updated files only.
```
