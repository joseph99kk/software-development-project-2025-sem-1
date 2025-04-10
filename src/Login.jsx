import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate login and role retrieval (replace with actual API call)
    const mockResponse = { role: 'student' }; // Replace with actual role from backend
    console.log('Logging in:', formData);

    // Redirect based on role
    if (mockResponse.role === 'student') {
      navigate('/student-dashboard');
    } else if (mockResponse.role === 'registrar') {
      navigate('/registrar-dashboard');
    } else if (mockResponse.role === 'lecturer') {
      navigate('/lecturer-dashboard');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
