import React, { useState } from "react";
import api from "../components/AxiosInstance"; // Import Axios
import "../components/Register.css"; // CSS file

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student"); // Default to 'student'
  const [studentNumber, setStudentNumber] = useState("");
  const [course, setCourse] = useState("");
  const [year, setYear] = useState("");
  const [staffId, setStaffId] = useState("");
  const [college, setCollege] = useState("");
  const [school, setSchool] = useState("");
  const [department, setDepartment] = useState("");
  const [officeLocation, setOfficeLocation] = useState(""); // For academic registrar
  const [officeHours, setOfficeHours] = useState(""); // For academic registrar

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = {
      email,
      password,
      role,
      studentNumber,
      course,
      year,
      staffId,
      college,
      school,
      department,
      officeLocation,
      officeHours,
    };

    try {
      formData["confirm_password"] = password; // Assuming confirm password is same as password

      console.log("Form Data:", formData); // Log the form data for debugging
      const response = await api.post("register/", formData);
      console.log("Registration successful:", response.data);
      alert("Registration successful!");
    } catch (error) {
      console.error("Error during registration:", error);
      alert("Registration failed. Please try again.");
    }
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
          <div className="custom-dropdown">
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
            <div className="dropdown-icon">
              <span>&#9662;</span> {/* Down arrow icon */}
            </div>
          </div>
        </div>

        {/* Display student fields if role is student */}
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

        {/* Display lecturer fields if role is lecturer */}
        {role === "lecturer" && (
          <>
            <div className="input-group">
              <label htmlFor="staffId">Staff ID:</label>
              <input
                type="text"
                id="staffId"
                name="staffId"
                value={staffId}
                onChange={(e) => setStaffId(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="college">College:</label>
              <input
                type="text"
                id="college"
                name="college"
                value={college}
                onChange={(e) => setCollege(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="school">School:</label>
              <input
                type="text"
                id="school"
                name="school"
                value={school}
                onChange={(e) => setSchool(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="department">Department:</label>
              <input
                type="text"
                id="department"
                name="department"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                required
              />
            </div>
          </>
        )}

        {/* Display academic registrar fields if role is academic_registrar */}
        {role === "academic_registrar" && (
          <>
            <div className="input-group">
              <label htmlFor="staffId">Staff ID:</label>
              <input
                type="text"
                id="staffId"
                name="staffId"
                value={staffId}
                onChange={(e) => setStaffId(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="officeLocation">Office Location:</label>
              <input
                type="text"
                id="officeLocation"
                name="officeLocation"
                value={officeLocation}
                onChange={(e) => setOfficeLocation(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="officeHours">Office Hours:</label>
              <input
                type="text"
                id="officeHours"
                name="officeHours"
                value={officeHours}
                onChange={(e) => setOfficeHours(e.target.value)}
                required
              />
            </div>
          </>
        )}

        <button type="submit">Register</button>
        <p className="login-link">Already have an account? <a href="/login">Log in</a></p>


      </form>
    </div>
  );
};

export default Register;

