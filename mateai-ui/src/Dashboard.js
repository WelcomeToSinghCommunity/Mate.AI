import React, { useEffect, useState } from "react";
import { apiRequest } from "./api";
import { ReactMic } from "react-mic";

function Dashboard({ onLogout }) {
  const [summary, setSummary] = useState("");
  const [tasks, setTasks] = useState([]);
  const [chatReply, setChatReply] = useState("");
  const [recording, setRecording] = useState(false);

  useEffect(() => {
    async function loadData() {
      const summaryData = await apiRequest("/summary");
      setSummary(summaryData.summary);

      const tasksData = await apiRequest("/tasks");
      setTasks(tasksData.tasks);
    }
    loadData();
  }, []);

  async function sendChat(question) {
    const reply = await apiRequest("/chat", "POST", { question });
    setChatReply(reply.answer);
  }

  // 🎤 Handle audio upload to FastAPI
  async function onStop(recordedBlob) {
    const formData = new FormData();
    formData.append("file", recordedBlob.blob, "audio.wav");

    const response = await fetch("http://127.0.0.1:8000/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setSummary(data.summary);
    setTasks(data.tasks);
    sendChat(data.summary); // optional: auto‑ask about summary
  }

  return (
    <div style={{ backgroundColor: "black", color: "white", minHeight: "100vh", padding: "2rem" }}>
      <h1>Mate.AI Dashboard</h1>
      <button onClick={onLogout}>Logout</button>

      <h2>Meeting Summary</h2>
      <p>{summary}</p>

      <h2>Tasks</h2>
      <ul>
        {tasks.map((task, idx) => <li key={idx}>{task}</li>)}
      </ul>

      <h2>Voice Input</h2>
      <ReactMic
        record={recording}
        className="sound-wave"
        onStop={onStop}
        mimeType="audio/wav"
      />
      <button onClick={() => setRecording(true)}>🎤 Start</button>
      <button onClick={() => setRecording(false)}>⏹ Stop</button>

      <h2>Chat Reply</h2>
      <p>{chatReply}</p>
    </div>
  );
}

export default Dashboard;
