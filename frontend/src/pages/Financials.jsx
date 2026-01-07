import React, { useState, useEffect } from 'react';
import { fetchCRMJobs } from '../services/api';
import { calculateJobFinancials } from '../services/financials';
import FinancialCard from '../components/FinancialCard';

function Financials() {
    const [jobs, setJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [financials, setFinancials] = useState(null);
    const [loading, setLoading] = useState(false);
    const [calculating, setCalculating] = useState(false);

    useEffect(() => {
        loadJobs();
    }, []);

    const loadJobs = async () => {
        setLoading(true);
        try {
            const data = await fetchCRMJobs();
            const jobList = Array.isArray(data) ? data : (data?.results || []);
            setJobs(jobList);

            // Auto-select first job with financial data
            const jobWithData = jobList.find(j => j.total_project || j.total_gross);
            if (jobWithData) {
                handleSelectJob(jobWithData);
            }
        } catch (err) {
            console.error('Failed to load jobs', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSelectJob = async (job) => {
        setSelectedJob(job);
        setCalculating(true);

        try {
            // Try to calculate fresh financials
            const data = await calculateJobFinancials(job.jnid);
            setFinancials(data);
        } catch (err) {
            console.error('Failed to calculate financials', err);
            // Fallback to cached data from job object
            setFinancials({
                total_invoiced: (job.total_project || 0) + (job.permit_fee || 0) + (job.financing_fee || 0),
                permit_fee: job.permit_fee || 0,
                financing_fee: job.financing_fee || 0,
                total_project: job.total_project || 0,
                total_gross: job.total_gross || 0,
                total_net: job.total_net || 0,
                commissions: job.commissions || 0
            });
        } finally {
            setCalculating(false);
        }
    };

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ marginBottom: '2rem' }}>
                <h1>💰 Financial Dashboard</h1>
                <p style={{ color: 'var(--color-text-muted)' }}>
                    Navigate job financials with intelligent revenue tracking
                </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' }}>
                {/* Job Selector */}
                <div className="card" style={{ padding: '15px', maxHeight: '600px', overflowY: 'auto' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '15px', fontSize: '1rem' }}>Select Job</h3>
                    {loading ? (
                        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Loading...</p>
                    ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            {jobs.slice(0, 50).map(job => (
                                <div
                                    key={job.lecla_id}
                                    onClick={() => handleSelectJob(job)}
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
                                    {job.total_project && (
                                        <div style={{ fontSize: '0.75rem', color: '#10b981', marginTop: '4px' }}>
                                            ${job.total_project.toLocaleString()}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Financial Display */}
                <div>
                    {selectedJob ? (
                        <div>
                            <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <h2 style={{ margin: 0, marginBottom: '5px' }}>
                                        {selectedJob.name || selectedJob.number}
                                    </h2>
                                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                                        #{selectedJob.number} • {selectedJob.status_name}
                                    </p>
                                </div>
                                {calculating && (
                                    <div style={{
                                        padding: '8px 16px',
                                        background: 'rgba(59, 130, 246, 0.1)',
                                        borderRadius: '6px',
                                        fontSize: '0.875rem',
                                        color: '#60a5fa'
                                    }}>
                                        Calculating...
                                    </div>
                                )}
                            </div>

                            <FinancialCard financials={financials} />

                            {/* Additional Details */}
                            {financials && (
                                <div className="card" style={{ marginTop: '20px', padding: '20px' }}>
                                    <h3>📊 Financial Breakdown</h3>
                                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', marginTop: '15px' }}>
                                        <div style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '6px' }}>
                                            <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
                                                Revenue per Dollar Invoiced
                                            </div>
                                            <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>
                                                {financials.total_invoiced > 0
                                                    ? `${((financials.total_project / financials.total_invoiced) * 100).toFixed(1)}%`
                                                    : 'N/A'}
                                            </div>
                                        </div>
                                        <div style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '6px' }}>
                                            <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
                                                Gross Profit Margin
                                            </div>
                                            <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>
                                                {financials.total_project > 0
                                                    ? `${((financials.total_gross / financials.total_project) * 100).toFixed(1)}%`
                                                    : 'N/A'}
                                            </div>
                                        </div>
                                        <div style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '6px' }}>
                                            <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
                                                Net Profit Margin
                                            </div>
                                            <div style={{ fontSize: '1.25rem', fontWeight: '600', color: '#8b5cf6' }}>
                                                {financials.total_project > 0
                                                    ? `${((financials.total_net / financials.total_project) * 100).toFixed(1)}%`
                                                    : 'N/A'}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="card" style={{ padding: '60px', textAlign: 'center' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '15px' }}>📊</div>
                            <h3>Select a job to view financials</h3>
                            <p style={{ color: 'var(--color-text-muted)' }}>
                                Choose a job from the list to see detailed financial breakdown
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Financials;
