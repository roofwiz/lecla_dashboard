import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { logout, user } = useAuth();

    // Helper to check active class
    const isActive = (path) => location.pathname === path ? 'active' : '';

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <aside className="sidebar">
            <div className="logo-container">
                <img
                    src="/lecla-logo.png"
                    alt="Lecla Home & Roofing"
                    className="brand-logo-img"
                    style={{
                        width: '180px',
                        height: 'auto',
                        marginBottom: '8px',
                        filter: 'brightness(1.1)'
                    }}
                />
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
                <Link to="/contacts" className={`nav-item ${isActive('/contacts')}`}>
                    <span className="icon">👥</span>
                    <span className="label">Contacts</span>
                </Link>
                <Link to="/jobs" className={`nav-item ${isActive('/jobs')}`}>
                    <span className="icon">🔨</span>
                    <span className="label">Jobs</span>
                </Link>
                <Link to="/directory" className={`nav-item ${isActive('/directory')}`}>
                    <span className="icon">📂</span>
                    <span className="label">Directory</span>
                </Link>
                <Link to="/photos" className={`nav-item ${isActive('/photos')}`}>
                    <span className="icon">📷</span>
                    <span className="label">Photos</span>
                </Link>
                <Link to="/schedule" className={`nav-item ${isActive('/schedule')}`}>
                    <span className="icon">📅</span>
                    <span className="label">Schedule</span>
                </Link>
                <Link to="/audit" className={`nav-item ${isActive('/audit')}`}>
                    <span className="icon">🔍</span>
                    <span className="label">Data Quality</span>
                </Link>
            </nav>

            <div className="nav-footer">
                <div className="user-profile">
                    <div className="user-text">
                        <span className="user-name">{user?.full_name}</span>
                        <span className="user-role">{user?.role}</span>
                    </div>
                </div>
                <button
                    onClick={handleLogout}
                    className="logout-btn"
                >
                    <span className="icon">🔒</span>
                    <span className="label">Log Out</span>
                </button>
                <Link to="/settings" className={`nav-item ${isActive('/settings')}`}>
                    <span className="icon">⚙️</span>
                    <span className="label">Settings</span>
                </Link>
            </div>
        </aside>
    );
};

export default Sidebar;
