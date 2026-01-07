import React from 'react';
import KanbanBoard from '../components/KanbanBoard';

function Board() {
    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1>Job Board</h1>
                    <p style={{ color: 'var(--color-text-muted)' }}>Drag and drop jobs to update their status</p>
                </div>
                <button style={{
                    padding: '10px 20px',
                    background: 'var(--color-accent)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontWeight: '600'
                }}>
                    + New Job
                </button>
            </div>

            <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                <KanbanBoard />
            </div>
        </div>
    );
}

export default Board;
