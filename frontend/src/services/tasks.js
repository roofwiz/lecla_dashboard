import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

// Attach JWT token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Tasks API
export const fetchTasks = async (params = {}) => {
    const { data } = await api.get('/tasks', { params });
    return data;
};

export const createTask = async (taskData) => {
    const { data } = await api.post('/tasks', taskData);
    return data;
};

export const updateTask = async (taskId, taskData) => {
    const { data } = await api.put(`/tasks/${taskId}`, taskData);
    return data;
};

export const deleteTask = async (taskId) => {
    const { data } = await api.delete(`/tasks/${taskId}`);
    return data;
};

export default {
    fetchTasks,
    createTask,
    updateTask,
    deleteTask
};
