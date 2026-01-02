import React from 'react';
import './Header.css';

const Header = ({ title }) => {
    return (
        <header className="header">
            <h1 className="page-title">{title}</h1>

            <div className="header-actions">
                <button className="icon-btn">
                    🔔 <span className="badge">3</span>
                </button>
                <div className="user-profile">
                    <div className="avatar">JS</div>
                    <div className="user-info">
                        <span className="user-name">John Smith</span>
                        <span className="user-role">Admin</span>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
