import React from 'react';
import './Sidebar.css';

const Sidebar = () => {
    return (
        <aside className="sidebar">
            <div className="logo-container">
                <h2 className="brand-logo">LECLA<span className="brand-dot">.</span></h2>
                <p className="brand-sub">Home & Roofing</p>
            </div>

            <nav className="nav-menu">
                <a href="#" className="nav-item active">
                    <span className="icon">🏠</span>
                    <span className="label">Dashboard</span>
                </a>
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
