export async function apiRequest(endpoint, method = "GET", body = null) {
  const token = localStorage.getItem("authToken");

  const response = await fetch(`http://localhost:8000${endpoint}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: body ? JSON.stringify(body) : null
  });

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return response.json();
}
