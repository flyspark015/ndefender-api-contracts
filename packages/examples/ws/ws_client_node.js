// Usage:
//   WS_URL=ws://127.0.0.1:8001/api/v1/ws node ws_client_node.js
//   WS_URL=wss://<host>/api/v1/ws node ws_client_node.js

const WebSocket = require("ws");

const wsUrl = process.env.WS_URL || "ws://127.0.0.1:8001/api/v1/ws";
const timeoutMs = 5000;
let gotMessage = false;

console.log(`CONNECTING ${wsUrl}`);
const ws = new WebSocket(wsUrl);

const timer = setTimeout(() => {
  if (!gotMessage) {
    console.error("NO_MESSAGE_WITHIN_5S");
    ws.terminate();
    process.exit(2);
  }
}, timeoutMs);

ws.on("open", () => {
  console.log("CONNECTED");
});

ws.on("message", (data) => {
  if (!gotMessage) {
    gotMessage = true;
    clearTimeout(timer);
    try {
      const parsed = JSON.parse(data.toString());
      console.log(JSON.stringify(parsed));
    } catch (e) {
      console.log(data.toString());
    }
    ws.close(1000);
    process.exit(0);
  }
});

ws.on("close", (code, reason) => {
  if (!gotMessage) {
    console.error(`CLOSED ${code} ${reason ? reason.toString() : ""}`.trim());
  }
});

ws.on("error", (err) => {
  console.error("WS_ERROR", err && err.message ? err.message : err);
});
