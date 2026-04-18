import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthPage from "./AuthPage";
import Dashboard from "./Dashboard";

function App() {
  const [token, setToken] = useState(null);

  // Load token from localStorage when app starts
  useEffect(() => {
    const savedToken = localStorage.getItem("authToken");
    if (savedToken) {
      setToken(savedToken);
    }
  }, []);

  // Save token to localStorage when user logs in
  const handleAuth = (newToken) => {
    localStorage.setItem("authToken", newToken);
    setToken(newToken);
  };

  // Logout function
  const handleLogout = () => {
    localStorage.removeItem("authToken");
    setToken(null);
  };

  return (
    <Router>
      <Routes>
        {/* Public route */}
        <Route path="/login" element={<AuthPage onAuth={handleAuth} />} />

        {/* Protected route */}
        <Route
          path="/dashboard"
          element={token ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" />}
        />

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
