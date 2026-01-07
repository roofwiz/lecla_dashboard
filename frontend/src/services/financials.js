import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

// Attach JWT token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

/**
 * Calculate financials for a job
 * Returns calculated values from invoices and budgets
 */
export const calculateJobFinancials = async (jobId) => {
    const { data } = await api.post(`/financials/calculate/${jobId}`);
    return data;
};

/**
 * Get cached financial data for a job
 */
export const getJobFinancials = async (jobId) => {
    const { data } = await api.get(`/financials/job/${jobId}`);
    return data;
};

/**
 * Sync financials back to JobNimbus
 */
export const syncFinancialsToJobNimbus = async (jobId) => {
    const { data } = await api.post(`/financials/sync/${jobId}`);
    return data;
};

export default {
    calculateJobFinancials,
    getJobFinancials,
    syncFinancialsToJobNimbus
};
