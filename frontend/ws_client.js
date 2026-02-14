 // TRAYAM — frontend/ws_client.js

const WS_URL = "ws://127.0.0.1:8000/ws";

let socket;

export function connectWebSocket(onEmotion) {
  socket = new WebSocket(WS_URL);

  socket.onopen = () => {
    console.log("✅ WebSocket connected");
  };

  socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "safe_mode") {
  window.dispatchEvent(new Event("safe_mode"));
  return;
  }

  if (data.type === "narrative") {
    window.dispatchEvent(new CustomEvent("narrative", { detail: data }));
    return;
  }

  if (onEmotion) {
    onEmotion(data);
  }
};


  socket.onclose = () => {
    console.log("⚠️ WebSocket closed — retrying in 2s");
    setTimeout(() => connectWebSocket(onEmotion), 2000);
  };

  socket.onerror = (err) => {
    console.error("WebSocket error:", err);
  };
}

