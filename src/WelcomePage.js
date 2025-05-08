// src/WelcomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './WelcomePage.css'; // if you have component-level styles

export default function WelcomePage() {
  return (
    <div
      className="welcome-container"
      style={{
        backgroundImage: `url(${'/college.jpg'})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        minHeight: '100vh',
      }}
    >
      
      <header className="site-header">
        <nav className="main-nav">
          <Link to="/">Home</Link>
          <Link to="/submit">Submit Issue</Link>
          <Link to="/status">My Tickets</Link>
          <Link to="/contact">Contact</Link>
        </nav>
        <div className="auth-buttons">
          <button className="login" aria-label="Login to your account">Login</button>
          <button className="signup" aria-label="Sign up for a new account">Sign Up</button>
        </div>
      </header>

      <main className="hero">
        <div className="hero-text">
          <h1>Welcome to the Issue Submission Portal</h1>
          <p>
            Have a question, concern, or suggestion about campus life or academics?  
            Use this portal to submit your issue, attach screenshots or documents,  
            and track its status in real time. Our support team will be in touch ASAP!
          </p>
          <button className="btn-submit" aria-label="Submit an issue">Submit an Issue</button>
        </div>
        <div className="hero-image">
          
        </div>
      </main>
    </div>
  );
}
