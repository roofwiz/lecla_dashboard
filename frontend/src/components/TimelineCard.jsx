import React, { useState } from 'react';

/**
 * Folio-style vertical timeline component
 * Shows project milestones with visual status indicators
 */
function TimelineCard({ timeline, onDateChange, onSync, loading = false }) {
    const [editingStep, setEditingStep] = useState(null);
    const [tempDate, setTempDate] = useState('');
    const [showCascadeModal, setShowCascadeModal] = useState(false);
    const [cascadeData, setCascadeData] = useState(null);

    if (!timeline || timeline.length === 0) {
        return (
            <div className="card" style={{ padding: '20px' }}>
                <h3>📅 Timeline</h3>
                <p style={{ color: 'var(--color-text-muted)' }}>No timeline data available</p>
            </div>
        );
    }

    const formatDate = (date) => {
        if (!date) return '';
        return new Date(date).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    };

    const getStatusColor = (status) => {
        const colors = {
            completed: '#10b981',
            today: '#3b82f6',
            pending: '#64748b',
            overdue: '#ef4444'
        };
        return colors[status] || colors.pending;
    };

    const getStatusIcon = (status) => {
        if (status === 'completed') return '✓';
        if (status === 'today') return '◉';
        if (status === 'overdue') return '!';
        return '○';
    };

    const handleDateEdit = (step, index) => {
        const dateToEdit = step.actualDate || step.calculatedDate;
        const dateString = new Date(dateToEdit).toISOString().split('T')[0];
        setTempDate(dateString);
        setEditingStep(index);
    };

    const handleDateSave = (step, index) => {
        const newDate = new Date(tempDate);
        const originalDate = step.actualDate || step.calculatedDate;

        // Check if this should trigger cascade
        const isSignificantChange = Math.abs(newDate - originalDate) / (1000 * 60 * 60 * 24) >= 1;
        const hasSubsequentSteps = index < timeline.length - 1;

        if (isSignificantChange && hasSubsequentSteps && !step.isAnchor) {
            // Show cascade confirmation
            setCascadeData({ step, index, newDate, originalDate });
            setShowCascadeModal(true);
        } else {
            // Just update this step
            onDateChange(index, newDate, false);
            setEditingStep(null);
        }
    };

    const handleCascadeConfirm = (shouldCascade) => {
        if (cascadeData) {
            onDateChange(cascadeData.index, cascadeData.newDate, shouldCascade);
        }
        setShowCascadeModal(false);
        setCascadeData(null);
        setEditingStep(null);
    };

    return (
        <div className="card timeline-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center', marginBottom: '20px' }}>
                <div>
                    <h3 style={{ margin: 0, marginBottom: '5px' }}>📅 Project Timeline</h3>
                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                        Folio-style milestone tracking
                    </p>
                </div>
                {onSync && (
                    <button
                        onClick={onSync}
                        disabled={loading}
                        style={{
                            padding: '8px 16px',
                            background: 'var(--color-accent)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading ? 0.6 : 1,
                            fontSize: '0.875rem',
                            fontWeight: '600'
                        }}
                    >
                        {loading ? 'Syncing...' : 'Sync to JobNimbus'}
                    </button>
                )}
            </div>

            {/* Timeline Steps */}
            <div style={{ position: 'relative' }}>
                {/* Vertical line */}
                <div style={{
                    position: 'absolute',
                    left: '15px',
                    top: '10px',
                    bottom: '10px',
                    width: '2px',
                    background: 'linear-gradient(180deg, rgba(59, 130, 246, 0.3) 0%, rgba(100, 116, 139, 0.3) 100%)'
                }} />

                {/* Steps */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    {timeline.map((step, index) => (
                        <div
                            key={step.id}
                            style={{
                                position: 'relative',
                                paddingLeft: '50px',
                                display: 'flex',
                                alignItems: 'start',
                                gap: '15px'
                            }}
                        >
                            {/* Status dot */}
                            <div style={{
                                position: 'absolute',
                                left: 0,
                                top: '2px',
                                width: '32px',
                                height: '32px',
                                borderRadius: '50%',
                                background: getStatusColor(step.status),
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '1rem',
                                fontWeight: '700',
                                color: 'white',
                                boxShadow: `0 0 0 4px rgba(0,0,0,0.5), 0 0 12px ${getStatusColor(step.status)}55`,
                                zIndex: 2
                            }}>
                                {getStatusIcon(step.status)}
                            </div>

                            {/* Step content */}
                            <div style={{ flex: 1 }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '6px' }}>
                                    <div>
                                        <div style={{ fontSize: '0.95rem', fontWeight: '600', marginBottom: '3px' }}>
                                            {step.name}
                                            {step.isAnchor && (
                                                <span style={{
                                                    marginLeft: '8px',
                                                    fontSize: '0.7rem',
                                                    padding: '2px 6px',
                                                    background: 'rgba(59, 130, 246, 0.2)',
                                                    color: '#60a5fa',
                                                    borderRadius: '4px',
                                                    fontWeight: '600'
                                                }}>
                                                    ANCHOR
                                                </span>
                                            )}
                                        </div>
                                        {step.description && (
                                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                                {step.description}
                                            </div>
                                        )}
                                    </div>

                                    {/* Date display/editor */}
                                    {editingStep === index ? (
                                        <div style={{ display: 'flex', gap: '6px' }}>
                                            <input
                                                type="date"
                                                value={tempDate}
                                                onChange={(e) => setTempDate(e.target.value)}
                                                style={{
                                                    padding: '4px 8px',
                                                    background: 'rgba(255,255,255,0.1)',
                                                    border: '1px solid #3b82f6',
                                                    borderRadius: '4px',
                                                    color: 'white',
                                                    fontSize: '0.875rem'
                                                }}
                                                autoFocus
                                            />
                                            <button
                                                onClick={() => handleDateSave(step, index)}
                                                style={{
                                                    padding: '4px 8px',
                                                    background: '#10b981',
                                                    border: 'none',
                                                    borderRadius: '4px',
                                                    color: 'white',
                                                    cursor: 'pointer',
                                                    fontSize: '0.75rem'
                                                }}
                                            >
                                                ✓
                                            </button>
                                            <button
                                                onClick={() => setEditingStep(null)}
                                                style={{
                                                    padding: '4px 8px',
                                                    background: '#64748b',
                                                    border: 'none',
                                                    borderRadius: '4px',
                                                    color: 'white',
                                                    cursor: 'pointer',
                                                    fontSize: '0.75rem'
                                                }}
                                            >
                                                ✕
                                            </button>
                                        </div>
                                    ) : (
                                        <div
                                            onClick={() => onDateChange && handleDateEdit(step, index)}
                                            style={{
                                                padding: '6px 10px',
                                                background: step.actualDate ? 'rgba(16, 185, 129, 0.1)' : 'rgba(100, 116, 139, 0.1)',
                                                border: `1px solid ${step.actualDate ? '#10b98144' : 'rgba(255,255,255,0.1)'}`,
                                                borderRadius: '6px',
                                                fontSize: '0.875rem',
                                                fontWeight: '600',
                                                color: step.actualDate ? '#10b981' : 'var(--color-text-muted)',
                                                cursor: onDateChange ? 'pointer' : 'default',
                                                transition: 'all 0.2s ease'
                                            }}
                                            onMouseEnter={(e) => {
                                                if (onDateChange) {
                                                    e.currentTarget.style.borderColor = '#3b82f6';
                                                }
                                            }}
                                            onMouseLeave={(e) => {
                                                if (onDateChange) {
                                                    e.currentTarget.style.borderColor = step.actualDate ? '#10b98144' : 'rgba(255,255,255,0.1)';
                                                }
                                            }}
                                        >
                                            {formatDate(step.actualDate || step.calculatedDate)}
                                            {!step.actualDate && ' (calc)'}
                                        </div>
                                    )}
                                </div>

                                {/* Status badges */}
                                <div style={{ display: 'flex', gap: '8px', marginTop: '8px', flexWrap: 'wrap' }}>
                                    {step.status === 'overdue' && (
                                        <span style={{
                                            fontSize: '0.7rem',
                                            padding: '2px 8px',
                                            background: 'rgba(239, 68, 68, 0.2)',
                                            color: '#ef4444',
                                            borderRadius: '12px',
                                            fontWeight: '600'
                                        }}>
                                            OVERDUE
                                        </span>
                                    )}
                                    {step.isSynced && step.relatedField && (
                                        <span style={{
                                            fontSize: '0.7rem',
                                            padding: '2px 8px',
                                            background: 'rgba(59, 130, 246, 0.1)',
                                            color: '#60a5fa',
                                            borderRadius: '12px'
                                        }}>
                                            ↻ Syncs to JN
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Cascade Modal */}
            {showCascadeModal && cascadeData && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0,0,0,0.7)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 1000
                }}>
                    <div style={{
                        background: '#1e293b',
                        padding: '30px',
                        borderRadius: '12px',
                        maxWidth: '500px',
                        border: '1px solid rgba(255,255,255,0.1)'
                    }}>
                        <h3 style={{ marginTop: 0 }}>⚡ Cascade Update?</h3>
                        <p style={{ color: 'var(--color-text-muted)', marginBottom: '20px' }}>
                            You've changed <strong>{cascadeData.step.name}</strong> by{' '}
                            <strong>{Math.round((cascadeData.newDate - cascadeData.originalDate) / (1000 * 60 * 60 * 24))} days</strong>.
                        </p>
                        <p style={{ color: 'var(--color-text-muted)', marginBottom: '25px' }}>
                            Would you like to shift all <strong>subsequent dates</strong> by the same amount?
                        </p>
                        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                            <button
                                onClick={() => handleCascadeConfirm(false)}
                                style={{
                                    padding: '10px 20px',
                                    background: 'rgba(255,255,255,0.1)',
                                    border: '1px solid rgba(255,255,255,0.2)',
                                    borderRadius: '6px',
                                    color: 'white',
                                    cursor: 'pointer',
                                    fontWeight: '600'
                                }}
                            >
                                No, just this step
                            </button>
                            <button
                                onClick={() => handleCascadeConfirm(true)}
                                style={{
                                    padding: '10px 20px',
                                    background: '#10b981',
                                    border: 'none',
                                    borderRadius: '6px',
                                    color: 'white',
                                    cursor: 'pointer',
                                    fontWeight: '600'
                                }}
                            >
                                Yes, cascade all
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TimelineCard;
