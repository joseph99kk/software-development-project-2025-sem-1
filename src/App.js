import logo from './makerere-logo.ico';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import IssueForm from './IssueForm';
import LecturerDashboard from './LecturerDashboard';
import RegistrarDashboard from './RegistrarDashboard';
import StudentDashboard from './StudentDashboard';
import Register from './Register';
import Login from './Login';
import WelcomePage from './WelcomePage'; // Import the WelcomePage component

function App() {
  return (
    <Router>
      <MainApp />
    </Router>
  );
}

function MainApp() {
  const location = useLocation(); // Get the current route

  // Define routes where the header should be hidden
  const hideHeaderRoutes = ['/register', '/login', '/lecturer-dashboard', '/student-dashboard', '/registrar-dashboard', '/welcome-page'];

  return (
    <div className="App">
      {/* Conditionally render the logo */}
      <div className="App-logo-container">
        <img
          src={logo}
          className="App-logo"
          alt="logo"
          style={{ width: '100px', height: '100px', borderRadius: '50%' }} // Example styling
        />
      </div>

      {/* Conditionally render the header */}
      {!hideHeaderRoutes.includes(location.pathname) && (
        <header className="App-header">
          <h1>Header Content</h1>
        </header>
      )}

      <Routes>
        <Route path="/welcome-page" element={<WelcomePage />} />
        <Route path="/" element={<IssueForm />} />
        <Route path="/lecturer-dashboard" element={<LecturerDashboard />} />
        <Route path="/registrar-dashboard" element={<RegistrarDashboard />} />
        <Route path="/student-dashboard" element={<StudentDashboard />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}

export default App;
