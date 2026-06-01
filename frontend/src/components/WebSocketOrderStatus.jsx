import { useEffect } from "react";

export default function WebSocketOrderStatus({ orderId, onStatus }) {
  useEffect(() => {
    if (!orderId) {
      return undefined;
    }
    const socket = new WebSocket(`ws://localhost:8000/ws/orders/${orderId}/`);
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      onStatus(payload);
    };
    return () => socket.close();
  }, [orderId, onStatus]);

  return null;
}
