import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

function Register() {
  const [formData, setFormData] = useState({ email: '', password: '', role: '' });
  const navigate = useNavigate();

  
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Registering:', formData);

    // Simulate backend response
    const mockResponse = { success: true, role: formData.role };

    if (mockResponse.success) {
      if (mockResponse.role === 'student') {
        navigate('/student-dashboard');
      } else if (mockResponse.role === 'registrar') {
        navigate('/registrar-dashboard');
      } else if (mockResponse.role === 'lecturer') {
        navigate('/lecturer-dashboard');
      }
    }
  };

  return (
    <div className="register-dashboard">
      <h1>Register</h1>
      <p className="register-description">Please fill out the form below to create an account.</p>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <select name="role" value={formData.role} onChange={handleChange} required>
          <option value="">Select Role</option>
          <option value="student">Student</option>
          <option value="registrar">Registrar</option>
          <option value="lecturer">Lecturer</option>
        </select>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
