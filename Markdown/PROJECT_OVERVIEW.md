# PROJECT OVERVIEW

## Current status
The BLENDY Django project already has its main structure in place, including the `accounts` and `core` apps, shared templates, authentication flow, and page routes for dashboard, users, groups, buildings, clients, and profile.[cite:8][cite:17]
The project remains layout-first: some pages are backed by real querysets while other pages still use sample or scaffold data, which is an intentional pattern in the current codebase.[cite:16][cite:20]
The Groups module has moved beyond a placeholder route and should now be treated as a multi-screen flow under the existing shared layout conventions.[cite:11][cite:20]

## Existing application structure
- `templates/base.html` provides the authenticated shell, including the top bar, hamburger button, breadcrumb bar, page title area, and icon-based navigation.[cite:10]
- `core/views.py` currently contains queryset-backed list pages for users, groups, and clients, plus sample-data-backed building screens.[cite:16]
- `core/urls.py` defines named routes for users, groups, buildings, clients, and profile.[cite:17]
- `static/css/app.css` contains the shared visual language for cards, forms, tables, banners, nav icons, buttons, and responsive adjustments.[cite:20]
- The data model already supports the future sidebar hierarchy because `ClientGroup` belongs to `Client`, `Building` belongs to `Client`, and `BuildingUser` can be associated to both groups and buildings.[cite:15]

## Groups module status
The Groups area should now be understood as a four-screen flow:
1. Groups list page.
2. Group add/edit page.
3. Group saved/detail page.
4. Group member-selection page.[cite:11]

These screens should keep the Groups icon highlighted in the shared icon navigation by extending the Groups active-state check in `base.html` to cover all Groups-related route names, not only `groups`.[cite:10]
The Groups add page also needs a defensive UX path: when no accessible client exists, it should show a warning banner that tells the user to create a client first instead of triggering a server error from the required `client_id` field.[cite:15][cite:21]

## Styling and UI approach
- Continue using the existing BLENDY visual language already seen in Users, Clients, and Buildings pages, including `content-card`, `section-head`, `primary-action-btn`, `icon-btn`, `primary-btn`, and `secondary-btn` patterns.[cite:12][cite:13][cite:20]
- Keep all Groups-related visual additions in `static/css/app.css` rather than introducing a new styling system.[cite:20]
- Stay with the current pragmatic pattern: accurate layout first, behavior second, with only minimal backend wiring needed to support the screens.[cite:16][cite:20]

## Next planned feature
The next step is a sliding left panel opened by the hamburger button in the shared top bar.[cite:10]
The panel is intended to show a structure tree with these tiers:
- Top tier: Profile.
- Second tier: Client.
- Third tier: Buildings under each client.[cite:15]

Because the actual model relationship is `Client -> Building`, the tree should be implemented as navigation hierarchy rather than implying a database parent-child link from Profile to Client.[cite:15][cite:17]

## Files most relevant for the next step
- `templates/base.html` for adding sidebar markup and preserving the shared shell.[cite:10]
- `static/css/app.css` for slide-in panel styles, overlay behavior, nested tree styling, and responsive handling.[cite:20]
- `static/js/app.js` for hamburger interaction and panel toggle behavior.[cite:18]
- `core/views.py` for providing accessible client/building tree data to templates if needed.[cite:16]

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.[cite:8][cite:17]
- Reuse current patterns before inventing new abstractions.[cite:10][cite:20]
- When using AI help, ask for complete updated files for the touched files only.[cite:8]
