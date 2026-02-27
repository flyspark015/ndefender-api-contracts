// Usage:
//   WS_URL=ws://127.0.0.1:8001/api/v1/ws node ws_client_node.js
//   WS_URL=wss://<host>/api/v1/ws node ws_client_node.js

const wsUrl = process.env.WS_URL || "ws://127.0.0.1:8001/api/v1/ws";

const ws = new WebSocket(wsUrl);
ws.onmessage = (evt) => {
  try {
    const data = JSON.parse(evt.data);
    console.log(JSON.stringify(data));
  } catch {
    console.log(evt.data);
  }
};
ws.onopen = () => console.log("connected");
ws.onerror = (err) => console.error("ws error", err);
