import React, { useEffect, useState } from 'react';
import DashboardLayout from './layouts/DashboardLayout';
import { fetchJobs, fetchProjects, fetchCalendar } from './services/api';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [projects, setProjects] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        // Parallel fetching
        const [jobsData, projectsData, calendarData] = await Promise.allSettled([
          fetchJobs(),
          fetchProjects(),
          fetchCalendar()
        ]);

        if (jobsData.status === 'fulfilled') {
          setJobs(jobsData.value.results || (Array.isArray(jobsData.value) ? jobsData.value : []));
        }

        if (projectsData.status === 'fulfilled') {
          setProjects(projectsData.value || []);
        }

        if (calendarData.status === 'fulfilled') {
          setEvents(calendarData.value || []);
        }

      } catch (err) {
        console.warn("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // Helper to format date
  const formatDate = (dateString, dateOnly) => {
    if (!dateString && !dateOnly) return '';
    const targetDate = dateString || dateOnly; // Support all-day events using 'date' field
    const date = new Date(targetDate);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: dateString ? 'numeric' : undefined, minute: dateString ? '2-digit' : undefined });
  };

  return (
    <DashboardLayout title="Dashboard">
      <div className="dashboard-grid">
        <div className="card welcome-card">
          <h2>Welcome Back, Lecla Team! 👋</h2>
          <p>Here's what's happening today.</p>
        </div>

        <div className="card stat-card">
          <h3>Active Jobs</h3>
          <div className="stat-value">
            {loading ? "..." : jobs.length}
          </div>
          <span className="stat-trend positive">
            {loading ? "Syncing..." : "Synced with JobNimbus"}
          </span>
        </div>

        <div className="card stat-card">
          <h3>Upcoming Events</h3>
          <div className="stat-value">{loading ? "..." : events.length}</div>
          <span className="stat-trend neutral">Next 7 Days</span>
        </div>

        <div className="card stat-card">
          <h3>Active Projects</h3>
          <div className="stat-value">{loading ? "..." : projects.length}</div>
          <span className="stat-trend positive">CompanyCam</span>
        </div>

        <div className="card recent-activity">
          <h3>Job Nimbus Jobs</h3>
          <ul>
            {jobs.slice(0, 5).map((job, index) => (
              <li key={job.jnid || index}>
                <strong>{job.name || job.number || "Unnamed Job"}</strong>
                <span className="status-badge" style={{ marginLeft: '8px', fontSize: '0.7em', padding: '2px 6px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px' }}>
                  {job.status_name || "Pending"}
                </span>
              </li>
            ))}
            {jobs.length === 0 && !loading && (
              <li>No jobs found.</li>
            )}
          </ul>
        </div>

        <div className="card recent-activity">
          <h3>CompanyCam Projects</h3>
          <ul>
            {projects.slice(0, 5).map((project, index) => (
              <li key={project.id || index}>
                <strong>{project.name}</strong>
                <br />
                <span style={{ fontSize: '0.8em', color: 'var(--color-text-muted)' }}>
                  {project.address ? `${project.address.street_address || ''}, ${project.address.city || ''}` : "No address"}
                </span>
              </li>
            ))}
            {projects.length === 0 && !loading && (
              <li>No projects found.</li>
            )}
          </ul>
        </div>

        <div className="card recent-activity">
          <h3>Schedule</h3>
          <ul className="event-list">
            {events.slice(0, 5).map((event, index) => (
              <li key={event.id || index} style={{ borderLeft: '3px solid var(--color-accent)', paddingLeft: '10px' }}>
                <strong>{event.summary || "No Title"}</strong>
                <br />
                <span style={{ fontSize: '0.8em', color: 'var(--color-text-muted)' }}>
                  {formatDate(event.start?.dateTime, event.start?.date)}
                </span>
              </li>
            ))}
            {events.length === 0 && !loading && (
              <li>No upcoming events.</li>
            )}
          </ul>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default App;
