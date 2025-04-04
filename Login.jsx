import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import "../components/Login.css";

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevents the form from refreshing the page

    // Simple email and password validation
    if (email === '' || password === '') {
      setErrorMessage('Please fill out both fields!');
      return;
    }

    try {
      // Make an API call to validate user credentials
      const response = await axios.post('https://mercylina.pythonanywhere.com/api/login/', {
        email,
        password,
      });

      // Assuming the API returns a token and role
      const { token, role } = response.data;


      console.log(token, role); // Log the token and role for debugging

      // Store the token in localStorage
      localStorage.setItem('authToken', token);
      localStorage.setItem('userRole', role); // Store the user role
      localStorage.setItem('email', response.data.user.email); // Store the email

      // Redirect based on the role
      if (role === 'student') {
        window.location.href = '/student'; // Redirect to student dashboard
      } else if (role === 'lecturer') {
        window.location.href = '/lecturer'; // Redirect to lecturer dashboard
      } else if (role === 'academic_registrar') {
        window.location.href = '/academic-registrar'; // Redirect to registrar dashboard
      }
    } catch (error) {
      console.error('Login failed:', error);
      setErrorMessage('Invalid credentials. Please try again.');
    }
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

