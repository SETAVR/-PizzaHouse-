import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";

export default function CheckoutPage() {
  const { user } = useAuth();
  const { items, clearCart } = useCart();
  const navigate = useNavigate();
  const [phone, setPhone] = useState(user?.phone || "");
  const [address, setAddress] = useState(user?.address || "");
  const [error, setError] = useState("");

  const submitOrder = async (event) => {
    event.preventDefault();
    if (!items.length) {
      setError("Нельзя оформить пустую корзину.");
      return;
    }
    if (!phone.trim() || !address.trim()) {
      setError("Телефон и адрес обязательны.");
      return;
    }
    const payload = {
      phone,
      address,
      items: items.map((item) => ({ pizza_id: item.pizza.id, quantity: item.quantity })),
    };
    const response = await api.post("/orders/", payload);
    clearCart();
    navigate(`/orders/${response.data.id}`);
  };

  return (
    <main className="container narrow">
      <h1>Оформление заказа</h1>
      <form className="form" onSubmit={submitOrder}>
        {error && <p className="form-error">{error}</p>}
        <label>Телефон<input value={phone} onChange={(event) => setPhone(event.target.value)} /></label>
        <label>Адрес<input value={address} onChange={(event) => setAddress(event.target.value)} /></label>
        <button type="submit">Создать заказ</button>
      </form>
    </main>
  );
}
