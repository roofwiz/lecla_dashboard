import React, { useEffect, useState } from 'react';
import { fetchCRMJobs, fetchProjects, fetchCalendar } from '../services/api';
import { JobNimbusIcon } from '../components/JobNimbusButton';
import MapWidget from '../components/MapWidget';

function Dashboard() {
    const [jobs, setJobs] = useState([]);
    const [projects, setProjects] = useState([]);
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState({
        jobs: true,
        projects: true,
        calendar: true
    });

    useEffect(() => {
        console.log("Dashboard: Component mounted, starting independent data fetches...");

        // Fetch Jobs
        fetchCRMJobs().then(data => {
            console.log("Dashboard: Jobs loaded");
            const result = Array.isArray(data) ? data : (data?.results || []);
            setJobs(result);
            setLoading(prev => ({ ...prev, jobs: false }));
        }).catch(err => {
            console.error("Dashboard: Error fetching jobs", err);
            setJobs([]);
            setLoading(prev => ({ ...prev, jobs: false }));
        });

        // Fetch Projects
        fetchProjects().then(data => {
            console.log("Dashboard: Projects loaded");
            setProjects(Array.isArray(data) ? data : []);
            setLoading(prev => ({ ...prev, projects: false }));
        }).catch(err => {
            console.error("Dashboard: Error fetching projects", err);
            setProjects([]);
            setLoading(prev => ({ ...prev, projects: false }));
        });

        // Fetch Calendar
        fetchCalendar().then(data => {
            console.log("Dashboard: Calendar loaded");
            setEvents(Array.isArray(data) ? data : []);
            setLoading(prev => ({ ...prev, calendar: false }));
        }).catch(err => {
            console.error("Dashboard: Error fetching calendar", err);
            setEvents([]);
            setLoading(prev => ({ ...prev, calendar: false }));
        });

    }, []);

    // Helper to format date
    const formatDate = (dateString, dateOnly) => {
        if (!dateString && !dateOnly) return '';
        const targetDate = dateString || dateOnly; // Support all-day events using 'date' field
        const date = new Date(targetDate);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: dateString ? 'numeric' : undefined, minute: dateString ? '2-digit' : undefined });
    };

    return (
        <div className="dashboard-grid">
            <div className="card welcome-card" style={{ gridColumn: 'span 3' }}>
                <h2>Welcome Back, Lecla Team! 👋</h2>
                <p>Here's what's happening today. You have {projects.length} active projects and {jobs.length} jobs in your pipeline.</p>
            </div>

            <div className="card stat-card">
                <h3>Active Jobs</h3>
                <div className="stat-value">
                    {loading.jobs ? "..." : jobs.length}
                </div>
                <span className="stat-trend positive">
                    {loading.jobs ? "Syncing..." : "Independent CRM"}
                </span>
            </div>

            <div className="card stat-card">
                <h3>Upcoming Events</h3>
                <div className="stat-value">{loading.calendar ? "..." : events.length}</div>
                <span className="stat-trend neutral">Next 7 Days</span>
            </div>

            <div className="card stat-card">
                <h3>Active Projects</h3>
                <div className="stat-value">{loading.projects ? "..." : projects.length}</div>
                <span className="stat-trend positive">CompanyCam</span>
            </div>

            <div className="card recent-activity">
                <h3>Lecla CRM Jobs</h3>
                <ul>
                    {jobs.slice(0, 5).map((job, index) => (
                        <li key={job.lecla_id || index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div style={{ flex: 1 }}>
                                <strong>{job.name || job.number || "Unnamed Job"}</strong>
                                <span className="status-badge" style={{ marginLeft: '8px', fontSize: '0.7em', padding: '2px 6px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px' }}>
                                    {job.status_name || "Pending"}
                                </span>
                            </div>
                            <JobNimbusIcon type="job" id={job.jnid} title={job.name} />
                        </li>
                    ))}
                    {jobs.length === 0 && !loading.jobs && (
                        <li>No jobs found.</li>
                    )}
                    {loading.jobs && (
                        <li>Loading jobs...</li>
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
                    {projects.length === 0 && !loading.projects && (
                        <li>No projects found.</li>
                    )}
                    {loading.projects && (
                        <li>Loading projects...</li>
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
                    {events.length === 0 && !loading.calendar && (
                        <li>No upcoming events.</li>
                    )}
                    {loading.calendar && (
                        <li>Loading events...</li>
                    )}
                </ul>
            </div>
        </div>
    );
}

export default Dashboard;
