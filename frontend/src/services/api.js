import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Attach token to all requests
api.interceptors.request.use(config => {
    const token = localStorage.getItem('lecla_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
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

export const login = async (email, password) => {
    // OAuth2PasswordRequestForm expects x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    const resp = await axios.post(`${API_BASE_URL}/auth/login`, params, { timeout: 15000 });
    return resp.data;
};

export const registerUser = async (userData) => {
    const resp = await axios.post(`${API_BASE_URL}/auth/register`, userData, { timeout: 15000 });
    return resp.data;
};

export const fetchMe = async (token) => {
    const resp = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 10000
    });
    return resp.data;
};

export const fetchCRMContacts = async () => {
    try {
        const response = await api.get('/crm/contacts');
        return response.data;
    } catch (error) {
        console.error("API Error fetching CRM contacts:", error);
        throw error;
    }
};

export const fetchCRMJobs = async () => {
    try {
        const response = await api.get('/crm/jobs');
        return response.data;
    } catch (error) {
        console.error("API Error fetching CRM jobs:", error);
        throw error;
    }
};

export const triggerSync = async () => {
    try {
        const response = await api.post('/crm/sync');
        return response.data;
    } catch (error) {
        console.error("API Error triggering sync:", error);
        throw error;
    }
};

export default api;
