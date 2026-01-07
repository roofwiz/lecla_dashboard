import React, { createContext, useState, useContext, useEffect } from 'react';
import { fetchMe } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const token = localStorage.getItem('lecla_token');
                if (token) {
                    const userData = await fetchMe(token);
                    setUser(userData);
                }
            } catch (err) {
                console.error("Auth initialization failed:", err);
                localStorage.removeItem('lecla_token');
            } finally {
                setLoading(false);
            }
        };
        checkAuth();
    }, []);

    const loginUser = (token, userData) => {
        localStorage.setItem('lecla_token', token);
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem('lecla_token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loginUser, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
