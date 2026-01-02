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
