# TASK

## Current task
Update project documentation so it reflects the completed Groups-related UI work and captures the next feature: a sliding left panel opened from the hamburger button.[cite:10][cite:11]

## Immediate objective
Document the current Groups flow accurately and prepare the next coding step for the shared sidebar/tree navigation feature.[cite:10][cite:15]

## Newly completed / clarified Groups scope
The Groups work should now be documented as including:
- `templates/core/groups.html` as the list page.[cite:11]
- A Group add/detail template following the same shared shell and bulky form style used elsewhere in the project.[cite:10][cite:20]
- A Group saved/detail template with success messaging, permissions summary, and members list.[cite:20]
- A Group member-selection template using a checkbox table of available users.[cite:12][cite:20]
- A Groups nav active-state update so the Groups icon stays yellow across all Groups-related pages in the shared navigation.[cite:10]
- A UX safeguard for `/groups/add/` so users see a warning if no client exists yet instead of hitting a server error caused by the required `ClientGroup.client` foreign key.[cite:15][cite:21]

## Next implementation task
Build the shared sliding left panel triggered by the top-left hamburger button in `templates/base.html`.[cite:10]
When opened, it should show a structure tree with:
- Profile as top tier.
- Client as second tier.
- Buildings under each client as third tier.[cite:15]

## Scope for the next coding round
In scope:
- `templates/base.html` for the sidebar container, overlay, and tree markup.[cite:10]
- `static/css/app.css` for sidebar positioning, open/close transition, nested tree styling, and responsive behavior.[cite:20]
- `static/js/app.js` for hamburger toggle behavior and panel dismissal.[cite:18]
- Small related `core/views.py` adjustments only if template context is required to provide the client/building tree.[cite:16]

Out of scope for the next round:
- Refactoring unrelated modules.
- Replacing the existing top icon navigation.
- Model redesign.
- Permission-system redesign.
- Full CRUD cleanup beyond the sidebar task.[cite:15][cite:17]

## Starting point for the next session
- `base.html` already includes the hamburger button and the shared authenticated shell, so the sidebar should grow from that existing structure rather than introducing a separate layout system.[cite:10]
- `app.css` already contains the button, nav, card, table, and banner styles that the sidebar should visually harmonize with.[cite:20]
- `core/views.py` already contains helper logic for filtering accessible clients and querysets for buildings, which can be reused or minimally extended for the navigation tree.[cite:16]
- The data model already supports rendering a client-to-buildings hierarchy because `Building` has a foreign key to `Client`.[cite:15]

## Expected deliverables for the next coding step
1. A sliding left panel connected to the existing hamburger button.[cite:10]
2. A tree view that presents Profile, Clients, and Buildings in the required hierarchy.[cite:15]
3. Only the minimum related HTML, CSS, JS, and context updates needed to support the feature.[cite:10][cite:16][cite:20]
4. No unrelated architecture or styling refactor.

## Acceptance criteria
- The sidebar opens and closes from the existing hamburger button without breaking the current shared shell.[cite:10]
- The navigation tree displays clients and their buildings in a structure that matches the existing data relationships.[cite:15]
- The feature fits the BLENDY visual language already established in `app.css`.[cite:20]
- Changes remain targeted and do not disturb unrelated modules.[cite:16]
