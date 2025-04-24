import React, { useState } from 'react';
import './StudentDashboard.css';
function StudentDashboard() {
  const [issue, setIssue] = useState({ title: '', description: '' });
  const [wordCount, setWordCount] = useState(0);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setIssue({ ...issue, [name]: value });
  };

    if (name === 'description') {
       const words = value.trim().split(/\s+/); // Split by spaces
       setWordCount(value.trim() === '' ? 0 : words.length);
    }
};


  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitting Issue:', issue);
    // Add logic to send the issue to the backend or API
    alert('Issue submitted successfully!');
    setIssue({ title: '', description: '' }); // Reset the form
    setWordCount(0); // Reset word count
  };

  return (
    <div className="student-dashboard">
      <h1>Welcome to the Student Dashboard</h1>
      <h2>Submit an Issue </h2>
      <form onSubmit={handleSubmit} className="issue-form">
        <div className="form-group">
          <label htmlFor="title">Issue Title:</label>
          <input
            type="text"
            id="title"
            name="title"
            value={issue.title}
            onChange={handleChange}
            placeholder="Enter the issue title"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Issue Description:</label>
          <textarea
            id="description"
            name="description"
            value={issue.description}
            onChange={handleChange}
            placeholder="Describe the issue in detail"
            required
          />
        </div>
        <button type="submit" className="submit-button">Submit Issue</button>
      </form>
    </div>
  );
}

export default StudentDashboard;