import React from 'react';
import { openJobNimbusWindow } from '../utils/jobnimbusWindow';

/**
 * JobNimbus link button component
 * Opens JobNimbus record in controlled popup window
 */
function JobNimbusButton({ type, id, title, size = 'medium', className = '' }) {
    if (!id) return null;

    const handleClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        openJobNimbusWindow(type, id, title);
    };

    const sizeClasses = {
        small: 'jn-btn-sm',
        medium: 'jn-btn-md',
        large: 'jn-btn-lg'
    };

    return (
        <button
            onClick={handleClick}
            className={`jn-link-btn ${sizeClasses[size]} ${className}`}
            title={`Open ${title || type} in JobNimbus`}
            style={{
                padding: size === 'small' ? '4px 8px' : '6px 12px',
                background: 'rgba(59, 130, 246, 0.1)',
                border: '1px solid rgba(59, 130, 246, 0.3)',
                borderRadius: '6px',
                color: '#60a5fa',
                fontSize: size === 'small' ? '0.75rem' : '0.875rem',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)';
                e.currentTarget.style.borderColor = '#3b82f6';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)';
                e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.3)';
            }}
        >
            {/* JobNimbus icon */}
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                <polyline points="15 3 21 3 21 9" />
                <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            JN
        </button>
    );
}

/**
 * Compact icon-only version
 */
export function JobNimbusIcon({ type, id, title }) {
    if (!id) return null;

    const handleClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        openJobNimbusWindow(type, id, title);
    };

    return (
        <button
            onClick={handleClick}
            className="jn-icon-btn"
            title={`Open in JobNimbus`}
            style={{
                padding: '6px',
                background: 'transparent',
                border: 'none',
                borderRadius: '4px',
                color: '#60a5fa',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
            }}
        >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                <polyline points="15 3 21 3 21 9" />
                <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
        </button>
    );
}

export default JobNimbusButton;
