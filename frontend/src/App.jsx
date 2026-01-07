import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import Contacts from './pages/Contacts';
import CRMJobs from './pages/CRMJobs';
import Directory from './pages/Directory';
import AdminSettings from './pages/AdminSettings';
import Photos from './pages/Photos';
import Schedule from './pages/Schedule';
import Audit from './pages/Audit';
import Tasks from './pages/Tasks';
import Board from './pages/Board';
import Financials from './pages/Financials';
import Timeline from './pages/Timeline';
import Login from './pages/Login';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css';

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <ProtectedRoute>
                <DashboardLayout title="Lecla Dashboard" />
              </ProtectedRoute>
            }>
              <Route index element={<Dashboard />} />
              <Route path="reports" element={<Reports />} />
              <Route path="contacts" element={<Contacts />} />
              <Route path="jobs" element={<CRMJobs />} />
              <Route path="board" element={<Board />} />
              <Route path="financials" element={<Financials />} />
              <Route path="timeline" element={<Timeline />} />
              <Route path="directory" element={<Directory />} />
              <Route path="photos" element={<Photos />} />
              <Route path="schedule" element={<Schedule />} />
              <Route path="audit" element={<Audit />} />
              <Route path="tasks" element={<Tasks />} />
              <Route path="settings" element={<AdminSettings />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
