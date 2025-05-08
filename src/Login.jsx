import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Logging in:', formData);

    // Simulate backend response
    const mockResponse = { success: true, role: 'student' }; // Replace with actual API call

    if (mockResponse.success) {
      if (mockResponse.role === 'student') {
        navigate('/student-dashboard');
      } else if (mockResponse.role === 'registrar') {
        navigate('/registrar-dashboard');
      } else if (mockResponse.role === 'lecturer') {
        navigate('/lecturer-dashboard');
      }
    } else {
      alert('Invalid username or password. Please try again.');
    }
  };

  return (
    <div className="login-dashboard">
      <h1>Login</h1>
      <p className="login-description">Please enter your credentials here.</p>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          name="email"
          placeholder="email"
          value={formData.username}
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
}


export default Login;
