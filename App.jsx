import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"; // Import React Router
import StudentDashboard from "./pages/StudentDashboard"; // Student Dashboard component
import LecturerDashboard from "./pages/LecturerDashboard"; // Lecturer Dashboard component
import AcademicRegistrarDashboard from "./pages/AcademicRegistrarDashboard"; // Academic Registrar Dashboard component
import Login from "./pages/Login";
import Register from "./pages/Register";
//import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
  const [userRole, setUserRole] = useState(null); // Track the user role from login

  useEffect(() => {
    // Check if a user role exists in localStorage
    const role = localStorage.getItem("userRole");
    if (role) {
      setUserRole(role);
    }
  }, []);

  const handleLogin = (role) => {
    // Set the role when the user logs in and store it in localStorage
    localStorage.setItem("userRole", role);
    setUserRole(role);
  };

  return (
    <Router>
      <div>
        {/* Define Routes for Dashboards */}
        <Routes>
          <Route
            path="/student"
            element={userRole === "student" ? <StudentDashboard /> : <Navigate to="/login" />}
          />
          <Route
            path="/lecturer"
            element={userRole === "lecturer" ? <LecturerDashboard /> : <Navigate to="/login" />}
          />
          <Route
            path="/academic-registrar"
            element={userRole === "academic_registrar" ? <AcademicRegistrarDashboard /> : <Navigate to="/login" />}
          />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          {/* You could have a catch-all route here for unrecognized paths */}
          <Route path="/" element={<Navigate to="/register" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
