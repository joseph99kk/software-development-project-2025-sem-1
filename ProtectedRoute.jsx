// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const authToken = localStorage.getItem('authToken'); // Check if the token exists in localStorage

  if (!authToken) {
    return <Navigate to="/login" />; // Redirect to login if no token is found
  }

  return children; // Render the protected component if the user is authenticated
};

export default ProtectedRoute;
