import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, fetchMe } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Login.css';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { loginUser } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            console.log("Login: Attempting login for", email);
            const authData = await login(email, password);
            console.log("Login: Success, fetching user data...");
            const userData = await fetchMe(authData.access_token);
            console.log("Login: User data received", userData);
            loginUser(authData.access_token, userData);
            console.log("Login: Navigating to dashboard...");
            navigate('/');
        } catch (err) {
            console.error("Login Error:", err);
            setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className="login-logo">
                    <h1>LECLA<span>.</span></h1>
                    <p>Internal CRM Portal</p>
                </div>

                <form onSubmit={handleSubmit}>
                    {error && <div className="login-error">{error}</div>}

                    <div className="form-group">
                        <label>Email Address</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="name@lecla.com"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <button type="submit" className="login-btn" disabled={loading}>
                        {loading ? 'Authenticating...' : 'Sign In'}
                    </button>
                </form>

                <div className="login-footer">
                    <p>© 2026 Lecla Home & Roofing. Authorized Access Only.</p>
                </div>
            </div>
        </div>
    );
}

export default Login;
