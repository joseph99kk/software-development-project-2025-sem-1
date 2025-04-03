// src/utils/axios.js
import axios from 'axios';

// Creating an Axios instance with baseURL pointing to Django API
const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Django backend URL
  headers: {
    'Content-Type': 'application/json', // Content-type header for requests
  },
});

export default api;
