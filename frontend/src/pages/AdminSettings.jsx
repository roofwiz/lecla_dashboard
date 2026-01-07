import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './AdminSettings.css';

function AdminSettings() {
    const { user } = useAuth();
    const [activeTab, setActiveTab] = useState('users');

    if (user?.role !== 'admin' && user?.role !== 'owner') {
        return <div className="no-access">Access Denied. You do not have administrative privileges.</div>;
    }

    return (
        <div className="admin-container">
            <header className="admin-header">
                <h2>Administrative Settings</h2>
                <div className="admin-tabs">
                    <button
                        className={activeTab === 'users' ? 'active' : ''}
                        onClick={() => setActiveTab('users')}
                    >👥 User Management</button>
                    <button
                        className={activeTab === 'sync' ? 'active' : ''}
                        onClick={() => setActiveTab('sync')}
                    >🔄 Sync Control</button>
                    <button
                        className={activeTab === 'system' ? 'active' : ''}
                        onClick={() => setActiveTab('system')}
                    >⚙️ System Config</button>
                </div>
            </header>

            <div className="admin-content">
                {activeTab === 'users' && (
                    <div className="admin-section">
                        <div className="section-header">
                            <h3>Lecla Team Members</h3>
                            <button className="add-btn">+ Add Team Member</button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{user.full_name}</td>
                                    <td>{user.email}</td>
                                    <td><span className="role-badge" data-role={user.role}>{user.role}</span></td>
                                    <td><span className="status-active">Active</span></td>
                                    <td><button className="edit-btn">Edit</button></td>
                                </tr>
                                {/* Stub for more users */}
                            </tbody>
                        </table>
                        <div className="role-guide">
                            <h4>Role Guide:</h4>
                            <ul>
                                <li><strong>Owner</strong>: Unrestricted access.</li>
                                <li><strong>Admin</strong>: Office Manager. Manages users & billing.</li>
                                <li><strong>Production</strong>: Manages dumpsters and field crews.</li>
                                <li><strong>Sales</strong>: Focus on leads and estimators.</li>
                                <li><strong>Bookkeeper</strong>: Accounting and financial reports.</li>
                            </ul>
                        </div>
                    </div>
                )}

                {activeTab === 'sync' && (
                    <div className="admin-section">
                        <h3>JobNimbus Sync Status</h3>
                        <div className="sync-status-card">
                            <div className="status-indicator online">System Online</div>
                            <p>Last full sync: <strong>2 hours ago</strong></p>
                            <div className="sync-controls">
                                <button className="sync-now-btn">Force Full Sync Now</button>
                                <p className="help-text">Syncs all JobNimbus records, custom fields, and associations.</p>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'system' && (
                    <div className="admin-section">
                        <h3>Lead Routing & System Configuration</h3>
                        <p>Configure automated lead routing based on the company directory logic.</p>
                        {/* More settings here */}
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdminSettings;
