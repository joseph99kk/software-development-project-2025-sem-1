import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
// import IssueForm from "./components/IssueForm";
import IssueDetail from "./components/IssueDetail";
import Notification from "./components/Notification";
import StudentDashboard from "./pages/StudentDashboard";

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
    <div>
      <StudentDashboard />
      {/* Pass issues, selectIssue, and notification as props  */}
      <Dashboard 
        issues={issues} 
        selectIssue={selectIssue} 
        notification={notification} 
      />
      {/* <IssueForm addIssue={addIssue} /> */}
      {/* {selectedIssue && <IssueDetail issue={selectedIssue} />} */}
      {/* <Notification message={notification} /> */}
    </div>
  );
};

export default App;
