import React, { useState, useEffect } from "react";
import "../components/LecturerDashboard.css"; 

const LecturerDashboard = () => {
  const [activeSection, setActiveSection] = useState("home"); // State to track active section
  const [receivedIssues, setReceivedIssues] = useState([]); // State for received issues
  const [resolvedIssues, setResolvedIssues] = useState([]); // State for resolved issues
  const [assignedIssues, setAssignedIssues] = useState([]); // State for assigned issues

  // Switch between sections
  const switchSection = (section) => {
    setActiveSection(section);
  };

  // Fetch data from backend APIs 
  const fetchReceivedIssues = async () => {
    const response = await fetch("API_ENDPOINT_FOR_RECEIVED_ISSUES");
    const data = await response.json();
    setReceivedIssues(data);
  };

  const fetchResolvedIssues = async () => {
    const response = await fetch("API_ENDPOINT_FOR_RESOLVED_ISSUES");
    const data = await response.json();
    setResolvedIssues(data);
  };

  const fetchAssignedIssues = async () => {
    const response = await fetch("API_ENDPOINT_FOR_ASSIGNED_ISSUES");
    const data = await response.json();
    setAssignedIssues(data);
  };

  // Fetch issues when the Home section is active
  useEffect(() => {
    if (activeSection === "home") {
      fetchReceivedIssues();
      fetchResolvedIssues();
      fetchAssignedIssues();
    }
  }, [activeSection]);

  return (
    <div className="dashboard">
      {/* Header Section */}
      <header className="header">
        <div className="logo-container">
          <img src="graduation-hat-logo.png" alt="AITS Logo" className="logo" />
        </div>
        <nav className="nav">
          <button
            onClick={() => switchSection("home")}
            className={`nav-btn ${activeSection === "home" ? "active" : ""}`}
          >
            Home
          </button>
          <button
            onClick={() => switchSection("notifications")}
            className={`nav-btn ${activeSection === "notifications" ? "active" : ""}`}
          >
            Notifications
          </button>
          <button
            onClick={() => switchSection("review-issues")}
            className={`nav-btn ${activeSection === "review-issues" ? "active" : ""}`}
          >
            Review Issues
          </button>
        </nav>
        <div className="profile">
          <div
            id="profile-picture"
            className="profile-pic"
            style={{
              backgroundImage: `url(default-profile.png)`,
              backgroundSize: "cover",
            }}
          >
            Profile Picture
          </div>
          <div className="profile-info">
            <p id="lecturer-name" className="name"></p>
            <p id="lecturer-title" className="degree">Lecturer</p>
          </div>
        </div>
      </header>

      {/* Main Content Section */}
      <main className="content">
        {activeSection === "home" && (
          <section id="home-section">
            <h2>Received Issues</h2>
            <div id="received-issues" className="issue-list">
              {receivedIssues.length > 0 ? (
                <ul>
                  {receivedIssues.map((issue) => (
                    <li key={issue.id}>
                      {issue.title} - <strong>{issue.student}</strong>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No received issues at the moment.</p>
              )}
            </div>
            <h2>Resolved Issues</h2>
            <div id="resolved-issues" className="issue-list">
              {resolvedIssues.length > 0 ? (
                <ul>
                  {resolvedIssues.map((issue) => (
                    <li key={issue.id}>
                      {issue.title} - Resolved on {issue.resolvedOn}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No resolved issues yet.</p>
              )}
            </div>
            <h2>Assigned Issues</h2>
            <div id="assigned-issues" className="issue-list">
              {assignedIssues.length > 0 ? (
                <ul>
                  {assignedIssues.map((issue) => (
                    <li key={issue.id}>
                      {issue.title} - Assigned by {issue.assignedBy}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No assigned issues.</p>
              )}
            </div>
          </section>
        )}

        {activeSection === "notifications" && (
          <section id="notifications-section">
            <h2>Notifications</h2>
            <p>No notifications available.</p>
          </section>
        )}

        {activeSection === "review-issues" && (
          <section id="review-issues-section">
            <h2>Review Issues</h2>
            <p>This section is for reviewing student-submitted issues.</p>
          </section>
        )}
      </main>

      {/* Footer Section */}
      <footer>
        <div className="footer-container">
          <p>
            <strong>Info:</strong> Makerere University
          </p>
          <p>
            <strong>AITS:</strong> Academic Issue Tracking System
          </p>
          <p>
            <strong>Contact Us:</strong> (256) 700953462 |{" "}
            <a href="mailto:AITS@gmail.com">AITS@gmail.com</a>
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LecturerDashboard;
