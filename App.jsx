import React, { useState, useEffect } from "react";
import "../components/StudentDashboard.css";
import axios from "../components/AxiosInstance";


const Dashboard = () => {
  const [activeSection, setActiveSection] = useState("home");
  const [wordCount, setWordCount] = useState(0);
  const [issueTitle, setIssueTitle] = useState("");
  const [courseCode, setCourseCode] = useState("");
  const [issueDetails, setIssueDetails] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [error, setError] = useState("");
  const [pendingIssues, setPendingIssues] = useState([]);

  const studentData = {
    name: localStorage.getItem("name") || "Student Name",
    course: "BSc. Computer Science",
    profilePic: "default-profile.png", 
  };

  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  const handleDescriptionChange = (e) => {
    const text = e.target.value;
    setWordCount(text.length); // Changed from counting only letters
    setIssueDetails(text);
  };

  
  useEffect(() => {
    const fetchIssues = async () => {
      try {
        const response = await axios.get("https://mercylina.pythonanywhere.com/api/issues/create/");
        setPendingIssues(response.data);
      } catch (err) {
        console.error("Failed to fetch issues:", err);
      }
    };

    fetchIssues();
  }, []);

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    if (wordCount > 200) {
      alert("Issue description cannot exceed 200 characters. Please revise it.");
      return;
    }

     const issueData = {
      title: issueTitle,
      course_code: courseCode,
      description: issueDetails,
      email: localStorage.getItem("email"),
    };

    try {
      setSuccessMessage("");
      setError("");

      const response = await axios.post(         


        "https://mercylina.pythonanywhere.com/api/issues/create/",
        issueData,
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 201) {
        setSuccessMessage("Issue submitted successfully!");
        setIssueTitle("");
        setCourseCode("");
        setIssueDetails("");
        setWordCount(0);
        window.alert("successful");
        window.location.reload();
      }
    } catch (error) {
      console.error("There was an error while submitting the issue:", error);
      setError("There was an error while submitting the issue. Please try again later.");
      setSuccessMessage("");
    }
  };

  return (
    <div className="dashboard">
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
            {studentData.profilePic === "default-profile.png" && "Profile Picture"}
          </div>
          <div className="profile-info">
            <p className="name">{studentData.name}</p>
            <p className="degree">{studentData.course}</p>
          </div>
        </div>
      </header>

      <main className="content">
        {activeSection === "home" && (
          <section id="home-section">
            <h2>Resolved Issues</h2>
            <div className="empty-state">
              <p>No resolved issues yet. Once issues are resolved, they'll show up here.</p>
            </div>

            <h2>Pending Issues</h2>
            <div className="issues" id="issuesID">
              {pendingIssues.length > 0 ? (
                pendingIssues.map((issue, index) => (
                  <div className="issue-item" key={index}>
                    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                      <h3>{issue.title}</h3>
                      <p><strong>Course Code:</strong> {issue.course_code}</p>
                      <p><strong>Description:</strong> {issue.description}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">
                  <p>Loading or no issues found.</p>
                </div>
              )}
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
            {error && <p className="error-message">{error}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}
            <form className="submit-issue-form" onSubmit={handleFormSubmit}>
              <label htmlFor="issue-title">Issue Title:</label>
              <input
                type="text"
                id="issue-title"
                placeholder="Enter the issue title"
                value={issueTitle}
                onChange={(e) => setIssueTitle(e.target.value)}
                name="title"
                required
              />

              <label htmlFor="course-code">Course code:</label>
              <input
                type="text"
                id="course-code"
                placeholder="Enter the course code"
                value={courseCode}
                onChange={(e) => setCourseCode(e.target.value)}
                name="course_code"
                required
              />

              <label htmlFor="issue-details">Issue Details:</label>
              <textarea
                id="issue-details"
                placeholder="Describe the issue (200 characters max)"
                value={issueDetails}
                onChange={handleDescriptionChange}
                name="description"
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

export default Dashboard;
