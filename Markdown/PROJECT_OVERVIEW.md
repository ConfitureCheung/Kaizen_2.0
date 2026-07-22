# PROJECT_OVERVIEW

## Project summary
BLENDY Analytics is a Python/Django/PostgreSQL web application with a custom `accounts` app and a `core` app for tenant-style operational pages including dashboard, users, groups, buildings, clients, and profile.[file:53]
The current codebase is structured as a standard Django project named `myportal` with `config`, `accounts`, `core`, shared templates, and shared static assets in `static/css/app.css` and `static/js/app.js`.[file:53]

## Tech stack
- Backend: Django with PostgreSQL configured through `psycopg2-binary` and environment variables loaded by `python-dotenv`.[file:53]
- Database: PostgreSQL as the default Django database engine in `config/settings.py`.[file:53]
- Frontend: Django templates, shared `base.html`, Font Awesome icons, custom CSS, and small vanilla JS helpers.[file:53]
- Auth: Custom `accounts.User` model extending `AbstractUser`, with login/logout handled in the `accounts` app.[file:53]

## App structure
### `accounts`
- Owns the custom user model `User` with `is_provider` and `is_client_user` flags.[file:53]
- Contains `ProviderProfile` for provider-side company details.[file:53]
- Exposes login/logout routes in `accounts/urls.py` and custom login/logout views in `accounts/views.py`.[file:53]

### `core`
- Owns tenant/business models including `DatabaseConnection`, `Client`, `ClientMembership`, `ClientGroup`, `Building`, and `BuildingUser`.[file:53]
- Contains the main authenticated pages and route handlers for dashboard, users, groups, buildings, clients, and profile.[file:53]
- Uses `get_allowed_client_ids(user)` to scope visible data for non-provider/non-staff users.[file:53]

## Current pages
Implemented or scaffolded templates currently include:
- `dashboard.html`.[file:53]
- `accounts/login.html` and `accounts/profile.html`.[file:53]
- `core/users.html` and `core/user_detail.html`.[file:53]
- `core/groups.html` scaffold reference exists in project tree and routes, but the Groups page is the next active UI task.[file:53]
- `core/buildings.html`, `core/building_detail.html`, and `core/building_report.html`.[file:53]
- `core/clients.html`, `core/client_detail.html`, and `core/client_saved.html`.[file:53]

## Navigation and layout rules
- Shared navigation lives in `templates/base.html`.[file:53]
- The top icon navigation includes Dashboard, Users, Groups, Buildings, Clients, and Profile, with active-state logic based on `request.resolver_match.url_name`.[file:53]
- Users-related pages already use active-state handling for `users` and `user_detail`; Groups currently has active-state handling for `groups` only.[file:53]
- Shared visual styling is centralized in `static/css/app.css`, so new HTML pages should reuse existing classes and naming patterns where possible.[file:53]

## Data and permission model
- `ClientMembership` connects a Django auth user to a client with role choices `admin`, `editor`, and `viewer`.[file:53]
- `ClientGroup` belongs to a `Client` and is unique per client/name pair.[file:53]
- `BuildingUser` belongs to a `Client` and links to groups and buildings through many-to-many fields.[file:53]
- Most list pages should respect `get_allowed_client_ids(user)` so the UI remains scoped to allowed clients.[file:53]

## Current implementation state
- Dashboard, clients, buildings, and users pages are present as UI-first pages, with some views already connected to real queryset data and some still using static sample data.[file:53]
- `users_view` already uses real queryset data from `BuildingUser.objects.filter(client_id__in=client_ids)`.[file:53]
- `groups_view` already returns `ClientGroup` queryset data to `core/groups.html`, so the next step is mainly frontend page build-out for Groups-related HTML pages.[file:53]
- Buildings pages mix scaffold UI with sample records and sample chart data, showing that the project is currently focused on layout-first implementation before full backend behavior.[file:53]

## Coding and collaboration constraints
- Keep the current Django project structure and shared template approach intact.[file:53][cite:1]
- Prefer minimal, targeted code changes rather than unrelated refactors, and preserve the user’s existing bulky but organized coding style.[cite:1]
- When asking AI for help, provide only the current task, relevant files, and the latest handoff summary to reduce context drift on larger projects.[web:16][web:22]
