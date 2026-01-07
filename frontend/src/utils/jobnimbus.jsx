/**
 * JobNimbus Integration Utilities
 * Provides helper functions for deep-linking to JobNimbus records
 */

const JOBNIMBUS_BASE_URL = 'https://app.jobnimbus.com';

/**
 * Generate a JobNimbus URL for a specific record
 * @param {string} entityType - 'jobs', 'contacts', 'budgets', 'estimates', 'invoices', 'tasks'
 * @param {string} jnid - JobNimbus ID (jnid)
 * @returns {string} Full URL to the record in JobNimbus
 */
export function getJobNimbusUrl(entityType, jnid) {
    if (!jnid) return null;
    return `${JOBNIMBUS_BASE_URL}/${entityType}/${jnid}`;
}

/**
 * Open a JobNimbus record in a new tab
 * @param {string} entityType - 'jobs', 'contacts', 'budgets', 'estimates', 'invoices', 'tasks'
 * @param {string} jnid - JobNimbus ID
 */
export function openInJobNimbus(entityType, jnid) {
    const url = getJobNimbusUrl(entityType, jnid);
    if (url) {
        window.open(url, '_blank', 'noopener,noreferrer');
    }
}

/**
 * JobNimbus Link Button Component
 * Renders a button that opens a record in JobNimbus
 */
export function JobNimbusLinkButton({ entityType, jnid, label = 'View in JobNimbus', variant = 'default', className = '' }) {
    if (!jnid) return null;

    const handleClick = (e) => {
        e.stopPropagation(); // Prevent row click if in table
        openInJobNimbus(entityType, jnid);
    };

    const buttonStyles = {
        default: {
            padding: '8px 16px',
            background: 'rgba(74, 144, 226, 0.1)',
            color: '#4a90e2',
            border: '1px solid rgba(74, 144, 226, 0.3)',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: '500',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s ease'
        },
        icon: {
            padding: '6px',
            background: 'transparent',
            color: '#4a90e2',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            transition: 'all 0.2s ease'
        },
        primary: {
            padding: '10px 20px',
            background: '#4a90e2',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: '600',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s ease'
        }
    };

    return (
        <button
            onClick={handleClick}
            style={buttonStyles[variant]}
            className={`jn-link-btn ${className}`}
            title={`Open in JobNimbus (${entityType})`}
        >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                <polyline points="15 3 21 3 21 9" />
                <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            {variant !== 'icon' && <span>{label}</span>}
        </button>
    );
}

/**
 * Small icon-only link (for table rows)
 */
export function JobNimbusIcon({ entityType, jnid }) {
    return <JobNimbusLinkButton entityType={entityType} jnid={jnid} variant="icon" />;
}

/**
 * Styled link component for inline use
 */
export function JobNimbusLink({ entityType, jnid, children }) {
    if (!jnid) return children;

    const url = getJobNimbusUrl(entityType, jnid);

    return (
        <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
                color: '#4a90e2',
                textDecoration: 'none',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px'
            }}
            onClick={(e) => e.stopPropagation()}
        >
            {children}
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ opacity: 0.6 }}>
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                <polyline points="15 3 21 3 21 9" />
                <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
        </a>
    );
}
