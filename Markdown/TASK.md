# TASK

## Current task
Build out the **function/content of the building-tab Dashboard page** — fill in the five placeholder cards inside `core/building_dashboard.html`, the template rendered by `building_dashboard` view (`/buildings/<int:building_id>/dashboard/`) and shown behind the first ("Dashboard") icon in the `base2.html` 8-icon building-tab nav.

## Immediate objective
Replace the empty `building-card-body` divs in `building_dashboard.html` with real card content using static/sample data, matching `Layout_Ref/07b_New_Dashboard.png`. The page must continue to fit seamlessly into the existing BLENDY building-tab shell (`base2.html`) and reuse the existing `.building-card` / `.building-card-tall` / `.building-card-wide` CSS classes from `static/css/app2.css`. Backend wiring (real queryset-backed data, live chart data pulled from the building's SQLite DB) is a **subsequent step** and is out of scope here.

Specific targets (five cards currently empty in the template):

- **BUILDING PROFILE** (`building-card-tall`) — building photo, building name, "Data Collection Device Status" line, "Fault Detection Insights" count with a progress/bar indicator, a small multi-day weather widget, building address, and an embedded location map — per `Layout_Ref/07b_New_Dashboard.png`.
- **DASHBOARD** (`building-card-wide`, main chart area) — a report-style chart (e.g. an "Average Cooling Load Report" stacked bar chart with an overlay temperature line), similar in spirit to the chart widgets already used on `chart.html`.
- **INSIGHTS** (`building-card-wide`) — a total-insights counter and a short "system with the most insights" list.
- **ENERGY BREAKDOWN** (`building-card`) — current-week energy breakdown labelled by system (e.g. "Chiller Plant") with a kWh figure.
- **GREEN FACTS** (`building-card`) — a small rotating tip/fact panel with an icon, short text, and pagination indicator.

## Background from the previous step
Charts, Systems, and Settings/Profile section is now complete:
- `building_charts`, `building_systems`, and `building_settings_profile` view functions are implemented in `core/views.py`, each `@login_required`, resolving the building via `pk` and enforcing `_user_can_access_object_client`.
- URL patterns `/buildings/<int:pk>/charts/`, `/buildings/<int:pk>/systems/`, and `/buildings/<int:pk>/settings/profile/` are registered in `core/urls.py`.
- `chart.html`, `systems.html`, and `settings_profile.html` are built as templates extending `base2.html`, wired into the building-tab sub-nav with `building_tab` active-state highlighting, consistent with the Vault, Insight, and Energy/Reports patterns.
- All 8 icons in the `base2.html` building-tab nav (Dashboard, Vault, Insights, Energy, Reports, Charts, Systems, Settings) now point to real `{% url %}` routes — no `href="#"` placeholders remain.

## Scope for the next coding round

**In scope:**
- `myportal/templates/core/building_dashboard.html` — fill in the five `building-card-body` sections with static/sample markup matching the mockup.
- `myportal/core/views.py` — extend the `building_dashboard` view context with sample data for each card (e.g. sample chart series, sample insight counts, sample energy figure, sample green-fact text) if the template needs it; keep the existing permission checks (`_user_can_access_object_client`) and session handling intact.

**Out of scope for this round:**
- Any changes to `admin.py` files or `admin_custom.css`.
- Structural changes to `static/css/app.css` / `app2.css` or `static/js/app.js` (small additive/scoped styles only if unavoidable).
- New Django models or migrations.
- Real queryset-backed data pulled from the building's linked SQLite database, live chart data, or weather/map API integration.
- Refactoring of existing views, URLs, or forms.
- Changes to `core/urls.py` — the `building_dashboard` route already exists and needs no new patterns.
- Buildings, app-level Dashboard, Groups, Users, Clients, Profile (account-level), Vault, Insight, Energy, Reports, Charts, Systems, or Settings pages.

## Starting point
- Review `myportal/templates/core/building_dashboard.html` for the current empty card skeleton (`building-dashboard-grid`, five `.building-card` sections).
- Review `Layout_Ref/07b_New_Dashboard.png` for the exact page layout and content per card.
- Review `myportal/core/views.py`'s `building_dashboard` view (renders `core/building_dashboard.html`, passes `selected_building`, `selected_client`, `building_tab="dashboard"`) for the current context shape.
- Review `static/css/app2.css` for the existing `.building-card` / `.building-card-tall` / `.building-card-wide` / `.building-card-head` / `.building-card-body` tokens to reuse.
- Review `chart.html` for any existing chart-widget pattern that can be reused for the Dashboard card's chart.
- Review `dashboard.html` (app-level) for the KPI card + chart widget layout pattern if useful for the Insights/Energy Breakdown cards.

## Expected deliverables
1. Updated `myportal/templates/core/building_dashboard.html` with real content in all five cards (Building Profile, Dashboard/chart, Insights, Energy Breakdown, Green Facts).
2. Updated `myportal/core/views.py` (`building_dashboard` view) with any additional sample context needed to support the new card content.

## Acceptance criteria
- The building dashboard page renders inside the shared BLENDY building-tab shell (`base2.html`) correctly, with the building-tab sub-nav still functional and the "Dashboard" tab showing an active state.
- Static/sample data is used for all card content (building profile fields, chart data, insight counts, energy figures, green fact text) — no real database queries required at this stage.
- Each card follows the visual pattern shown in `Layout_Ref/07b_New_Dashboard.png`.
- No regressions in any existing pages, including Vault, Insight, Energy, Reports, Charts, Systems, and Settings tabs.
- `app.css` and all admin files are untouched (aside from any minor, additive, clearly-scoped CSS if genuinely unavoidable).
