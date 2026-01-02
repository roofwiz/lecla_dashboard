import axios from 'axios';

// Base instance
const api = axios.create({
    baseURL: 'http://localhost:8000/api', // Pointing to our FastAPI backend
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// API Calls
export const fetchJobs = async (limit = 10) => {
    try {
        const response = await api.get('/jobs', { params: { limit } });
        return response.data;
    } catch (error) {
        console.error("API Error fetching jobs:", error);
        throw error;
    }
};

export const fetchProjects = async (limit = 25) => {
    try {
        const response = await api.get('/projects', { params: { limit } });
        return response.data;
    } catch (error) {
        console.error("API Error fetching projects:", error);
        throw error;
    }
};

export const fetchCalendar = async (limit = 10) => {
    try {
        const response = await api.get('/calendar', { params: { limit } });
        return response.data; // Standard Google API response structure might be different, but our backend sends the 'items' list directly
    } catch (error) {
        console.error("API Error fetching calendar:", error);
        throw error;
    }
};

export default api;
