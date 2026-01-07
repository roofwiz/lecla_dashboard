import React, { useEffect, useState } from 'react';
import api from '../services/api';

function Audit() {
    const [auditData, setAuditData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadAudit = async () => {
            setLoading(true);
            try {
                const resp = await api.get('/crm/audit');
                setAuditData(Array.isArray(resp.data) ? resp.data : []);
            } catch (err) {
                console.error("Failed to load audit data", err);
            } finally {
                setLoading(false);
            }
        };
        loadAudit();
    }, []);

    return (
        <div className="audit-page">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Data Quality Audit</h1>
                <p style={{ color: 'var(--color-text-muted)' }}>Mismatches between Budget Revenue and Job Totals</p>
            </header>

            <div className="card">
                {loading ? (
                    <p>Analyzing financial data...</p>
                ) : (
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                                <th style={{ padding: '12px' }}>Budget #</th>
                                <th style={{ padding: '12px' }}>Sales Rep</th>
                                <th style={{ padding: '12px' }}>Job Name</th>
                                <th style={{ padding: '12px', textAlign: 'right' }}>Budget Rev</th>
                                <th style={{ padding: '12px', textAlign: 'right' }}>Job Total</th>
                                <th style={{ padding: '12px', textAlign: 'right' }}>Discrepancy</th>
                                <th style={{ padding: '12px', textAlign: 'center' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {auditData.map((row, index) => (
                                <tr key={index} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                    <td style={{ padding: '12px' }}>{row.budget_number}</td>
                                    <td style={{ padding: '12px' }}>{row.sales_rep}</td>
                                    <td style={{ padding: '12px' }}>{row.job_name || '—'}</td>
                                    <td style={{ padding: '12px', textAlign: 'right' }}>${row.budget_revenue?.toLocaleString()}</td>
                                    <td style={{ padding: '12px', textAlign: 'right' }}>${row.job_total?.toLocaleString() || '0'}</td>
                                    <td style={{
                                        padding: '12px',
                                        textAlign: 'right',
                                        fontWeight: 'bold',
                                        color: Math.abs(row.discrepancy) > 1000 ? '#ef4444' : '#f59e0b'
                                    }}>
                                        ${row.discrepancy?.toLocaleString()}
                                    </td>
                                    <td style={{ padding: '12px', textAlign: 'center' }}>
                                        {row.related_job_id && (
                                            <a
                                                href={`https://app.jobnimbus.com/job/${row.related_job_id}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="btn-link"
                                                style={{ color: 'var(--color-primary)', textDecoration: 'none', fontSize: '0.8rem' }}
                                            >
                                                View JN ↗
                                            </a>
                                        )}
                                    </td>
                                </tr>
                            ))}
                            {auditData.length === 0 && (
                                <tr>
                                    <td colSpan="6" style={{ padding: '40px', textAlign: 'center', color: 'var(--color-text-muted)' }}>
                                        ✅ No major discrepancies found. Data is clean!
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                )}
            </div>

            <div style={{ marginTop: '20px', padding: '15px', background: 'rgba(245, 158, 11, 0.1)', borderRadius: '8px', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
                <p style={{ margin: 0, fontSize: '0.9rem', color: '#f59e0b' }}>
                    <strong>Note:</strong> Discrepancies usually indicate that a Budget was updated without adjusting the associated Job Record, or vice versa. These should be reviewed in JobNimbus.
                </p>
            </div>
        </div>
    );
}

export default Audit;
