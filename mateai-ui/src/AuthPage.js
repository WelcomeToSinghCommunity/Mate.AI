import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function AuthPage({ onAuth }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    const endpoint = isLogin ? "/login" : "/signup";

    try {
      const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (isLogin) {
        // Save JWT token to localStorage
        localStorage.setItem("authToken", data.token);
        onAuth(data.token);
        navigate("/dashboard");
      } else {
        alert("Signup successful! Please log in.");
        setIsLogin(true);
      }
    } catch (err) {
      console.error("Error:", err);
      alert("Something went wrong");
    }
  }

  return (
    <div style={{ backgroundColor: "black", color: "white", minHeight: "100vh", padding: "2rem" }}>
      <h1>{isLogin ? "Login" : "Signup"}</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", marginBottom: "1rem" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: "block", marginBottom: "1rem" }}
        />
        <button type="submit">{isLogin ? "Login" : "Signup"}</button>
      </form>
      <p style={{ marginTop: "1rem" }}>
        {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
        <button onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "Signup" : "Login"}
        </button>
      </p>
    </div>
  );
}

export default AuthPage;
