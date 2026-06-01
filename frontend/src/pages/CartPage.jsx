import { Link } from "react-router-dom";
import CartItem from "../components/CartItem";
import { useCart } from "../context/CartContext";

export default function CartPage() {
  const { items, total, updateQuantity, removeFromCart } = useCart();

  return (
    <main className="container">
      <h1>Корзина</h1>
      {!items.length && <p>Корзина пуста.</p>}
      {items.map((item) => (
        <CartItem key={item.pizza.id} item={item} onQuantityChange={updateQuantity} onRemove={removeFromCart} />
      ))}
      <div className="summary">
        <strong>Итого: {total.toFixed(0)} ₽</strong>
        <Link className={`button-link ${!items.length ? "disabled" : ""}`} to="/checkout">Оформить заказ</Link>
      </div>
    </main>
  );
}
