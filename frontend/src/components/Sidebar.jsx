import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
    const location = useLocation();

    // Helper to check active class
    const isActive = (path) => location.pathname === path ? 'active' : '';

    return (
        <aside className="sidebar">
            <div className="logo-container">
                <h2 className="brand-logo">LECLA<span className="brand-dot">.</span></h2>
                <p className="brand-sub">Home & Roofing</p>
            </div>

            <nav className="nav-menu">
                <Link to="/" className={`nav-item ${isActive('/')}`}>
                    <span className="icon">🏠</span>
                    <span className="label">Dashboard</span>
                </Link>
                <Link to="/reports" className={`nav-item ${isActive('/reports')}`}>
                    <span className="icon">📊</span>
                    <span className="label">Sales Reports</span>
                </Link>
                <a href="#" className="nav-item">
                    <span className="icon">🔨</span>
                    <span className="label">Jobs</span>
                </a>
                <a href="#" className="nav-item">
                    <span className="icon">📷</span>
                    <span className="label">Photos</span>
                </a>
                <a href="#" className="nav-item">
                    <span className="icon">📅</span>
                    <span className="label">Schedule</span>
                </a>
            </nav>

            <div className="nav-footer">
                <a href="#" className="nav-item">
                    <span className="icon">⚙️</span>
                    <span className="label">Settings</span>
                </a>
            </div>
        </aside>
    );
};

export default Sidebar;
