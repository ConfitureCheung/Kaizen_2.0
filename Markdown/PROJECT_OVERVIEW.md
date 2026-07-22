# PROJECT OVERVIEW

## Current status
The BLENDY Django project already includes the `accounts` and `core` apps, shared authenticated templates, route wiring for dashboard, users, groups, buildings, clients, and profile, and a common visual system in `static/css/app.css`.[cite:8][cite:10][cite:17][cite:20]
The project is still intentionally hybrid: some screens are queryset-backed and some remain layout-first or sample-data driven while interface work progresses in stages.[cite:16][cite:20]
The shared navigation model has now expanded beyond the icon row to include a planned sliding left panel triggered from the hamburger button in the authenticated shell.[cite:10]

## Existing structure relevant to the next step
- `templates/base.html` contains the top bar, hamburger button, breadcrumb bar, page title, and global icon navigation shared across authenticated pages.[cite:10]
- `core/views.py` already contains helper logic for allowed clients and queryset-backed pages that can be reused to provide shared navigation context.[cite:16]
- `core/urls.py` already defines the main application page routes that the shared shell depends on.[cite:17]
- `static/css/app.css` already defines the app’s visual language for cards, forms, banners, tables, buttons, and responsive behavior.[cite:20]
- The data model already supports a client/building hierarchy because `Building` has a foreign key to `Client`, and related group/building-user relationships also already exist.[cite:15]

## Groups and navigation state
The Groups area should now be treated as a multi-screen flow rather than a single placeholder list page, and the Groups icon should remain highlighted across all Groups-related routes in the shared navigation.[cite:10][cite:11]
The add-group flow also needs a defensive UX path when no client exists yet, because `ClientGroup.client` is required and should not be allowed to fail as a raw integrity error in front of users.[cite:15][cite:21]

## Sliding left panel direction
The hamburger-triggered left panel should be implemented in the shared authenticated shell so it can appear on any page that includes the hamburger control.[cite:10]
The intended tree structure is:
- Profile as top tier.
- Client as second tier.
- Buildings under each client as third tier.[cite:15]

The tree should render cleanly even when no profile/client/building records exist yet, using an empty state initially and queryset-backed data later as records are created.[cite:15][cite:16]
The panel should also close when the user clicks outside it or chooses page navigation elsewhere, so it behaves consistently across routes.[cite:10]

## Next planned feature
The next concrete implementation task is the functional part of the Profile page.
This work should cover:
- saving profile information,
- avatar image upload,
- persistence visible from the backend admin page,
- and using saved profile information later in the left panel display.[cite:10][cite:20]

## Files most relevant for the next step
- `accounts/profile.html` for the profile form UI.
- The view file currently responsible for the profile page route, which is presently exposed through `profile_view` in `core/views.py`.[cite:16][cite:17]
- The model file that should store profile metadata or avatar fields.[cite:14][cite:15]
- The relevant admin configuration so the saved profile data is visible in Django admin.[cite:14]
- `templates/base.html` if the left panel starts showing live profile information.[cite:10]
- `static/css/app.css` and `static/js/app.js` for any shared styling or upload/panel behavior support.[cite:18][cite:20]

## Project guardrails
- Keep changes targeted.
- Avoid unrelated refactors.
- Preserve the current Django structure and naming style.[cite:8][cite:17]
- Reuse the shared shell and CSS language already present in the project.[cite:10][cite:20]
- Ask for complete updated files for touched files only when using AI help.[cite:8]
