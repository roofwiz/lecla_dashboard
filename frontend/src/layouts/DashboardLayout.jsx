import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import './DashboardLayout.css';

const DashboardLayout = ({ children, title = "Overview" }) => {
    return (
        <div className="layout-container">
            <Sidebar />
            <main className="main-content">
                <Header title={title} />
                <div className="content-scrollable">
                    <div className="content-area">
                        {children}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default DashboardLayout;
