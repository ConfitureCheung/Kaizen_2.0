# TASK

## Current task
Implement the **sliding left panel** interactive function in `base.html`.

## Immediate objective
Wire up the full interactive behaviour for the existing sliding left panel in `base.html`. The panel HTML structure and Client → Building data rendering are already in place — this task is purely frontend: CSS animation, JavaScript event handling, and tree expand/collapse behaviour.

This should include:
- Open/close toggle triggered by the hamburger button using a smooth CSS `transform: translateX()` slide animation.
- A semi-transparent overlay backdrop that appears when the panel is open and closes the panel on click.
- Keyboard dismissal — pressing `Escape` closes the open panel.
- Tree expand/collapse for the Client → Building hierarchy inside the panel.
- Active state highlighting for the currently visited page's item in the tree.
- (Optional) Persistent panel open/closed state across navigation.

## Background from the previous step
The Dashboard functional update is now complete:
- `dashboard.html` is connected to real queryset-backed KPI counts, recent activity feed, Client → Building summary, and alert/insight strip.
- Chart widgets are wired to context data passed from `dashboard_view`.
- No sample/placeholder data remains in the dashboard.

The project already uses a shared authenticated shell in `templates/base.html`, including the sliding left panel HTML structure and Client → Building tree rendering from `sidebar_clients` context.
All CSS conventions live in `static/css/app.css` and all shared interaction logic lives in `static/js/app.js`.

## Scope for the next coding round

**In scope:**
- `templates/base.html` — add overlay element if not present; verify panel and hamburger button IDs/classes.
- `static/css/app.css` — add panel slide-in/out transition, overlay styles, and tree expand/collapse transitions.
- `static/js/app.js` — add open/close toggle logic, overlay click handler, Escape key handler, and tree expand/collapse logic.

**Out of scope for this round:**
- Refactoring unrelated modules (Groups, Buildings, Clients, Profile, Users, Dashboard).
- Adding new backend routes or view logic.
- Redesigning the data model.
- Functional wiring of Buildings pages (deferred).
- Unrelated styling cleanup.

## Starting point
- The panel HTML and Client → Building tree already exist in `base.html` — do not re-render or restructure the data layer.
- The `sidebar_clients` and `sidebar_profile` context keys must continue to be supplied by every authenticated view; do not remove or rename them.
- Check existing IDs and class names in `base.html` for the hamburger button and panel wrapper before writing JS selectors.
- Check `static/js/app.js` for any existing partial panel logic before adding new handlers.
- Check `static/css/app.css` for any existing panel positioning or transition rules before adding new ones.

## Expected deliverables
1. Hamburger button toggles the panel open and closed with a smooth CSS slide animation.
2. An overlay backdrop appears behind the open panel and closes it on click.
3. Pressing `Escape` closes the panel.
4. Client rows in the panel expand and collapse to show/hide their buildings.
5. The active page item in the tree is visually highlighted.
6. No unrelated architecture refactor.

## Acceptance criteria
- Panel slides in and out smoothly without layout shift on the main content area.
- Overlay appears and disappears in sync with the panel.
- All three close triggers (hamburger re-click, overlay click, Escape key) work correctly.
- Tree expand/collapse works for all client rows and their buildings.
- Active highlighting correctly reflects the current page.
- Changes remain targeted and do not disturb unrelated modules.
