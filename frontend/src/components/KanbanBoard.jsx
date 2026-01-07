import React, { useState, useEffect } from 'react';
import { fetchCRMJobs } from '../services/api';
import { JobNimbusIcon } from '../utils/jobnimbus';

// Default JobNimbus statuses (14 as requested)
const DEFAULT_STATUSES = [
    { name: 'Lead', color: '#94a3b8' },
    { name: 'Appointment Scheduled', color: '#60a5fa' },
    { name: 'Estimating', color: '#f59e0b' },
    { name: 'Signed', color: '#10b981' },
    { name: 'Follow Up', color: '#a855f7' },
    { name: 'On Hold', color: '#64748b' },
    { name: 'Pending Deposit', color: '#fb923c' },
    { name: 'Pending Permit', color: '#FBBF24' },
    { name: 'Job Prep', color: '#3b82f6' },
    { name: 'In Progress', color: '#8b5cf6' },
    { name: 'Job Complete', color: '#22c55e' },
    { name: 'Pending Payments', color: '#eab308' },
    { name: 'Paid and Closed', color: '#059669' },
    { name: 'Lost', color: '#dc2626' },
    { name: 'Unqualified', color: '#9ca3af' }
];

function KanbanBoard() {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [statuses, setStatuses] = useState(DEFAULT_STATUSES);
    const [draggedJob, setDraggedJob] = useState(null);

    useEffect(() => {
        loadJobs();
    }, []);

    const loadJobs = async () => {
        setLoading(true);
        try {
            const data = await fetchCRMJobs();
            setJobs(Array.isArray(data) ? data : (data?.results || []));
        } catch (err) {
            console.error('Failed to load jobs', err);
        } finally {
            setLoading(false);
        }
    };

    const getJobsByStatus = (statusName) => {
        return jobs.filter(job => {
            const jobStatus = job.status_name || job.status || 'Lead';
            return jobStatus === statusName;
        });
    };

    const handleDragStart = (e, job) => {
        setDraggedJob(job);
        e.dataTransfer.effectAllowed = 'move';
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    };

    const handleDrop = async (e, newStatus) => {
        e.preventDefault();
        if (!draggedJob) return;

        // Update job status in local state
        const updatedJobs = jobs.map(job => {
            if (job.lecla_id === draggedJob.lecla_id) {
                return { ...job, status_name: newStatus };
            }
            return job;
        });

        setJobs(updatedJobs);
        setDraggedJob(null);

        // TODO: Make API call to update job status in backend
        console.log(`Updated job ${draggedJob.lecla_id} to status: ${newStatus}`);
    };

    const formatCurrency = (amount) => {
        if (!amount) return '$0';
        return `$${Number(amount).toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
    };

    if (loading) {
        return <div style={{ padding: '20px' }}>Loading jobs...</div>;
    }

    return (
        <div className="kanban-board" style={{ padding: '20px', overflowX: 'auto' }}>
            <div style={{ display: 'flex', gap: '15px', minWidth: 'max-content', paddingBottom: '20px' }}>
                {statuses.map(status => {
                    const statusJobs = getJobsByStatus(status.name);

                    return (
                        <div
                            key={status.name}
                            className="kanban-column"
                            onDragOver={handleDragOver}
                            onDrop={(e) => handleDrop(e, status.name)}
                            style={{
                                minWidth: '280px',
                                maxWidth: '280px',
                                background: 'rgba(255,255,255,0.03)',
                                borderRadius: '8px',
                                border: '1px solid rgba(255,255,255,0.1)'
                            }}
                        >
                            {/* Column Header */}
                            <div style={{
                                padding: '15px',
                                borderBottom: '1px solid rgba(255,255,255,0.1)',
                                background: `${status.color}15`,
                                borderTopLeftRadius: '8px',
                                borderTopRightRadius: '8px'
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <div style={{
                                            width: '8px',
                                            height: '8px',
                                            borderRadius: '50%',
                                            background: status.color
                                        }}></div>
                                        <h4 style={{ margin: 0, fontSize: '0.875rem', fontWeight: '600' }}>
                                            {status.name}
                                        </h4>
                                    </div>
                                    <span style={{
                                        background: `${status.color}30`,
                                        color: status.color,
                                        padding: '2px 8px',
                                        borderRadius: '12px',
                                        fontSize: '0.75rem',
                                        fontWeight: '600'
                                    }}>
                                        {statusJobs.length}
                                    </span>
                                </div>
                            </div>

                            {/* Job Cards */}
                            <div style={{ padding: '10px', maxHeight: '70vh', overflowY: 'auto' }}>
                                {statusJobs.map(job => (
                                    <div
                                        key={job.lecla_id}
                                        draggable
                                        onDragStart={(e) => handleDragStart(e, job)}
                                        style={{
                                            background: 'rgba(255,255,255,0.05)',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            borderRadius: '6px',
                                            padding: '12px',
                                            marginBottom: '8px',
                                            cursor: 'move',
                                            transition: 'all 0.2s ease'
                                        }}
                                        className="kanban-card"
                                    >
                                        <div style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                                            <div style={{ flex: 1 }}>
                                                <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '4px' }}>
                                                    {job.name || job.number || 'Unnamed Job'}
                                                </div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                                    #{job.number}
                                                </div>
                                            </div>
                                            <JobNimbusIcon entityType="jobs" jnid={job.jnid} />
                                        </div>

                                        {job.total && (
                                            <div style={{
                                                fontSize: '0.875rem',
                                                fontWeight: '700',
                                                color: '#10b981',
                                                marginTop: '8px'
                                            }}>
                                                {formatCurrency(job.total)}
                                            </div>
                                        )}

                                        {job.type && (
                                            <div style={{
                                                fontSize: '0.7rem',
                                                color: 'var(--color-text-muted)',
                                                marginTop: '4px',
                                                fontStyle: 'italic'
                                            }}>
                                                {job.type}
                                            </div>
                                        )}
                                    </div>
                                ))}

                                {statusJobs.length === 0 && (
                                    <div style={{
                                        padding: '20px',
                                        textAlign: 'center',
                                        color: 'var(--color-text-muted)',
                                        fontSize: '0.875rem'
                                    }}>
                                        No jobs
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            <style>{`
                .kanban-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    border-color: rgba(255,255,255,0.2);
                }
                
                .kanban-column:has(.kanban-card:hover) {
                    background: rgba(255,255,255,0.05);
                }
            `}</style>
        </div>
    );
}

export default KanbanBoard;
