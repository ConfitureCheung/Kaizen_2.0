# HANDOFF

## Current status
The BLENDY Django project already has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.[file:53]
The project is in a layout-first stage: several pages are already built as HTML/CSS screens, while some backend actions remain scaffold-only or sample-data based.[file:53]

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app.[file:53]
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, and icon-based main navigation.[file:53]
- Users pages are already laid out with `users.html` and `user_detail.html`, and the Users nav active state handles both list and detail pages.[file:53]
- Clients pages are already laid out with list/detail/saved screens.[file:53]
- Buildings pages are already laid out with list/detail/report screens.[file:53]
- `groups_view` and the `/groups/` route already exist, and they already pass filtered `ClientGroup` data to the template layer.[file:53]

## Important implementation notes
- Use the existing shared page shell in `base.html`; do not create a separate standalone layout for Groups pages.[file:53]
- Keep styling inside the established `static/css/app.css` conventions instead of introducing a disconnected CSS approach.[file:53]
- Preserve the current project structure, naming style, and minimal-change workflow.[file:53][cite:1]
- The project currently mixes real queryset pages and static sample pages, so Groups should follow the same pragmatic approach: build the HTML accurately first, then wire more behavior later if needed.[file:53]

## Next task
Build the Groups-related HTML pages.

Likely next pieces:
- Finalize `templates/core/groups.html` list page.[file:53]
- Add a Group detail/add page if the UI flow needs it to match other modules.[file:53]
- Update nav active-state logic if a new Group detail route is added.[file:53]
- Add only the CSS needed for Groups pages in `static/css/app.css`.[file:53]

## Relevant files for the next session
- `core/views.py`.[file:53]
- `core/urls.py`.[file:53]
- `templates/base.html`.[file:53]
- `templates/core/groups.html`.[file:53]
- `static/css/app.css`.[file:53]
- Optional new Group detail template if introduced.

## Constraints for the next edit
- Focus on Groups only.
- Do not refactor unrelated modules.
- Preserve existing backend queryset logic unless a small Groups-specific adjustment is necessary.[file:53][cite:1]
- Keep the same bulky but organized project style and return complete updated files for affected code when requesting AI help.[cite:1]

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build Groups related HTML pages only.
Constraints:
- keep current Django structure
- keep existing bulky style
- no unrelated refactor
- preserve existing shared base.html shell
- only touch Groups-related files unless a small nav/CSS update is required
Relevant files:
- core/views.py
- core/urls.py
- templates/base.html
- templates/core/groups.html
- static/css/app.css
Please return complete updated files only.
```
