# Lecla Dashboard - Developer Journal

This document tracks the daily progress of the Lecla Dashboard project, summarizing key decisions, implemented features, and technical details.

## [2026-01-01] - Project Kickoff & Core Integrations
### Summary
Successfully initialized the project, implemented the full-stack architecture, and completed core integrations with Job Nimbus, Company Cam, and Google Calendar. The "Home" dashboard is live and displaying real-time data from all three sources.

### Details
- **Architecture Setup**:
  - **Frontend**: Initialized React (Vite) with a Premium Dark Theme design system.
  - **Backend**: Configured FastAPI with `httpx` for async proxy requests.
  - **Security**: set up `.env` management and `config.py` for API keys.
- **API Integration**:
  - Created `/api/jobs` endpoint (Job Nimbus).
  - Created `/api/projects` endpoint (Company Cam).
  - Created `/api/calendar` endpoint (Google Calendar) using OAuth2 flow.
  - **[Verified]** Frontend is successfully fetching and displaying data from all 3 services.
  - **[Pending]** Google Maps integration (API Key configured but needs validation).
- **Dashboard UI**:
  - Implemented core layout with **Sidebar** and **Header**.
  - Created a responsive Grid layout with Glassmorphism effects.
  - Added widgets for Active Jobs, Projects, and Upcoming Schedule.

### Technical Notes & Gotchas (Things to Remember)
1.  **Git Security**: 
    -   NEVER commit `client_secret.json`, `token.pickle`, or `.env` files.
    -   If a push is rejected by "pre-receive hook", check if you are accidentally committing secrets.
    -   Ensure sensitive files are listed in `.gitignore`.
2.  **Google OAuth**: 
    -   First-time run requires executing `python backend/google_auth_flow.py` locally to generate `token.pickle`.
    -   Test Users must be added in Google Cloud Console while the app is in "Testing" mode.
3.  **Environment Variables**:
    -   Always restarting the backend (`Ctrl+C` then `uvicorn...`) is required to load changes from `.env`.

### Next Steps (Pick Up Here)
1.  **Google Maps**: Debug `GOOGLE_API_KEY` to enable the map widget.
2.  **Dedicated Pages**: Create full-view pages for:
    -   **/jobs**: Detailed table of Job Nimbus leads.
    -   **/photos**: Gallery view for Company Cam projects.
    -   **/schedule**: Full calendar view.
3.  **Deployment**: Prepare for eventual deployment (likely Vercel/Render or similar).

## [2026-01-02] - Sales Audit & Local Database
### Summary
Addressed data reliability issues with JobNimbus sales figures. Shifted from live API scraping (which was slow and hitting pagination limits) to a robust **Local Database (SQLite)** architecture. Successfully implemented a synchronization engine and generated audit reports flagging significant revenue discrepancies.

### Details
- **Backend Architecture Update**:
  - **Local Database**: Implemented `backend/lecla.db` (SQLite) to serve as the single source of truth for dashboard data.
  - **Smart Sync Service**: Created `backend/sync_service.py` which:
    - Fetches all Budgets and Estimates.
    - Intelligently identifies and fetches only the relevant linked Jobs.
    - **Fixes**: Worked around JobNimbus API broken pagination for `/jobs` by using targeted lookups.
  - **CLI Tools**: Added `sync_db.bat` for one-click database updates.
- **Sales Data Audit**:
  - Created `backend/report_from_db.py` to analyze financial integrity.
  - **Findings**: Flagged **949** instances where "Budget Revenue" did not match "Job Total" (discrepancy > $1.00).
  - **Report**: Generated `backend/discrepancy_report_db.csv` for user review.

### Technical Notes
- **API Limits**: The JobNimbus API `/jobs` endpoint `skip` parameter is unreliable for deep paging (>5000 items). The new "Smart Sync" strategy avoids this by fetching specific IDs gathered from Budgets.
- **Performance**: Dashboard reporting is now instant (querying local DB) rather than waiting minutes for API calls.

### Next Steps
1.  **Frontend Integration**: Connect the React dashboard to read from the local database endpoints instead of proxying live requests.
2.  **Discrepancy UI**: Create a "Data Quality" view in the dashboard to visualize these budget vs. job mismatches.

