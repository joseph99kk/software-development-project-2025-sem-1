import React, { useState } from "react";
import "../components/Register.css"; // Including the CSS file

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student"); // Default to 'student'
  const [studentNumber, setStudentNumber] = useState("");
  const [course, setCourse] = useState("");
  const [year, setYear] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission (send to API or validate)
    console.log({
      email,
      password,
      role,
      studentNumber,
      course,
      year,
    });
  };

  return (
    <div className="register-container">
      <h2 style={{ color: 'purple' }}>Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="role">Role:</label>
          <select
            id="role"
            name="role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          >
            <option value="student">Student</option>
            <option value="lecturer">Lecturer</option>
            <option value="academic_registrar">Academic Registrar</option>
          </select>
        </div>

        {role === "student" && (
          <>
            <div className="input-group">
              <label htmlFor="studentNumber">Student Number:</label>
              <input
                type="text"
                id="studentNumber"
                name="studentNumber"
                value={studentNumber}
                onChange={(e) => setStudentNumber(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="course">Course:</label>
              <input
                type="text"
                id="course"
                name="course"
                value={course}
                onChange={(e) => setCourse(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="year">Year:</label>
              <input
                type="number"
                id="year"
                name="year"
                value={year}
                onChange={(e) => setYear(e.target.value)}
                required
              />
            </div>
          </>
        )}

        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
