import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // Increased to 30s for slow Google Sheet responses
    headers: {
        'Content-Type': 'application/json',
    }
});

export const fetchJobs = async () => {
    try {
        const response = await api.get('/jobs');
        return response.data;
    } catch (error) {
        console.error("API Error fetching jobs:", error);
        throw error;
    }
};

export const fetchProjects = async () => {
    try {
        const response = await api.get('/projects?limit=25');
        return response.data;
    } catch (error) {
        console.error("API Error fetching projects:", error);
        throw error;
    }
};

export const fetchCalendar = async () => {
    try {
        const response = await api.get('/calendar/events');
        return response.data;
    } catch (error) {
        console.error("API Error fetching calendar:", error);
        throw error;
    }
};

export const fetchSalesReports = async (year) => {
    try {
        const response = await api.get('/reports/sales-by-rep', { params: { year } });
        return response.data;
    } catch (error) {
        console.error("API Error fetching sales:", error);
        throw error;
    }
};

export default api;
