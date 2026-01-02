import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import './App.css';

function App() {
  return (
    <Router>
      {/* Layout wraps the Routes so Sidebar/Header are always present */}
      <DashboardLayout title="Lecla Dashboard">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </DashboardLayout>
    </Router>
  );
}

export default App;
