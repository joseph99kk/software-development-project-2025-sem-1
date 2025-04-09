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
    profilePic: "default-profile.png", // Should ideally be a real image URL
  };

  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  const handleDescriptionChange = (e) => {
    const text = e.target.value;
    setWordCount(text.length); // Changed from counting only letters
    setIssueDetails(text);
  };

  // Fetch issues using useEffect
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

