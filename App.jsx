import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; // Import React Router
import StudentDashboard from "./pages/StudentDashboard"; // Student Dashboard component
import LecturerDashboard from "./pages/LecturerDashboard"; // Lecturer Dashboard component
import AcademicRegistrarDashboard from "./pages/AcademicRegistrarDashboard"; // Academic Registrar Dashboard component
import Dashboard from "./components/Dashboard"; 
import Login from "./pages/Login";


const App = () => {
  const [issues, setIssues] = useState([]);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [notification, setNotification] = useState("");

  const addIssue = (issue) => {
    const newIssue = { ...issue, id: issues.length + 1, status: "Open" };
    setIssues([...issues, newIssue]);
    setNotification("New issue added!");
    setTimeout(() => setNotification(""), 3000);
  };

  const selectIssue = (issue) => {
    setSelectedIssue(issue);
  };

  return (
    <Router>
      <div>
        {/* Define Routes for Dashboards */}
        <Routes>
          <Route path="/student" element={<StudentDashboard />} /> 
          <Route path="/Login" element={<Login /> } />
          <Route path="/lecturer" element={<LecturerDashboard />} /> 
          <Route path="/academic registrar" element={<AcademicRegistrarDashboard />} />
        </Routes>

        {/* Existing Dashboard Components  */}
        <Dashboard 
          issues={issues} 
          selectIssue={selectIssue} 
          notification={notification} 
        />
        {/* <IssueForm addIssue={addIssue} /> */}
        {/* {selectedIssue && <IssueDetail issue={selectedIssue} />} */}
        {/* <Notification message={notification} /> */}
      </div>
    </Router>
  );
};

export default App;
