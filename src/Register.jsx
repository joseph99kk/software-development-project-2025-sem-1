import React, { useState } from 'react';

function Register() {
  const [formData, setFormData] = useState({ email:'', password: '' , role: ''});

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Send POST request to your Django registration endpoint here
    console.log('Registering:', formData);
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="email" placeholder="email" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <select name="role" onChange={handleChange} required>
          <option value="">Select Role</option>
          <option value="lecturer">Lecturer</option>
          <option value="registrar">Registrar</option>  
          <option value="student">Student</option>
        </select>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
