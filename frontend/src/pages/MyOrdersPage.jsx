import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import { orderStatusLabels } from "../components/OrderStatus";

export default function MyOrdersPage() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/orders/my/").then((response) => setOrders(response.data));
  }, []);

  return (
    <main className="container">
      <h1>Мои заказы</h1>
      {!orders.length && <p>Заказов пока нет.</p>}
      <div className="list">
        {orders.map((order) => (
          <Link className="list-row" to={`/orders/${order.id}`} key={order.id}>
            <span>#{order.id}</span>
            <span>{orderStatusLabels[order.status]}</span>
            <strong>{Number(order.total_price).toFixed(0)} ₽</strong>
          </Link>
        ))}
      </div>
    </main>
  );
}
