import React, { useState } from 'react';
import "../components/Login.css";

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevents the form from refreshing the page

    // Simple email and password validation
    if (email === '' || password === '') {
      setErrorMessage('Please fill out both fields!');
      return;
    }

    // Mock API call to validate user and get the role (replace with actual API call)
    setTimeout(() => {
      const mockUsers = [
        { email: 'student@example.com', password: 'password123', role: 'student' },
        { email: 'lecturer@example.com', password: 'password123', role: 'lecturer' },
        { email: 'registrar@example.com', password: 'password123', role: 'academic_registrar' },
      ];

      const user = mockUsers.find((u) => u.email === email && u.password === password);

      if (user) {
        setErrorMessage('');
        alert('Login successful!');

        // Store the role and other information (e.g., token)
        localStorage.setItem('userRole', user.role);

        // Redirect based on the role
        if (user.role === 'student') {
          window.location.href = '/student-dashboard';  // Redirect to student dashboard
        } else if (user.role === 'lecturer') {
          window.location.href = '/lecturer-dashboard';  // Redirect to lecturer dashboard
        } else if (user.role === 'academic_registrar') {
          window.location.href = '/registrar-dashboard';  // Redirect to registrar dashboard
        }
      } else {
        // Invalid login credentials
        setErrorMessage('Invalid credentials. Please try again.');
      }
    }, 1000); // Simulate network delay (remove this in production)
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form id="loginForm" onSubmit={handleSubmit}>
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
        <button type="submit">Login</button>
      </form>
      {errorMessage && <p id="error-message" style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
};

export default Login;
