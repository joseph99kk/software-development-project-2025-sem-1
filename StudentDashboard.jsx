import React from "react";
import "../components/StudentDashboard.css" 
import axios from "axios";  // Importing axios for API requests


import { useState } from "react";

const Dashboard = () => {
  // These are states for managing active sections and word count
  const [activeSection, setActiveSection] = useState("home");
  const [wordCount, setWordCount] = useState(0);

  // Dummy data for profile
  const studentData = {
    name: " ",
    course: "BSc. Computer Science",
    profilePic: "default-profile.png", // To be replaced with actual path
  };

  // Handles switching between sections
  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  // Handle counting characters for the "Submit New Issue" description
  const handleDescriptionChange = (e) => {
    const text = e.target.value;
    const letters = text.split("").filter((char) => /[a-zA-Z]/.test(char));
    setWordCount(letters.length);
    setIssueDetails(text);
  };

  // Handle form submission with validation
  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (wordCount > 200) {
      alert("Issue description cannot exceed 200 characters. Please revise it.");
    } else {
      const issueData = {
        title:issueTitle,
        course_code:courseCode,
        
      
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
            onClick={() => handleSectionChange("home")}
            className={`nav-btn ${activeSection === "home" ? "active" : ""}`}
          >
            Home
          </button>
          <button
            onClick={() => handleSectionChange("notifications")}
            className={`nav-btn ${activeSection === "notifications" ? "active" : ""}`}
          >
            Notifications
          </button>
          <button
            onClick={() => handleSectionChange("new-issue")}
            className={`nav-btn ${activeSection === "new-issue" ? "active" : ""}`}
          >
            Submit New Issue
          </button>
        </nav>
        <div className="profile">
          <div
            id="profile-picture"
            className="profile-pic"
            style={{
              backgroundImage: `url(${studentData.profilePic})`,
              backgroundSize: "cover",
            }}
          >
            {!studentData.profilePic && "Profile Picture"}
          </div>
          <div className="profile-info">
            <p className="name">{studentData.name}</p>
            <p className="degree">{studentData.course}</p>
          </div>
        </div>
      </header>

      {/* Main Content Section */}
      <main className="content">
        {activeSection === "home" && (
          <section id="home-section">
            <h2>Resolved Issues</h2>
            <div className="empty-state">
              <p>No resolved issues yet. Once issues are resolved, they'll show up here.</p>
            </div>
            <h2>Pending Issues</h2>
            <div className="empty-state">
              <p>No pending issues yet. Submit an issue to track it here.</p>
            </div>
          </section>
        )}

        {activeSection === "notifications" && (
          <section id="notifications-section">
            <h2>Notifications</h2>
            <div className="notification">
              <p>No notifications yet. Notifications about updates or issues will appear here.</p>
            </div>
          </section>
        )}

        {activeSection === "new-issue" && (
          <section id="new-issue-section">
            <h2>Submit New Issue</h2>
            <form className="submit-issue-form" onSubmit={handleFormSubmit}>
              <label htmlFor="issue-title">Issue Title:</label>
              <input
                type="text"
                id="issue-title"
                placeholder="Enter the issue title"
                required
              />

              <label htmlFor="course-code">Course code:</label>
              <input
                type="text"
                id="course-unit"
                placeholder="Enter the course code"
                required
              />

              <label htmlFor="issue-details">Issue Details:</label>
              <textarea
                id="issue-details"
                placeholder="Describe the issue (200 characters max)"
                onChange={handleDescriptionChange}
                required
              ></textarea>
              <small style={{ color: wordCount > 200 ? "red" : "gray" }}>
                {wordCount}/200 characters
              </small>

              <button type="submit">Submit Issue</button>
            </form>
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

export default Dashboard;
