import React, { useState, useEffect } from 'react';
import { fetchTasks, createTask, updateTask, deleteTask } from '../services/tasks';

function TaskList({ relatedToType = null, relatedToId = null }) {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);
    const [newTask, setNewTask] = useState({
        title: '',
        description: '',
        due_date: '',
        priority: 'medium'
    });

    const loadTasks = async () => {
        setLoading(true);
        try {
            const params = {};
            if (relatedToType) params.related_to_type = relatedToType;
            if (relatedToId) params.related_to_id = relatedToId;

            const data = await fetchTasks(params);
            setTasks(data);
        } catch (err) {
            console.error('Failed to load tasks', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadTasks();
    }, [relatedToType, relatedToId]);

    const handleAddTask = async (e) => {
        e.preventDefault();
        try {
            await createTask({
                ...newTask,
                related_to_type: relatedToType,
                related_to_id: relatedToId,
                due_date: newTask.due_date ? Math.floor(new Date(newTask.due_date).getTime() / 1000) : null
            });
            setNewTask({ title: '', description: '', due_date: '', priority: 'medium' });
            setShowAddForm(false);
            loadTasks();
        } catch (err) {
            console.error('Failed to create task', err);
            alert('Failed to create task');
        }
    };

    const handleToggleComplete = async (task) => {
        try {
            const newStatus = task.status === 'completed' ? 'pending' : 'completed';
            await updateTask(task.lecla_id, { status: newStatus });
            loadTasks();
        } catch (err) {
            console.error('Failed to update task', err);
        }
    };

    const handleDeleteTask = async (taskId) => {
        if (!confirm('Are you sure you want to delete this task?')) return;
        try {
            await deleteTask(taskId);
            loadTasks();
        } catch (err) {
            console.error('Failed to delete task', err);
        }
    };

    const formatDate = (timestamp) => {
        if (!timestamp) return '';
        return new Date(timestamp * 1000).toLocaleDateString();
    };

    const getPriorityColor = (priority) => {
        const colors = {
            low: '#10b981',
            medium: '#f59e0b',
            high: '#ef4444',
            urgent: '#dc2626'
        };
        return colors[priority] || colors.medium;
    };

    if (loading) return <div style={{ padding: '20px' }}>Loading tasks...</div>;

    return (
        <div className="task-list">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3>Tasks ({tasks.length})</h3>
                <button
                    onClick={() => setShowAddForm(!showAddForm)}
                    style={{
                        padding: '8px 16px',
                        background: 'var(--color-accent)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer'
                    }}
                >
                    {showAddForm ? 'Cancel' : '+ Add Task'}
                </button>
            </div>

            {showAddForm && (
                <form onSubmit={handleAddTask} style={{ marginBottom: '20px', padding: '15px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                    <input
                        type="text"
                        placeholder="Task title *"
                        value={newTask.title}
                        onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                        required
                        style={{ width: '100%', padding: '10px', marginBottom: '10px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '4px' }}
                    />
                    <textarea
                        placeholder="Description (optional)"
                        value={newTask.description}
                        onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                        style={{ width: '100%', padding: '10px', marginBottom: '10px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '4px', minHeight: '60px' }}
                    />
                    <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                        <input
                            type="date"
                            value={newTask.due_date}
                            onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
                            style={{ flex: 1, padding: '10px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '4px' }}
                        />
                        <select
                            value={newTask.priority}
                            onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                            style={{ flex: 1, padding: '10px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '4px' }}
                        >
                            <option value="low">Low Priority</option>
                            <option value="medium">Medium Priority</option>
                            <option value="high">High Priority</option>
                            <option value="urgent">Urgent</option>
                        </select>
                    </div>
                    <button type="submit" style={{ padding: '10px 20px', background: '#10b981', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                        Create Task
                    </button>
                </form>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {tasks.map(task => (
                    <div
                        key={task.lecla_id}
                        style={{
                            padding: '15px',
                            background: task.status === 'completed' ? 'rgba(255,255,255,0.02)' : 'rgba(255,255,255,0.05)',
                            border: `1px solid ${getPriorityColor(task.priority)}33`,
                            borderRadius: '8px',
                            borderLeft: `4px solid ${getPriorityColor(task.priority)}`,
                            opacity: task.status === 'completed' ? 0.6 : 1
                        }}
                    >
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                            <input
                                type="checkbox"
                                checked={task.status === 'completed'}
                                onChange={() => handleToggleComplete(task)}
                                style={{ marginTop: '4px', cursor: 'pointer', width: '18px', height: '18px' }}
                            />
                            <div style={{ flex: 1 }}>
                                <div style={{ fontWeight: '500', marginBottom: '5px', textDecoration: task.status === 'completed' ? 'line-through' : 'none' }}>
                                    {task.title}
                                </div>
                                {task.description && (
                                    <div style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: '8px' }}>
                                        {task.description}
                                    </div>
                                )}
                                <div style={{ display: 'flex', gap: '15px', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                    {task.due_date && (
                                        <span>📅 Due: {formatDate(task.due_date)}</span>
                                    )}
                                    <span style={{ color: getPriorityColor(task.priority), fontWeight: '500' }}>
                                        {task.priority.toUpperCase()}
                                    </span>
                                </div>
                            </div>
                            <button
                                onClick={() => handleDeleteTask(task.lecla_id)}
                                style={{
                                    padding: '6px 10px',
                                    background: 'transparent',
                                    color: '#ef4444',
                                    border: '1px solid #ef444433',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    fontSize: '0.75rem'
                                }}
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                ))}
                {tasks.length === 0 && (
                    <div style={{ padding: '40px', textAlign: 'center', color: 'var(--color-text-muted)' }}>
                        No tasks yet. Click "+ Add Task" to create one.
                    </div>
                )}
            </div>
        </div>
    );
}

export default TaskList;
