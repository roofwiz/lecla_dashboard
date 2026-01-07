import React, { useState, useEffect } from 'react';
import { fetchCRMJobs } from '../services/api';
import TimelineCard from '../components/TimelineCard';
import { TIMELINE_TEMPLATES, applyTimeline, cascadeTimelineUpdate } from '../utils/timeline';

function Timeline() {
    const [jobs, setJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [selectedTemplate, setSelectedTemplate] = useState('roofing_standard');
    const [timeline, setTimeline] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadJobs();
    }, []);

    useEffect(() => {
        if (selectedJob) {
            calculateTimeline();
        }
    }, [selectedJob, selectedTemplate]);

    const loadJobs = async () => {
        setLoading(true);
        try {
            const data = await fetchCRMJobs();
            const jobList = Array.isArray(data) ? data : (data?.results || []);
            setJobs(jobList);

            // Auto-select first job with anchor date
            const jobWithAnchor = jobList.find(j => j.first_estimate_signed_date);
            if (jobWithAnchor) {
                setSelectedJob(jobWithAnchor);
            }
        } catch (err) {
            console.error('Failed to load jobs', err);
        } finally {
            setLoading(false);
        }
    };

    const calculateTimeline = () => {
        if (!selectedJob) return;

        try {
            const template = TIMELINE_TEMPLATES[selectedTemplate];
            const calculatedTimeline = applyTimeline(selectedJob, template);
            setTimeline(calculatedTimeline);
        } catch (err) {
            console.error('Failed to calculate timeline', err);
            alert('Could not calculate timeline. Make sure the job has an anchor date (Estimate Signed).');
        }
    };

    const handleDateChange = (stepIndex, newDate, shouldCascade) => {
        if (!timeline) return;

        const originalDate = timeline[stepIndex].calculatedDate;

        if (shouldCascade) {
            // Apply cascading update
            const updatedTimeline = cascadeTimelineUpdate(timeline, stepIndex, newDate, originalDate);
            setTimeline(updatedTimeline);
        } else {
            // Just update this single step
            const updatedTimeline = [...timeline];
            updatedTimeline[stepIndex] = {
                ...updatedTimeline[stepIndex],
                actualDate: newDate,
                status: 'completed'
            };
            setTimeline(updatedTimeline);
        }
    };

    const handleSync = async () => {
        if (!timeline || !selectedJob) return;

        // TODO: Implement sync to JobNimbus
        // This would push actualDate values to their corresponding relatedField in JobNimbus
        console.log('Syncing timeline to JobNimbus...', {
            jobId: selectedJob.jnid,
            updates: timeline
                .filter(step => step.relatedField && step.actualDate)
                .map(step => ({
                    field: step.relatedField,
                    value: step.actualDate
                }))
        });

        alert('Timeline sync feature coming soon! This will push dates to JobNimbus custom fields.');
    };

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ marginBottom: '2rem' }}>
                <h1>📅 Smart Timeline</h1>
                <p style={{ color: 'var(--color-text-muted)' }}>
                    Folio-style project milestones with anchor dates and cascading updates
                </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' }}>
                {/* Left sidebar - Job & Template Selector */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    {/* Template Selector */}
                    <div className="card" style={{ padding: '15px' }}>
                        <h3 style={{ marginTop: 0, marginBottom: '12px', fontSize: '0.95rem' }}>
                            📋 Timeline Template
                        </h3>
                        <select
                            value={selectedTemplate}
                            onChange={(e) => setSelectedTemplate(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '10px',
                                background: 'rgba(255,255,255,0.05)',
                                border: '1px solid rgba(255,255,255,0.2)',
                                borderRadius: '6px',
                                color: 'white',
                                fontSize: '0.875rem',
                                cursor: 'pointer'
                            }}
                        >
                            {Object.values(TIMELINE_TEMPLATES).map(template => (
                                <option key={template.id} value={template.id}>
                                    {template.name}
                                </option>
                            ))}
                        </select>
                        {TIMELINE_TEMPLATES[selectedTemplate] && (
                            <p style={{
                                fontSize: '0.75rem',
                                color: 'var(--color-text-muted)',
                                marginTop: '8px',
                                marginBottom: 0
                            }}>
                                {TIMELINE_TEMPLATES[selectedTemplate].description}
                            </p>
                        )}
                    </div>

                    {/* Job Selector */}
                    <div className="card" style={{ padding: '15px', maxHeight: '500px', overflowY: 'auto' }}>
                        <h3 style={{ marginTop: 0, marginBottom: '15px', fontSize: '0.95rem' }}>Select Job</h3>
                        {loading ? (
                            <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Loading...</p>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                {jobs.slice(0, 50).map(job => (
                                    <div
                                        key={job.lecla_id}
                                        onClick={() => setSelectedJob(job)}
                                        style={{
                                            padding: '10px',
                                            background: selectedJob?.lecla_id === job.lecla_id
                                                ? 'rgba(59, 130, 246, 0.2)'
                                                : 'rgba(255,255,255,0.03)',
                                            border: selectedJob?.lecla_id === job.lecla_id
                                                ? '1px solid #3b82f6'
                                                : '1px solid rgba(255,255,255,0.1)',
                                            borderRadius: '6px',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s ease'
                                        }}
                                        onMouseEnter={(e) => {
                                            if (selectedJob?.lecla_id !== job.lecla_id) {
                                                e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                                            }
                                        }}
                                        onMouseLeave={(e) => {
                                            if (selectedJob?.lecla_id !== job.lecla_id) {
                                                e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                                            }
                                        }}
                                    >
                                        <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: '4px' }}>
                                            {job.name || job.number || 'Unnamed Job'}
                                        </div>
                                        <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>
                                            #{job.number} • {job.status_name || 'No status'}
                                        </div>
                                        {job.first_estimate_signed_date && (
                                            <div style={{ fontSize: '0.7rem', color: '#10b981', marginTop: '4px' }}>
                                                ✓ Has anchor date
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {/* Timeline Display */}
                <div>
                    {selectedJob && timeline ? (
                        <div>
                            <div style={{ marginBottom: '20px' }}>
                                <h2 style={{ margin: 0, marginBottom: '5px' }}>
                                    {selectedJob.name || selectedJob.number}
                                </h2>
                                <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                                    #{selectedJob.number} • {selectedJob.status_name} • {TIMELINE_TEMPLATES[selectedTemplate].name}
                                </p>
                            </div>

                            <TimelineCard
                                timeline={timeline}
                                onDateChange={handleDateChange}
                                onSync={handleSync}
                            />

                            {/* Template Info */}
                            <div className="card" style={{ marginTop: '20px', padding: '20px' }}>
                                <h3 style={{ marginTop: 0 }}>ℹ️ How It Works</h3>
                                <ul style={{ paddingLeft: '20px', margin: 0, color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
                                    <li style={{ marginBottom: '8px' }}>
                                        <strong>Anchor Date</strong>: {TIMELINE_TEMPLATES[selectedTemplate].anchorLabel} is the starting point
                                    </li>
                                    <li style={{ marginBottom: '8px' }}>
                                        <strong>Calculated Dates</strong>: All other dates are calculated based on offsets from the anchor
                                    </li>
                                    <li style={{ marginBottom: '8px' }}>
                                        <strong>Edit Dates</strong>: Click any date to manually adjust it
                                    </li>
                                    <li style={{ marginBottom: '8px' }}>
                                        <strong>Cascade Updates</strong>: When you change a date, you can automatically shift all future dates
                                    </li>
                                    <li style={{ marginBottom: 0 }}>
                                        <strong>Sync</strong>: Push dates to JobNimbus custom fields (dates marked with "↻ Syncs to JN")
                                    </li>
                                </ul>
                            </div>
                        </div>
                    ) : (
                        <div className="card" style={{ padding: '60px', textAlign: 'center' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '15px' }}>📅</div>
                            <h3>Select a job to view timeline</h3>
                            <p style={{ color: 'var(--color-text-muted)' }}>
                                Choose a job from the list and a template to generate a project timeline
                            </p>
                            <p style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginTop: '20px' }}>
                                <strong>Tip:</strong> Jobs need an "Estimate Signed" date to use as the timeline anchor
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Timeline;
