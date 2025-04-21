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
import WelcomePage from './WelcomePage'; 

function App() {
  return (
    <Router>
      <MainApp />
    </Router>
  );
}

function MainApp() {
  const location = useLocation(); 

  return (
    <div className="App">
      <header className="App-header">
        
        {location.pathname !== '/register' && location.pathname !== '/login' &&  location.pathname !== '/lecturer-dashboard' && (
          <img src={logo} className="App-logo" alt="logo" />
        )}
      </header>
    
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
