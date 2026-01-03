import React, { useEffect, useState } from 'react';
import { fetchSalesReports } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';

function Reports() {
    const [reportData, setReportData] = useState({ results: [], total_revenue: 0, total_leads: 0, total_closed: 0, goal: 0, year: 2026 });
    const [loading, setLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState(2025); // Default to Last Year as requested

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            console.log("Fetching report for year:", selectedYear);
            try {
                const data = await fetchSalesReports(selectedYear);
                console.log("Report Data Received:", data);
                setReportData(data || { results: [], total_revenue: 0, total_leads: 0, total_closed: 0, goal: 0, year: selectedYear });
            } catch (err) {
                console.error("Failed to load reports", err);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, [selectedYear]);

    // Colors for visualization
    const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

    // Goal Calculation
    const progressPercent = reportData.goal > 0 ? (reportData.total_revenue / reportData.goal) * 100 : 0;

    return (
        <div className="reports-page">
            <header style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1>Sales Reports {selectedYear}</h1>
                    <p style={{ color: 'var(--color-text-muted)' }}>Performance based on Budgets & Invoices</p>
                </div>

                {/* Year Selector */}
                <div className="year-selector" style={{ display: 'flex', gap: '10px', background: 'rgba(255,255,255,0.05)', padding: '5px', borderRadius: '8px' }}>
                    <button
                        onClick={() => setSelectedYear(2025)}
                        style={{
                            background: selectedYear === 2025 ? 'var(--color-accent)' : 'transparent',
                            border: 'none', color: 'white', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer'
                        }}>
                        2025 (Past)
                    </button>
                    <button
                        onClick={() => setSelectedYear(2026)}
                        style={{
                            background: selectedYear === 2026 ? 'var(--color-accent)' : 'transparent',
                            border: 'none', color: 'white', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer'
                        }}>
                        2026 (Current)
                    </button>
                </div>
            </header>

            <div className="dashboard-grid">
                {/* 1. Leads Card */}
                <div className="card stat-card">
                    <h3>Total Leads</h3>
                    <div className="stat-value">
                        {reportData.total_leads ? reportData.total_leads.toLocaleString() : 0}
                    </div>
                    <span className="stat-trend neutral">All Opportunities Created</span>
                </div>

                {/* 2. Revenue Card with Goal */}
                <div className="card stat-card">
                    <h3>Total Sales Revenue</h3>
                    <div className="stat-value">
                        ${reportData.total_revenue.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                    </div>

                    {/* Goal Progress */}
                    <div style={{ marginTop: '15px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '5px' }}>
                            <span>Goal: ${reportData.goal.toLocaleString()}</span>
                            <span>{progressPercent.toFixed(1)}%</span>
                        </div>
                        <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                            <div style={{
                                width: `${Math.min(progressPercent, 100)}%`,
                                height: '100%',
                                background: progressPercent >= 100 ? '#10b981' : 'var(--color-accent)',
                                transition: 'width 1s ease-out'
                            }}></div>
                        </div>
                    </div>
                </div>

                {/* 3. Closed Card */}
                <div className="card stat-card">
                    <h3>Paid & Closed Jobs</h3>
                    <div className="stat-value">
                        {reportData.total_closed ? reportData.total_closed.toLocaleString() : 0}
                    </div>
                    <span className="stat-trend positive">Success Rate: {reportData.total_leads > 0 ? ((reportData.total_closed / reportData.total_leads) * 100).toFixed(1) : 0}%</span>
                </div>

                {/* Main Chart */}
                <div className="card" style={{ gridColumn: 'span 3', minHeight: '400px' }}>
                    <h3>Sales by Representative ({selectedYear})</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginBottom: '1rem' }}>Ranked by Budgeted Revenue for {selectedYear}</p>

                    <div style={{ width: '100%', height: '300px' }}>
                        {loading ? (
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                                Loading data...
                            </div>
                        ) : (
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={reportData.results} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" horizontal={false} />
                                    <XAxis type="number" hide />
                                    <YAxis
                                        dataKey="name"
                                        type="category"
                                        tick={{ fill: 'var(--color-text-primary)', fontSize: 12 }}
                                        width={100}
                                    />
                                    <Tooltip
                                        itemStyle={{ color: '#000' }}
                                        formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']}
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
                                    />
                                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                                        {reportData.results.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        )}
                    </div>
                </div>

                {/* Detailed List */}
                <div className="card recent-activity" style={{ gridColumn: 'span 3' }}>
                    <h3>{selectedYear} Performance Breakdown</h3>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                                <th style={{ padding: '10px' }}>Sales Rep</th>
                                <th style={{ padding: '10px' }}>Revenue (Budgeted)</th>
                                <th style={{ padding: '10px' }}>Contribution</th>
                            </tr>
                        </thead>
                        <tbody>
                            {reportData.results.map((row, index) => (
                                <tr key={index} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                    <td style={{ padding: '12px' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: COLORS[index % COLORS.length] }}></div>
                                            {row.name}
                                        </div>
                                    </td>
                                    <td style={{ padding: '12px', fontWeight: 'bold' }}>
                                        ${row.value.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                                    </td>
                                    <td style={{ padding: '12px', color: 'var(--color-text-muted)' }}>
                                        {reportData.total_revenue > 0 ? ((row.value / reportData.total_revenue) * 100).toFixed(1) : 0}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Reports;
