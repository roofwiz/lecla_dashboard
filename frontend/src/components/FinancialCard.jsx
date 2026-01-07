import React from 'react';

/**
 * Financial Summary Card
 * Shows revenue breakdown with pass-through fees and profit margins
 */
function FinancialCard({ financials, compact = false }) {
    if (!financials) {
        return (
            <div className="card" style={{ padding: '20px' }}>
                <h3>Financials</h3>
                <p style={{ color: 'var(--color-text-muted)' }}>Loading financial data...</p>
            </div>
        );
    }

    const {
        total_invoiced = 0,
        permit_fee = 0,
        financing_fee = 0,
        total_project = 0,
        total_gross = 0,
        total_net = 0,
        commissions = 0
    } = financials;

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(amount || 0);
    };

    const calculateMargin = (net, revenue) => {
        if (!revenue || revenue === 0) return 0;
        return ((net / revenue) * 100).toFixed(1);
    };

    const marginPercent = calculateMargin(total_net, total_project);
    const totalPassThrough = permit_fee + financing_fee;

    return (
        <div className="card financial-card" style={{
            padding: compact ? '15px' : '20px',
            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%)'
        }}>
            <div style={{ marginBottom: '20px' }}>
                <h3 style={{ margin: 0, marginBottom: '5px' }}>💰 Financials</h3>
                {!compact && (
                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                        Revenue, margins, and fees
                    </p>
                )}
            </div>

            {/* Revenue Breakdown */}
            <div style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
                    <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>Total Invoiced</span>
                    <span style={{ fontSize: '1.25rem', fontWeight: '600', color: '#60a5fa' }}>
                        {formatCurrency(total_invoiced)}
                    </span>
                </div>

                {/* Pass-through fees */}
                {totalPassThrough > 0 && (
                    <>
                        <div style={{
                            padding: '10px',
                            background: 'rgba(239, 68, 68, 0.1)',
                            borderLeft: '3px solid #ef4444',
                            borderRadius: '4px',
                            marginBottom: '10px'
                        }}>
                            <div style={{ fontSize: '0.75rem', fontWeight: '600', color: '#ef4444', marginBottom: '5px' }}>
                                Pass-Through Fees (Not Revenue)
                            </div>
                            {permit_fee > 0 && (
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', marginBottom: '3px' }}>
                                    <span style={{ color: 'var(--color-text-muted)' }}>Permit Fee</span>
                                    <span style={{ color: '#ef4444' }}>-{formatCurrency(permit_fee)}</span>
                                </div>
                            )}
                            {financing_fee > 0 && (
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                                    <span style={{ color: 'var(--color-text-muted)' }}>Financing Fee</span>
                                    <span style={{ color: '#ef4444' }}>-{formatCurrency(financing_fee)}</span>
                                </div>
                            )}
                        </div>
                    </>
                )}

                {/* Effective Revenue */}
                <div style={{
                    padding: '12px',
                    background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%)',
                    borderLeft: '4px solid #10b981',
                    borderRadius: '4px'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                        <div>
                            <div style={{ fontSize: '0.75rem', fontWeight: '600', color: '#10b981', marginBottom: '2px' }}>
                                EFFECTIVE REVENUE
                            </div>
                            <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>
                                True Top Line
                            </div>
                        </div>
                        <span style={{ fontSize: '1.5rem', fontWeight: '700', color: '#10b981' }}>
                            {formatCurrency(total_project)}
                        </span>
                    </div>
                </div>
            </div>

            {/* Profit Margins */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: compact ? '1fr' : 'repeat(2, 1fr)',
                gap: '10px',
                marginBottom: '15px'
            }}>
                <div style={{ padding: '12px', background: 'rgba(251, 146, 60, 0.1)', borderRadius: '6px' }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>
                        Gross Profit
                    </div>
                    <div style={{ fontSize: '1.125rem', fontWeight: '600', color: '#fb923c' }}>
                        {formatCurrency(total_gross)}
                    </div>
                </div>

                <div style={{ padding: '12px', background: 'rgba(139, 92, 246, 0.1)', borderRadius: '6px' }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>
                        Net Profit
                    </div>
                    <div style={{ fontSize: '1.125rem', fontWeight: '600', color: '#8b5cf6' }}>
                        {formatCurrency(total_net)}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>
                        {marginPercent}% margin
                    </div>
                </div>
            </div>

            {/* Commissions */}
            {commissions > 0 && (
                <div style={{
                    padding: '10px',
                    background: 'rgba(234, 179, 8, 0.1)',
                    borderRadius: '6px',
                    border: '1px solid rgba(234, 179, 8, 0.2)'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                Total Commissions
                            </div>
                            <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', fontStyle: 'italic' }}>
                                From budget
                            </div>
                        </div>
                        <span style={{ fontSize: '1rem', fontWeight: '600', color: '#eab308' }}>
                            {formatCurrency(commissions)}
                        </span>
                    </div>
                </div>
            )}

            {/* Quick Insights */}
            {!compact && (
                <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '8px', fontWeight: '600' }}>
                        💡 INSIGHTS
                    </div>
                    {marginPercent > 40 && (
                        <div style={{ fontSize: '0.75rem', color: '#10b981', marginBottom: '4px' }}>
                            ✓ Excellent margin ({marginPercent}%)
                        </div>
                    )}
                    {totalPassThrough > 0 && (
                        <div style={{ fontSize: '0.75rem', color: '#f59e0b', marginBottom: '4px' }}>
                            ⚠ {formatCurrency(totalPassThrough)} in pass-through fees
                        </div>
                    )}
                    {commissions > 0 && total_net > 0 && (
                        <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                            → Commission is {((commissions / total_net) * 100).toFixed(1)}% of net profit
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default FinancialCard;
