import React, { useState, useEffect } from "react";
import "../components/AcademicRegistrarDashboard.css";

const AcademicRegistrarDashboard = () => {
  const [activeSection, setActiveSection] = useState("home"); // State to track active section
  const [receivedIssues, setReceivedIssues] = useState([]); // State for received issues
  const [resolvedIssues, setResolvedIssues] = useState([]); // State for resolved issues
  const [assignedIssues, setAssignedIssues] = useState([]); // State for assigned issues
  const [pendingIssues, setPendingIssues] = useState([]); // State for pending issues
  const [availableLecturers, setAvailableLecturers] = useState([]); // State for available lecturers
  const [selectedLecturer, setSelectedLecturer] = useState(""); // State for selected lecturer
  const [selectedIssue, setSelectedIssue] = useState(""); // State for selected issue

  // Fetching data from backend APIs
  const fetchReceivedIssues = async () => {
    const response = await fetch("https://mercylina.pythonanywhere.com/");
    const data = await response.json();
    setReceivedIssues(data);
  };

  const fetchResolvedIssues = async () => {
    const response = await fetch("https://mercylina.pythonanywhere.com");
    const data = await response.json();
    setResolvedIssues(data);
  };

  const fetchAssignedIssues = async () => {
    const response = await fetch("https://mercylina.pythonanywhere.com/");
    const data = await response.json();
    setAssignedIssues(data);
  };

  const fetchPendingIssues = async () => {
    const response = await fetch("https://mercylina.pythonanywhere.com/");
    const data = await response.json();
    setPendingIssues(data);
  };

  const fetchAvailableLecturers = async () => {
    const response = await fetch("https://mercylina.pythonanywhere.com/");
    const data = await response.json();
    setAvailableLecturers(data);
  };

  // Fetch issues when the Home section is active
  useEffect(() => {
    if (activeSection === "home") {
      fetchReceivedIssues();
      fetchResolvedIssues();
      fetchAssignedIssues();
      fetchPendingIssues();
    }

    if (activeSection === "assign-issues") {
      fetchAvailableLecturers();
    }
  }, [activeSection]);

  // Switching between sections
  const switchSection = (section) => {
    setActiveSection(section);
  };

  // Handle issue selection
  const handleIssueSelect = (issueId) => {
    setSelectedIssue(issueId);
  };

  // Handle lecturer selection
  const handleLecturerSelect = (lecturerId) => {
    setSelectedLecturer(lecturerId);
  };

  // Handle issue assignment
  const handleAssignIssue = async () => {
    if (!selectedLecturer || !selectedIssue) {
      alert("Please select both an issue and a lecturer.");
      return;
    }

    const issue = pendingIssues.find((issue) => issue.id === selectedIssue);
    const lecturer = availableLecturers.find((lecturer) => lecturer.id === selectedLecturer);

    if (issue && lecturer) {
      // Call the API to assign the issue to the lecturer
      const response = await fetch("YOUR_API_ENDPOINT_FOR_ASSIGN_ISSUE", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          issueId: selectedIssue,
          lecturerId: selectedLecturer,
        }),
      });

      if (response.ok) {
        alert(`Assigned "${issue.title}" to ${lecturer.name}.`);
        setPendingIssues(pendingIssues.filter((issue) => issue.id !== selectedIssue));
      } else {
        alert("Failed to assign issue.");
      }
    }
  };

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
            onClick={() => switchSection("assign-issues")}
            className={`nav-btn ${activeSection === "assign-issues" ? "active" : ""}`}
          >
            Assign Issues
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
            <p id="registrar-name" className="name">Dr. Lwuma Joseph</p>
            <p id="registrar-title" className="degree">Academic Registrar</p>
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

        {activeSection === "assign-issues" && (
          <section id="assign-issues-section">
            <h2>Assign Issues</h2>
            <p>This section allows you to assign pending issues to relevant lecturers.</p>

            <div className="assign-issues-container">
              <div className="issues-list">
                <h3>Pending Issues</h3>
                <ul>
                  {pendingIssues.map((issue) => (
                    <li
                      key={issue.id}
                      className={selectedIssue === issue.id ? "selected" : ""}
                      onClick={() => handleIssueSelect(issue.id)}
                    >
                      {issue.title} - Raised by {issue.student}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="lecturer-selection">
                <h3>Select Lecturer</h3>
                <select onChange={(e) => handleLecturerSelect(Number(e.target.value))} value={selectedLecturer}>
                  <option value="">Select Lecturer</option>
                  {availableLecturers.map((lecturer) => (
                    <option key={lecturer.id} value={lecturer.id}>
                      {lecturer.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="assign-btn">
                <button onClick={handleAssignIssue}>Assign Issue</button>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer Section */}
      <footer>
        <div className="footer-container">
          <p><strong>Info:</strong> Makerere University</p>
          <p><strong>AITS:</strong> Academic Issue Tracking System</p>
          <p><strong>Contact Us:</strong> (256) 700953462 | <a href="mailto:AITS@gmail.com">AITS@gmail.com</a></p>
        </div>
      </footer>
    </div>
  );
};

export default AcademicRegistrarDashboard;
