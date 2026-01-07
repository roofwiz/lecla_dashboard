import React, { useEffect, useState } from 'react';
import { fetchCRMJobs, triggerSync } from '../services/api';
import DetailModal from '../components/DetailModal';
import { JobNimbusIcon } from '../components/JobNimbusButton';

function CRMJobs() {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const [searchTerm, setSearchTerm] = useState('');
    const [statusFilter, setStatusFilter] = useState('All');
    const [activeOnly, setActiveOnly] = useState(false); // New: active jobs filter

    const loadJobs = async () => {
        setLoading(true);
        try {
            // Fetch active or all jobs based on toggle
            const endpoint = activeOnly ? '/api/crm/jobs/active' : '/api/crm/jobs';
            const response = await fetch(`http://localhost:8000${endpoint}`);
            const data = await response.json();
            setJobs(Array.isArray(data) ? data : []);
        } catch (err) {
            console.error("Failed to load jobs", err);
            setJobs([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadJobs();
    }, [activeOnly]); // Reload when active filter changes

    const handleSync = async () => {
        setSyncing(true);
        try {
            await triggerSync();
            alert("Sync started in background. Please refresh in a few moments.");
        } catch (err) {
            alert("Failed to start sync");
        } finally {
            setSyncing(false);
        }
    };

    const handleRowClick = (job) => {
        setSelectedJob(job);
        setIsModalOpen(true);
    };

    const filteredJobs = jobs.filter(job => {
        const matchesSearch = (job.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            job.number?.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesStatus = statusFilter === 'All' || job.status_name === statusFilter;
        return matchesSearch && matchesStatus;
    });

    const statuses = ['All', ...new Set(jobs.map(j => j.status_name))];

    return (
        <div className="crm-container">
            <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>CRM Jobs {activeOnly && <span style={{ fontSize: '0.875rem', color: '#10b981' }}>(Active Only)</span>}</h2>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        onClick={() => setActiveOnly(!activeOnly)}
                        style={{
                            padding: '10px 15px',
                            background: activeOnly ? '#10b981' : 'rgba(255,255,255,0.1)',
                            color: 'white',
                            border: activeOnly ? '1px solid #10b981' : '1px solid rgba(255,255,255,0.2)',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontWeight: '600'
                        }}
                    >
                        {activeOnly ? '✓ Active Jobs' : 'Show Active Only'}
                    </button>
                    <button onClick={loadJobs} className="btn-refresh" style={{ padding: '10px 15px', background: 'rgba(255,255,255,0.1)', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                        🔄 Refresh
                    </button>
                    <button
                        onClick={handleSync}
                        disabled={syncing}
                        className="btn-sync"
                        style={{
                            padding: '10px 20px',
                            background: 'var(--color-accent)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer'
                        }}
                    >
                        {syncing ? "Syncing..." : "Force JN Sync"}
                    </button>
                </div>
            </div>

            <div className="filters-bar" style={{ display: 'flex', gap: '15px', marginBottom: '20px' }}>
                <input
                    type="text"
                    placeholder="Search name or job #..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{
                        flex: 1,
                        padding: '10px 15px',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '6px',
                        color: 'white'
                    }}
                />
                <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    style={{
                        padding: '10px',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '6px',
                        color: 'white'
                    }}
                >
                    {statuses.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
            </div>

            <div className="card">
                {loading ? (
                    <p>Loading jobs...</p>
                ) : (
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                                <th style={{ padding: '12px' }}>Job #</th>
                                <th style={{ padding: '12px' }}>Name</th>
                                <th style={{ padding: '12px' }}>Status</th>
                                <th style={{ padding: '12px', textAlign: 'right' }}>Total</th>
                                <th style={{ padding: '12px', textAlign: 'center' }}>JobNimbus</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredJobs.map(job => (
                                <tr
                                    key={job.lecla_id}
                                    onClick={() => handleRowClick(job)}
                                    className="clickable-row"
                                    style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', cursor: 'pointer' }}
                                >
                                    <td style={{ padding: '12px' }}>{job.number || '—'}</td>
                                    <td style={{ padding: '12px' }}>{job.name}</td>
                                    <td style={{ padding: '12px' }}>
                                        <span className="status-badge" style={{ fontSize: '0.8em', padding: '2px 8px', borderRadius: '12px', background: 'rgba(255,255,255,0.1)' }}>
                                            {job.status_name}
                                        </span>
                                    </td>
                                    <td style={{ padding: '12px', textAlign: 'right' }}>${job.total?.toLocaleString()}</td>
                                    <td style={{ padding: '12px', textAlign: 'center' }}>
                                        <JobNimbusIcon type="job" id={job.jnid} title={job.name} />
                                    </td>
                                </tr>
                            ))}
                            {filteredJobs.length === 0 && (
                                <tr>
                                    <td colSpan="5" style={{ padding: '20px', textAlign: 'center' }}>No jobs found. Try adjusting filters or syncing.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                )}
            </div>

            <DetailModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={`Job ${selectedJob?.number || selectedJob?.name}`}
                data={selectedJob}
            />
        </div>
    );
}

export default CRMJobs;
