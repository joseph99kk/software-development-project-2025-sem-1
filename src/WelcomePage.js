import React from 'react';
import { Link } from 'react-router-dom';

function WelcomePage() {
  return (
    <div className="welcome-page">
      <h1>Welcome to the University Issue Submission  Portal</h1>
      <p className="welcome-message">
      Thank you for visiting . Click Below to proceed with Registration:</p>
      <Link to="/register" className="register-button">Register</Link>
      <p>If you already have an account, please login:</p>
        <Link to="/login" className="login-button">Login</Link>

    </div>
  );
}
export default WelcomePage;