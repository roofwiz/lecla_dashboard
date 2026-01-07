import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import AiAgent from '../components/AiAgent';
import './DashboardLayout.css';

const DashboardLayout = ({ title = "Overview" }) => {
    console.log("DashboardLayout: Rendering with title", title);
    return (
        <div className="layout-container">
            <Sidebar />
            <main className="main-content">
                <Header title={title} />
                <div className="content-scrollable">
                    <div className="content-area">
                        <Outlet />
                    </div>
                </div>
            </main>
            <AiAgent />
        </div>
    );
};

export default DashboardLayout;
