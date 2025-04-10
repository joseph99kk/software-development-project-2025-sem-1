import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes ,Link} from 'react-router-dom';
import IssueForm from './IssueForm';
import LecturerDashboard from './LecturerDashboard';
import RegistrarDashboard from './RegistrarDashboard';
import Register from './Register';
import Login from './Login';
function App() {
  return (
    <Router>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
           
      </header>
      <nav>
        <ul>  
          <li><Link to="/welcome-page"></Link></li>
          
        </ul>
      </nav>
      <Routes>
        <Route path="/welcome-page" element={<WelcomePage />} />
        <Route path="/" element={<IssueForm />} />
        <Route path="/lecturer-dashboard" element={<LecturerDashboard />} />
        <Route path="/registrar-dashboard" element={<RegistrarDashboard />} />
        <Route path="/register" element={<Register/>} />  
        <Route path="/login" element={<Login/>} />
      </Routes>
    </div>
    </Router>
  );
      
}

export default App;
