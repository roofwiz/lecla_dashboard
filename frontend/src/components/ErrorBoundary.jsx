import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error("Uncaught error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: '40px', textAlign: 'center', color: 'white', background: '#1e293b', borderRadius: '12px', margin: '20px' }}>
                    <h2>Oops! Something went wrong.</h2>
                    <p style={{ color: '#94a3b8', margin: '10px 0' }}>The dashboard encountered an error while rendering.</p>
                    <button
                        onClick={() => window.location.reload()}
                        style={{ padding: '8px 16px', background: 'var(--color-primary)', border: 'none', borderRadius: '4px', cursor: 'pointer', color: 'white' }}
                    >
                        Reload Page
                    </button>
                    {process.env.NODE_ENV === 'development' && (
                        <pre style={{ textAlign: 'left', background: '#0f172a', padding: '15px', marginTop: '20px', borderRadius: '6px', fontSize: '12px', overflow: 'auto' }}>
                            {this.state.error?.toString()}
                        </pre>
                    )}
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
