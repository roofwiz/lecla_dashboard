import React from 'react';
import TaskList from '../components/TaskList';

function Tasks() {
    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ marginBottom: '2rem' }}>
                <h1>Tasks & To-Do</h1>
                <p style={{ color: 'var(--color-text-muted)' }}>Manage all tasks and follow-ups</p>
            </div>

            <div className="card">
                <TaskList />
            </div>
        </div>
    );
}

export default Tasks;
