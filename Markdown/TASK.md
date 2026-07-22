# TASK

## Current task
Update the project direction so the next coding step focuses on the functional part of the Profile page while keeping the new shared left-panel concept in view.[cite:10]

## Immediate objective
Implement real Profile-page behavior instead of layout-only behavior.
This should include:
- saving profile information,
- uploading an avatar image,
- syncing or corresponding properly with the backend admin page,
- and preparing the saved data for display in the left panel later.[cite:10][cite:20]

## Background from the previous step
The project already uses a shared authenticated shell in `templates/base.html`, including the hamburger button that is intended to open a sliding left panel.[cite:10]
That left panel is planned to show a tree with Profile at the top tier, Clients at the second tier, and Buildings under each client at the third tier, based on the existing data relationships in the models.[cite:15]
The left panel should work even before records exist by showing an empty state, and later update automatically when records are created.[cite:15][cite:16]

## Scope for the next coding round
In scope:
- `accounts/profile.html`.
- The view used by the profile route, currently `profile_view`.[cite:16][cite:17]
- The relevant model(s) needed to store profile fields and avatar data.[cite:14][cite:15]
- The relevant `admin.py` configuration so profile records and uploaded image fields can be viewed and managed in Django admin.[cite:14]
- Small related updates to `templates/base.html`, `static/css/app.css`, and `static/js/app.js` only if required to support avatar display or shared behavior.[cite:10][cite:18][cite:20]

Out of scope for the next round:
- Refactoring unrelated modules.
- Replacing the existing top icon navigation.
- Redesigning the client/building data model.
- Broad permission-system changes.
- Unrelated styling cleanup.[cite:15][cite:17]

## Starting point
- `profile_view` already exists and currently renders the profile page through the shared shell, but it is still non-functional from a save/persistence point of view.[cite:16]
- The project already has established CSS patterns for forms, file-upload placeholders, cards, and save buttons that should be reused rather than replaced.[cite:20]
- The authenticated shell and planned left panel mean profile data should be treated as shared application data, not just isolated form content.[cite:10]

## Expected deliverables for the next coding step
1. A working profile save flow.
2. Avatar image upload support.
3. Django admin visibility and manageability for the saved profile data.
4. The minimum shared-layout updates needed so profile data can later appear in the left panel or shared header if required.[cite:10]
5. No unrelated architecture refactor.

## Acceptance criteria
- Profile information can be saved successfully through the Profile page.
- Avatar upload works and persists correctly.
- Saved profile data is visible in the backend admin page.
- The implementation fits the existing BLENDY visual language and shared shell structure.[cite:10][cite:20]
- Changes remain targeted and do not disturb unrelated modules.[cite:16]
