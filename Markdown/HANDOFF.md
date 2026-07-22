# HANDOFF

## Current status
The BLENDY Django project already has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.[cite:8][cite:17]
The project remains in a pragmatic layout-first stage: some pages already use real querysets while others still use static or sample-data rendering patterns, and that mixed approach is intentional in the current codebase.[cite:16][cite:20]
The shared layout has now been expanded conceptually to support a global sliding left panel triggered from the hamburger button in `base.html`, so navigation behavior is no longer limited to the top icon row alone.[cite:10]

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.[cite:8][cite:10]
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, and icon-based main navigation.[cite:10]
- Users pages are already laid out with `users.html` and `user_detail.html`, and the Users nav active state handles both list and detail pages.[cite:11][cite:12]
- Clients pages are already laid out with list/detail/saved screens.[cite:11][cite:13]
- Buildings pages are already laid out with list/detail/report screens.[cite:11][cite:16]
- The Groups area has already been extended beyond the original placeholder state into a list/detail/member-selection style flow aligned with the shared BLENDY page shell and CSS conventions.[cite:11][cite:20]
- A defensive UX requirement has been identified for `/groups/add/`: when no client exists, the page should show a friendly warning instead of raising a database integrity error, because `ClientGroup.client` is required.[cite:15][cite:21]
- The next navigation layer has now been defined: a left-side sliding panel should be available from any page that contains the hamburger icon in the shared layout.[cite:10]

## Sliding left panel scope and behavior
The left panel is intended to be implemented in the shared layout so it can be opened from any page that extends `base.html`.[cite:10]
It should use the current data relationships to show a structure tree with:
- Profile as the top tier.
- Clients as the second tier.
- Buildings under each client as the third tier.[cite:15]

The panel should support an empty state when there are no records yet, so the UI can be built now without requiring profile, client, or building records to exist first.[cite:15][cite:16]
Once records are created later, the panel should update from queryset-backed context rather than needing a redesign.[cite:15][cite:16]
The panel should also close when the user clicks outside it or clicks page-navigation items that redirect elsewhere, so it behaves cleanly across all pages using the shared shell.[cite:10]

## Important implementation notes
- Use the existing shared page shell in `base.html`; do not create a separate standalone layout system for the left panel.[cite:10]
- Keep styling inside the established `static/css/app.css` conventions instead of introducing a disconnected CSS approach.[cite:20]
- Keep interactivity inside the existing `static/js/app.js` file rather than spreading panel behavior across page-specific scripts.[cite:18]
- Preserve the current project structure, naming style, and minimal-change workflow.[cite:8][cite:10]
- `ClientGroup` and `Building` both relate to `Client`, which is important for tree rendering and for keeping the panel data-driven once records exist.[cite:15]

## Relevant files for the next session
- `templates/base.html`.[cite:9][cite:10]
- `static/css/app.css`.[cite:19][cite:20]
- `static/js/app.js`.[cite:18]
- `core/views.py`.[cite:14][cite:16]
- `core/urls.py`.[cite:17]
- `accounts/profile.html`.
- Any account/profile model or admin file used to persist profile data.

## Next task
Work on the functional part of the Profile page.

This next step should include:
- Saving profile information from the Profile page form into the backend instead of leaving it as layout-only.[cite:10][cite:20]
- Supporting avatar image upload on the Profile page.[cite:20]
- Making the saved profile data correspond properly with the backend admin page so records are visible and manageable there.[cite:8][cite:14]
- Using relevant saved profile data for display in the left panel once that panel is wired in full, especially the top-tier Profile section and any avatar/name display needed there.[cite:10]

## Constraints for the next edit
- Focus on Profile functionality only.
- Do not refactor unrelated modules.
- Preserve the shared `base.html` shell and the new left-panel concept.[cite:10]
- Keep CSS in `static/css/app.css` and shared interaction logic in `static/js/app.js` unless a backend-specific addition is necessary.[cite:18][cite:20]
- Keep the same bulky but organized project style and return complete updated files for affected code when requesting AI help.[cite:8][cite:10]

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: build the functional part of the Profile page.
Constraints:
- keep current Django structure
- keep existing bulky style
- no unrelated refactor
- preserve existing shared base.html shell and left panel concept
- only touch profile-related files unless a small shared CSS/JS/admin/model update is required
Relevant files:
- accounts/profile.html
- core/views.py or accounts views file used by profile route
- related models.py
- related admin.py
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
