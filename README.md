# Lecla Dashboard

**A professional executive command center for Lecla Home Improvements and Roofing Inc.**

---

## 🎯 Overview

The Lecla Dashboard is a modern, AI-powered business intelligence platform that integrates real-time data from JobNimbus CRM, CompanyCam photo management, and Google Services to provide comprehensive visibility into operations, sales, and project management.

## ✨ Features

### 📊 Executive Dashboard
- **Live Project Map**: Geolocation visualization of active projects
- **Real-Time Statistics**: Jobs, projects, and calendar events
- **Interactive Widgets**: Customizable data displays

### 🏠 CRM Integration
- **1,000+ Jobs**: Synced from JobNimbus with intelligent duplicate detection
- **Advanced Search**: Filter by status, customer, or date
- **Background Sync**: Automatic data updates

### 📸 Photo Gallery
- **CompanyCam Integration**: 25+ active project portfolios
- **Professional Grid Layout**: Hover effects and responsive design
- **Project Timeline**: Visual progress tracking

### 🗓️ Schedule Management
- **Google Calendar**: Seamless event integration
- **Timeline View**: Upcoming appointments and deadlines
- **Event Details**: Location, time, and attendee information

### 🧠 AI Co-Pilot
- **Powered by Gemini 2.0 Flash**: Instant business insights
- **Natural Language Queries**: Ask questions about revenue, jobs, or projects
- **Context-Aware**: Accesses live CRM and sales data

### 📊 Sales Audit
- **Data Quality Monitoring**: Budget vs. Job discrepancy tracking
- **Direct Links**: Fast navigation to JobNimbus records
- **Revenue Analysis**: SQL-powered reporting engine

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Google Cloud Project** (for API keys and service accounts)

### Installation

#### 1. Clone & Setup
```powershell
cd "c:\Users\eric\React Projects\Lecla Dashboard"
```

#### 2. Backend Setup
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```env
JOB_NIMBUS_API_TOKEN=your_token
COMPANY_CAM_TOKEN=your_token
GOOGLE_MAPS_PLATFORM_API_KEY=AIza...
DATABASE_URL=sqlite:///./lecla.db  # or PostgreSQL URI
```

Add `service_account.json` for Vertex AI.

#### 3. Frontend Setup
```powershell
cd frontend
npm install
```

#### 4. Run Application

**Terminal 1 (Backend):**
```powershell
cd backend
venv\Scripts\activate
python -m uvicorn backend.app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm run dev -- --port 5173
```

**Access**: http://localhost:5173

---

## 🏗️ Architecture

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Vite 7.3 |
| Backend | FastAPI + SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI | Vertex AI (Gemini 2.0 Flash) |
| Auth | OAuth 2.0 |

### Key Integrations
- **JobNimbus API**: CRM data, jobs, contacts, budgets
- **CompanyCam API**: Project photos and timelines
- **Google Calendar API**: Event management
- **Google Maps API**: Project geolocation
- **Vertex AI API**: Business intelligence assistant

---

## 📁 Project Structure

```
lecla-dashboard/
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI
│   │   ├── pages/             # Route pages
│   │   ├── services/          # API clients
│   │   └── App.jsx
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # External API clients
│   │   ├── models.py          # SQLAlchemy ORM
│   │   ├── database.py        # DB config
│   │   └── main.py            # FastAPI app
│   ├── crm_sync.py            # Background sync
│   ├── google_auth_flow.py    # OAuth setup
│   └── .env                   # Environment vars
│
└── docs/                       # Documentation
```

---

## 🔐 Security

- **Environment Variables**: Secrets stored in `.env` (gitignored)
- **OAuth 2.0**: Google API authentication
- **Service Accounts**: Vertex AI enterprise access
- **API Key Restrictions**: Domain and IP restrictions enabled

---

## 📊 Database Schema

**SQLAlchemy Models** (PostgreSQL-ready):
- `users`: Authentication and roles
- `contacts`: Customer information
- `jobs`: Project records from JobNimbus
- `leads`: Sales pipeline
- `budgets`: Financial estimates
- `estimates`: Pricing proposals
- `invoices`: Billing records

---

## 🌐 API Endpoints

### Core Routes
- `GET /api/config`: Frontend configuration
- `GET /api/jobs`: Job list with filters
- `GET /api/projects`: CompanyCam projects
- `GET /api/calendar/events`: Google Calendar

### CRM Routes (`/api/crm`)
- `GET /crm/contacts`: Customer list
- `GET /crm/jobs`: Job database
- `GET /crm/audit`: Sales discrepancy report
- `POST /crm/sync`: Trigger background sync

### AI Routes (`/api/ai`)
- `POST /ai/chat`: Gemini AI conversation

### Reports Routes (`/api/reports`)
- `GET /reports/sales-by-rep`: Revenue by sales rep

---

## 🎨 UI/UX Highlights

- **Premium Dark Mode**: Professional glassmorphism effects
- **Responsive Design**: Desktop and mobile optimized
- **Interactive Maps**: Google Maps with custom styling
- **Smooth Animations**: Hover effects and transitions
- **Accessibility**: ARIA labels and keyboard navigation

---

## 🚀 Deployment

### Cloud-Ready Architecture
The dashboard is designed for Google Cloud Platform:

1. **Cloud Run**: Backend API hosting
2. **Cloud SQL**: PostgreSQL database
3. **Secret Manager**: Environment variable management
4. **Cloud Storage**: Media and backups

### Database Migration
Switch to PostgreSQL by updating `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/lecla_dashboard
```

SQLAlchemy handles all database compatibility automatically.

---

## 📈 Performance

- **SQLAlchemy ORM**: Efficient database queries
- **Duplicate Detection**: Intelligent sync prevents data bloat
- **Lazy Loading**: Images and components load on demand
- **Caching**: API responses cached for speed

---

## 🤝 Contributing

This is a proprietary project for Lecla Home Improvements and Roofing Inc.

---

## 📄 License

Proprietary - © 2026 Lecla Home Improvements and Roofing Inc.

---

## 📞 Support

For technical support or questions, contact the development team.

---

## 🎯 Mission Statement

**Empower Lecla's leadership team with real-time, AI-driven business intelligence.**

The Lecla Dashboard transforms raw data from JobNimbus, CompanyCam, and Google Services into actionable insights, enabling faster decision-making and operational excellence.

---

**Status**: ✅ Production Ready | **Version**: 1.0 | **Last Updated**: January 5, 2026
