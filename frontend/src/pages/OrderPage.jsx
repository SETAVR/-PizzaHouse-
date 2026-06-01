import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/client";
import OrderStatus from "../components/OrderStatus";
import WebSocketOrderStatus from "../components/WebSocketOrderStatus";

export default function OrderPage() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    api.get(`/orders/${id}/`).then((response) => setOrder(response.data));
  }, [id]);

  const handleStatus = useCallback((payload) => {
    setOrder((current) => current ? { ...current, status: payload.status, is_paid: payload.is_paid } : current);
  }, []);

  const payOrder = async () => {
    const response = await api.post(`/orders/${id}/pay/`);
    setOrder(response.data);
  };

  if (!order) {
    return <main className="container">Загрузка...</main>;
  }

  return (
    <main className="container">
      <WebSocketOrderStatus orderId={order.id} onStatus={handleStatus} />
      <h1>Заказ #{order.id}</h1>
      <OrderStatus status={order.status} />
      <p>Телефон: {order.phone}</p>
      <p>Адрес: {order.address}</p>
      <p>Сумма: {Number(order.total_price).toFixed(0)} ₽</p>
      <ul className="plain-list">
        {order.items.map((item) => (
          <li key={item.id}>{item.pizza_title} x {item.quantity}</li>
        ))}
      </ul>
      {!order.is_paid && <button onClick={payOrder}>Оплатить условно</button>}
    </main>
  );
}
