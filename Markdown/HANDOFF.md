# HANDOFF

## Current status
The BLENDY Django project has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.
The Buildings pages (`buildings.html`, `building_detail.html`, `building_report.html`) are still layout-only or sample-data driven and are **deferred** to a later stage.
The Groups pages (`groups.html`, `group_detail.html`, `group_saved.html`, `group_members.html`) are **complete** — all four screens are queryset-backed, wired to real backend logic, and consistent with the shared BLENDY visual language.
The Users pages (`users.html`, `user_detail.html`) are **complete** — both screens are queryset-backed, wired to real backend logic (create, edit, group assignment, activate/deactivate), and consistent with the shared visual language.
The **`dashboard.html` functional review and update is now complete** — the page is fully connected to real queryset-backed data and live summary logic.
The next active implementation stage is the **sliding left panel function** in `base.html`.

## What is already done
- Custom auth model and login/logout flow are set up in the `accounts` app, and authenticated pages use the shared shell in `templates/base.html`.
- Shared authenticated shell is implemented in `templates/base.html` with breadcrumb bar, page title, top-left hamburger button, icon-based main navigation, and a sliding left panel showing a Client → Building tree.
- Groups pages are fully functional: `groups.html` is queryset-backed, `group_detail.html` handles create and edit flows with POST save and permission wiring, `group_saved.html` shows the confirmation screen with real group context, and `group_members.html` handles membership updates.
- Profile page save flow, avatar upload, and Django admin visibility are implemented.
- Clients pages are fully functional: `clients.html` is queryset-backed, `client_detail.html` shows real data with prefetched buildings and groups, and `client_saved.html` handles both create and edit flows with POST save and redirect on success.
- Users pages are fully functional: `users.html` is queryset-backed showing full name, email, work phone, group badges, and action buttons; `user_detail.html` handles both create and edit flows with POST save, validation feedback, group assignment, and activate/deactivate toggling.
- `dashboard.html` is now fully functional: connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip. Chart widgets are wired to context data.
- The sliding left panel in `base.html` renders the Client → Building hierarchy from queryset-backed context and remains consistent after write actions.
- Buildings pages exist as layout-only or sample-data screens; their full functional wiring is deferred.

## What is not yet done — current target
The **sliding left panel** in `base.html` needs its full interactive behaviour implemented. Currently the panel structure and data rendering exist, but the open/close animation, overlay, keyboard dismissal, and any nested expand/collapse of the Client → Building tree require JavaScript and CSS work.

Planned functional behaviour for the sliding left panel includes:
- **Open/close toggle** — hamburger button in the top bar triggers a smooth CSS slide-in/out animation for the panel.
- **Overlay backdrop** — a semi-transparent overlay appears behind the panel when open; clicking it closes the panel.
- **Keyboard dismissal** — pressing `Escape` closes the open panel.
- **Tree expand/collapse** — clients in the panel can be expanded or collapsed to show/hide their associated buildings.
- **Active state highlighting** — the currently visited page's building or client is visually highlighted in the tree.
- **Persistent state (optional)** — the panel's last open/closed state can be preserved across navigation using session or localStorage if desirable.

## Important implementation notes
- All JavaScript for the panel should live in `static/js/app.js` following the existing interaction patterns.
- CSS transitions and panel layout should live in `static/css/app.css`; reuse existing variable and class conventions.
- The panel HTML structure is already in `base.html` — only JS wiring and CSS transitions should change, not the panel's data rendering or context dependencies.
- The left panel depends on `sidebar_clients` and `sidebar_profile` context keys — these must continue to be supplied by every authenticated view's context.
- Do not introduce any new backend routes or view logic for the panel interaction — it is a pure frontend behaviour.
- Preserve the existing shared shell structure and all other authenticated page behaviour.

## Relevant files for the next session
- `templates/base.html` — panel HTML structure, hamburger button, overlay element
- `static/css/app.css` — panel slide animation, overlay styles, tree expand/collapse transitions
- `static/js/app.js` — open/close toggle, overlay click handler, Escape key handler, tree expand/collapse logic

## Next task
Work on the **sliding left panel function** in `base.html`.

This next step should include:
- Reviewing the current panel HTML structure in `base.html` and identifying what JS wiring and CSS is missing.
- Implementing the open/close animation using CSS `transform: translateX()` or equivalent.
- Adding the overlay backdrop element and click-to-close behaviour.
- Adding `Escape` key dismissal.
- Implementing tree expand/collapse for the Client → Building hierarchy in the panel.
- Highlighting the active page item in the tree.

## Constraints for the next edit
- Focus on the sliding left panel function only.
- Do not refactor unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard).
- Preserve the shared `base.html` data rendering and context dependencies.
- Keep CSS in `static/css/app.css` and all interaction logic in `static/js/app.js`.
- Return complete updated files for affected code when requesting AI help.

## Recommended next prompt
Use a prompt in this shape for the next coding session:

```text
Current task: implement the sliding left panel interactive function.
Constraints:
- keep current Django structure
- keep existing bulk style
- no unrelated refactor
- preserve existing base.html data rendering and context keys
- only touch panel-related CSS and JS unless a small shared update is required
Relevant files:
- templates/base.html
- static/css/app.css
- static/js/app.js
Please return complete updated files only.
```
